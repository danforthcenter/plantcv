import pytest
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.analyze import bound_horizontal as analyze_bound_horizontal
from plantcv.plantcv.analyze.bound_horizontal import _boundary_img_annotation


# Foreground spans rows 10:90: a line below it (95) gives the full 80 px height, a line crossing
# the stem (50) gives rows 10-49 (40 px), and lines above it (5) or negative (-1) give 0
@pytest.mark.parametrize('pos,exp', [[95, 80], [-1, 0], [5, 0], [50, 40]])
def test_analyze_bound_horizontal(pos, exp, synthetic_rgb, synthetic_mask):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    _ = analyze_bound_horizontal(img=synthetic_rgb, labeled_mask=synthetic_mask, simplify=True,
                                 n_labels=1, line_position=pos)
    assert outputs.observations["default_1"]["height_above_reference"]["value"] == exp
    assert outputs.observations["default_1"]["area_above_reference"]["label"] == "pixels"
    assert outputs.observations["default_1"]["area_below_reference"]["label"] == "pixels"


def test_analyze_bound_horizontal_grayscale_image(synthetic_gray, synthetic_mask):
    """Test for PlantCV."""
    boundary_img = analyze_bound_horizontal(img=synthetic_gray, labeled_mask=synthetic_mask, simplify=False,
                                            n_labels=1, line_position=95)
    assert len(boundary_img.shape) == 2


def test_analyze_bound_horizontal_simplify_labels(synthetic_rgb, synthetic_mask):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Line crosses the stem so foreground lies on both sides
    labeled = analyze_bound_horizontal(img=synthetic_rgb, labeled_mask=synthetic_mask, simplify=True,
                                       n_labels=1, line_position=50, label="prefix")
    # Simplified output is 1 above the line and 2 below
    assert np.array_equal(np.unique(labeled), [0, 1, 2])
    assert np.count_nonzero(labeled) == np.count_nonzero(synthetic_mask)
    assert "prefix_1" in outputs.observations


@pytest.mark.parametrize("axis", [0, 1])
def test_boundary_img_annotation_simplify_colors(axis):
    """Test for PlantCV."""
    # Two objects on either side of the line plus one straddling it
    mask = np.zeros((50, 100), dtype=np.int32)
    mask[5:15, 5:20] = 1
    mask[35:45, 60:80] = 2
    mask[20:30, 40:60] = 3
    img = np.zeros((50, 100, 3), dtype=np.uint8)
    out_img, out_mask = _boundary_img_annotation(img, mask, [25, 50][axis], axis, simplify=True)
    colors = {tuple(c) for c in out_img.reshape(-1, 3)}
    # Both sides of the boundary are painted
    assert (255, 0, 255) in colors
    assert (0, 255, 0) in colors
    assert np.array_equal(np.unique(out_mask), [0, 1, 2])
