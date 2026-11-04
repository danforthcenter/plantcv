import pytest
import numpy as np
from plantcv.plantcv.transform import merge_images
from tests import synthetic

TILES = np.array(synthetic.TILE_BGR, dtype=int)


def _merge_line(length, method):
    """Expected BGR values along the merge axis for 3 tiles of the given length overlapping by 30%."""
    # Same formula as merge_images: int(height * overlap_percentage / 100).
    n = int(length * 30 / 100)
    step = length - n
    line = np.zeros((3 * length - 2 * n, 3), dtype=int)
    line[:length] = TILES[0]
    for i in (1, 2):
        a, b = TILES[i - 1], TILES[i]
        start = i * step
        for x in range(n):
            # Weight of tile i: 1 (stacked), 1/2 (average), x/n (gradual). Neighboring tiles differ
            # by a multiple of 60, so with n = 3 or 6 every blend is a whole number.
            weight = {"stacked": (1, 1), "average": (1, 2), "gradual": (x, n)}[method]
            # given positive (b-a) and whole results / and // should be the same.
            # using / here to be exact.
            line[start + x] = a + (b - a) * weight[0] / weight[1]
        line[start + n:start + length] = b
    return line


def _expected(direction, method):
    """Expected merged image of the synthetic tiles."""
    rows, cols = synthetic.TILE_SHAPE
    if direction == "horizontal":
        line = _merge_line(cols, method)
        return np.broadcast_to(line[None, :, :], (rows, len(line), 3)).astype(np.uint8)
    line = _merge_line(rows, method)
    return np.broadcast_to(line[:, None, :], (len(line), cols, 3)).astype(np.uint8)


@pytest.mark.parametrize("direction", ["horizontal", "vertical"])
@pytest.mark.parametrize("method", ["stacked", "average", "gradual"])
def test_merge_images(direction, method, tmp_path):
    """Test for PlantCV."""
    # The tiles are sorted by name, so their order in the list does not matter
    tiles = synthetic.write_tiles(tmp_path)[::-1]
    merged_img = merge_images(tiles, overlap_percentage=30, direction=direction, method=method)
    # Horizontal: 20-px-wide tiles overlap by 6 px, 3 * 20 - 2 * 6 = 48 columns
    # Vertical: 10-px-tall tiles overlap by 3 px, 3 * 10 - 2 * 3 = 24 rows
    assert merged_img.shape == {"horizontal": (10, 48, 3), "vertical": (24, 20, 3)}[direction]
    assert np.array_equal(merged_img, _expected(direction, method))


@pytest.mark.parametrize("direction", ["horizontal", "vertical"])
def test_merge_images_random(direction, tmp_path):
    """Test for PlantCV."""
    merged_img = merge_images(synthetic.write_tiles(tmp_path), overlap_percentage=30,
                              direction=direction, method="random")
    if direction == "vertical":
        merged_img = merged_img.transpose(1, 0, 2)
    expected = _expected(direction, "stacked")
    if direction == "vertical":
        expected = expected.transpose(1, 0, 2)
    length = synthetic.TILE_SHAPE[1] if direction == "horizontal" else synthetic.TILE_SHAPE[0]
    n = int(length * 30 / 100)
    step = length - n
    overlaps = [range(i * step, i * step + n) for i in (1, 2)]
    in_overlap = np.zeros(merged_img.shape[1], dtype=bool)
    for i, cols in enumerate(overlaps, start=1):
        in_overlap[cols] = True
        # Each overlap shows either the earlier or the later tile, whole
        region = merged_img[:, cols]
        assert np.all(region == TILES[i - 1]) or np.all(region == TILES[i])
    assert np.array_equal(merged_img[:, ~in_overlap], expected[:, ~in_overlap])


def test_merge_images_dir(tmp_path):
    """Test for PlantCV."""
    synthetic.write_tiles(tmp_path)
    merged_img = merge_images(str(tmp_path), overlap_percentage=30, direction="vertical", method="gradual")
    assert np.array_equal(merged_img, _expected("vertical", "gradual"))
