"""Tests for the color_correction module."""
import pytest
import os
import numpy as np
from plantcv.plantcv._globals import outputs
from plantcv.plantcv.transform.color_correction import (calc_transformation_matrix,
                                                        apply_transformation_matrix, save_matrix, load_matrix, correct_color,
                                                        create_color_card_mask, affine_color_correction)
from plantcv.plantcv.transform.get_color_matrix import get_color_matrix, get_matrix_m
from plantcv.plantcv.transform.standard_matrices import std_color_matrix, astro_color_matrix
from plantcv.plantcv.transform.detect_color_card import detect_color_card
from tests import synthetic


def test_affine_color_correction():
    """Test for Plantcv."""
    outputs.clear()
    # apply affine color correction to an image and check that the chip colors
    # get closer to the standard values
    img = synthetic.color_cast(synthetic.color_card())
    # The first chip is centered at (85, 85) and the chips are 70 px apart
    mask = create_color_card_mask(rgb_img=img, radius=20, start_coord=(85, 85),
                                  spacing=(70, 70), nrows=6, ncols=4)
    _, s_matrix = get_color_matrix(rgb_img=img, mask=mask)
    t_matrix = std_color_matrix(pos=3)
    corrected_img = affine_color_correction(rgb_img=img, source_matrix=s_matrix,
                                            target_matrix=t_matrix)
    _, c_matrix = get_color_matrix(rgb_img=corrected_img, mask=mask)

    # calculate Euclidean distance between the chip values
    # between the standard values and the source image
    dist_source = np.sum((s_matrix - t_matrix)**2)
    # between the standard values and the corrected image
    dist_correct = np.sum((c_matrix - t_matrix)**2)

    assert dist_correct <= dist_source
    # The cast is a per-channel scale, which the affine correction undoes up to rounding: recorded value 1
    # (8-bit units; each chip is uniform, so its mean is a whole number of 8-bit units)
    assert np.max(np.abs(np.rint(c_matrix[:, 1:] * 255) - np.rint(t_matrix[:, 1:] * 255))) <= 1


def test_affine_color_correction_bad_shape():
    """Test for PlantCV."""
    img = synthetic.color_card()
    t_matrix = std_color_matrix(pos=3)
    with pytest.raises(RuntimeError):
        _ = affine_color_correction(rgb_img=img, source_matrix=t_matrix,
                                    target_matrix=t_matrix[0:-1, :])


@pytest.mark.parametrize("pos", [0, 1, 2, 3])
def test_std_color_matrix(pos):
    """Test for PlantCV."""
    std_matrix = std_color_matrix(pos=pos)

    # indices for the color matrix where the white chip should be depending on
    # the value of pos
    white_indices = [18, 23, 5, 0]
    white_idx_pos = white_indices[pos]

    # RGB values in white chip of the returned matrix in the range [0-1]
    white_val = std_matrix[white_idx_pos, 1:]

    # RGB values of the white chip in the range [0-255]
    white_rgb = np.array([243., 243., 242.], dtype=np.float64)
    # compare RGB values in the range [0-255]
    assert np.sum(np.abs(255*white_val - white_rgb)) < 1


def test_std_color_matrix_bad_pos():
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = std_color_matrix(pos=4.5)


def test_astro_color_matrix():
    """Test for PlantCV."""
    astro_matrix = astro_color_matrix()

    # Index and RGB values (range [0-1]) of the yellow chip in color matrix
    yellow_idx = 3
    yellow_val = astro_matrix[yellow_idx, 1:]

    # RGB values of the yellow chip
    yellow_rgb = np.array([228., 207., 50.], dtype=np.float64)

    # compare RGB values in the range [0-255]
    assert np.sum(np.abs(255*yellow_val - yellow_rgb)) < 1


def test_get_color_matrix():
    """Test for PlantCV."""
    # Each chip of the card is uniform with its standard color
    _, matrix = get_color_matrix(synthetic.color_card(), synthetic.color_card_mask())
    assert np.allclose(matrix, std_color_matrix(pos=3), rtol=0, atol=1e-12)


def test_get_color_matrix_img():
    """Test for PlantCV."""
    # Two gray-scale images
    mask = synthetic.color_card_mask()
    # The input for rgb_img needs to be an RGB image
    with pytest.raises(RuntimeError):
        _, _ = get_color_matrix(mask, mask)


def test_get_color_matrix_mask():
    """Test for PlantCV."""
    # A 3-channel mask
    mask = np.dstack([synthetic.color_card_mask()] * 3)
    # The mask needs to be a gray-scale image
    with pytest.raises(RuntimeError):
        _, _ = get_color_matrix(synthetic.color_card(), mask)


def _powers(matrix):
    """R, R^2, R^3, G, G^2, G^3, B, B^2, B^3 columns of a color matrix."""
    return np.column_stack([matrix[:, c] ** p for c in (1, 2, 3) for p in (1, 2, 3)])


def test_get_matrix_m():
    """Test for PlantCV."""
    t_matrix = std_color_matrix(pos=3)
    s_matrix = synthetic.color_cast_matrix(t_matrix)
    matrix_a, matrix_m, matrix_b = get_matrix_m(t_matrix, s_matrix)
    # matrix_a holds the source R, G, B, then their squares, then their cubes
    expected_a = np.column_stack([s_matrix[:, 1:] ** p for p in (1, 2, 3)])
    assert np.array_equal(matrix_a, expected_a)
    # matrix_m is the left inverse of matrix_a
    assert np.allclose(matrix_m @ matrix_a, np.eye(9), rtol=0, atol=1e-6)
    assert np.array_equal(matrix_b, _powers(t_matrix))


def test_get_matrix_m_unequal_data():
    """Test for PlantCV."""
    t_matrix = std_color_matrix(pos=3)
    # The source is missing chips 30 and 60; only the matching chips are used
    s_matrix = np.delete(synthetic.color_cast_matrix(t_matrix), [2, 5], axis=0)
    matrix_a, matrix_m, matrix_b = get_matrix_m(t_matrix, s_matrix)
    expected_a = np.column_stack([s_matrix[:, 1:] ** p for p in (1, 2, 3)])
    assert np.array_equal(matrix_a, expected_a)
    assert np.allclose(matrix_m @ matrix_a, np.eye(9), rtol=0, atol=1e-6)
    assert np.array_equal(matrix_b, _powers(np.delete(t_matrix, [2, 5], axis=0)))


def _cast_transformation():
    """Transformation from the cast standard colors back to the standard colors, and the exact solution."""
    t_matrix = std_color_matrix(pos=3)
    _, matrix_m, matrix_b = get_matrix_m(t_matrix, synthetic.color_cast_matrix(t_matrix))
    # Target R = source R / 0.7 (and so on), so target R^p = source R^p / 0.7^p: the fit is exact and diagonal
    scale = 1 / np.array([0.7, 0.8, 0.9])
    expected = np.diag(np.concatenate([scale, scale ** 2, scale ** 3]))
    return matrix_m, matrix_b, expected


def test_calc_transformation_matrix():
    """Test for PlantCV."""
    matrix_m, matrix_b, expected = _cast_transformation()
    deviance, matrix_t = calc_transformation_matrix(matrix_m, matrix_b)
    assert np.allclose(matrix_t, expected, rtol=0, atol=1e-6)
    assert deviance == pytest.approx(1 - np.prod(np.diag(expected)))


def test_calc_transformation_matrix_b_incorrect():
    """Test for PlantCV."""
    matrix_m, matrix_b, _ = _cast_transformation()
    matrix_b = np.asmatrix(matrix_b, float)
    with pytest.raises(RuntimeError):
        _, _ = calc_transformation_matrix(matrix_m, matrix_b.T)


def test_calc_transformation_matrix_not_mult():
    """Test for PlantCV."""
    matrix_m, matrix_b, _ = _cast_transformation()
    with pytest.raises(RuntimeError):
        _, _ = calc_transformation_matrix(matrix_m, matrix_b[:3])


def test_calc_transformation_matrix_not_mat():
    """Test for PlantCV."""
    matrix_m, matrix_b, _ = _cast_transformation()
    with pytest.raises(RuntimeError):
        _, _ = calc_transformation_matrix(matrix_m[:, 1], matrix_b[:, 1])


def _half_square_transformation():
    """Transformation that maps every channel x (0-1) to 0.5 * x + 0.5 * x^2."""
    matrix_t = np.zeros((9, 9))
    for c in range(3):
        # Column c is the output channel c (R, G, B); rows c and c + 3 are that channel and its square
        matrix_t[c, c] = 0.5
        matrix_t[c + 3, c] = 0.5
    return matrix_t


def test_apply_transformation():
    """Test for PlantCV."""
    # x = 0, 0.2, 0.4, 0.6, 0.8, 1 maps to 0, 0.12, 0.28, 0.48, 0.72, 1, and 255 times those values truncates to
    # 0, 30, 71, 122, 183, 255
    values = np.array([0, 51, 102, 153, 204, 255], dtype=np.uint8)
    expected = np.array([0, 30, 71, 122, 183, 255], dtype=np.uint8)
    # Give each channel its own order of the values
    order = np.array([[0, 1, 2, 3, 4, 5], [5, 4, 3, 2, 1, 0], [2, 3, 4, 5, 0, 1]])
    source_img = np.dstack([values[o] for o in order])
    corrected_img = apply_transformation_matrix(source_img, _half_square_transformation())
    assert np.array_equal(corrected_img, np.dstack([expected[o] for o in order]))


def test_apply_transformation_incorrect_t():
    """Test for PlantCV."""
    # A 24 x 9 matrix, like matrix_b
    _, matrix_b, _ = _cast_transformation()
    with pytest.raises(RuntimeError):
        _ = apply_transformation_matrix(synthetic.color_card(), matrix_b)


def test_apply_transformation_incorrect_img():
    """Test for PlantCV."""
    source_img = synthetic.color_card_mask()
    with pytest.raises(RuntimeError):
        _ = apply_transformation_matrix(source_img, _half_square_transformation())


def test_save_matrix(tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    # .npz filename
    filename = os.path.join(cache_dir, 'test.npz')
    save_matrix(_half_square_transformation(), filename)
    assert os.path.exists(filename) is True


def test_save_matrix_incorrect_filename():
    """Test for PlantCV."""
    # .npz filename
    filename = "test"
    with pytest.raises(RuntimeError):
        save_matrix(_half_square_transformation(), filename)


def test_load_matrix(tmp_path):
    """Test for PlantCV."""
    matrix_t = _half_square_transformation()
    filename = str(tmp_path / "matrix_t.npz")
    np.savez(filename, matrix_t)
    matrix_t_loaded = load_matrix(filename)
    assert np.array_equal(matrix_t, matrix_t_loaded)


def _doubling_cards():
    """Source card with half the standard chip values and target card with twice those values."""
    halves = std_color_matrix(pos=3)
    halves[:, 1:] = np.floor(halves[:, 1:] * 255 / 2) / 255
    doubles = halves.copy()
    doubles[:, 1:] *= 2
    return synthetic.color_card(colors=doubles), synthetic.color_card(colors=halves)


@pytest.mark.parametrize("subdir", ["", "outputs"])
def test_correct_color(subdir, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory; correct_color creates the output directory if it does not exist
    cache_dir = os.path.join(tmpdir.mkdir("cache"), subdir)
    target_img, source_img = _doubling_cards()
    mask = synthetic.color_card_mask()
    _, _, matrix_t, corrected_img = correct_color(target_img, mask, source_img, mask, cache_dir)
    # The target chips are twice the source chips, so the fit is exact: R, G, B scale by 2, their squares by 4
    # and their cubes by 8
    assert np.allclose(matrix_t, np.diag([2, 2, 2, 4, 4, 4, 8, 8, 8]), rtol=0, atol=1e-6)
    # Every pixel doubles, up to 255; truncation of the floating point result can take off 1
    expected = np.minimum(2 * source_img.astype(int), 255)
    assert np.max(np.abs(corrected_img.astype(int) - expected)) <= 1
    assert all([os.path.exists(os.path.join(cache_dir, "target_matrix.npz")) is True,
                os.path.exists(os.path.join(cache_dir, "source_matrix.npz")) is True,
                os.path.exists(os.path.join(cache_dir, "transformation_matrix.npz")) is True])


def test_create_color_card_mask():
    """Test for PlantCV."""
    rgb_img = synthetic.color_card()
    mask = create_color_card_mask(rgb_img=rgb_img, radius=20, start_coord=(85, 85), spacing=(70, 70), nrows=6,
                                  ncols=4, exclude=[20, 0])
    # 22 chips remain, labeled 10 to 220
    assert np.array_equal(np.unique(mask), np.arange(0, 230, 10))
    # Label 10 * k is chip k (counting from 0) for k up to 19 and chip k + 1 after that
    chip_labels = synthetic.color_card_mask()
    for k in range(1, 23):
        chip = k if k < 20 else k + 1
        assert np.all(chip_labels[mask == 10 * k] == 10 * (chip + 1))


def test_cameratrax_and_astro_consistent_color_calibration():
    """Test for PlantCV."""
    rgb_img = synthetic.color_cast(synthetic.color_card_scene())

    # Correct with cameratrax card and measure corrected astrocard values
    ctrax_mat = detect_color_card(rgb_img=rgb_img)
    ctrax_std_mat = std_color_matrix(pos=3)
    ctrax_corr_img = affine_color_correction(rgb_img=rgb_img, source_matrix=ctrax_mat, target_matrix=ctrax_std_mat)

    # Correct with astrocard and measure corrected astrocard values
    astro_mat = detect_color_card(rgb_img=rgb_img, color_chip_size="astro")
    astro_std_mat = astro_color_matrix()
    astro_corr_img = affine_color_correction(rgb_img=rgb_img, source_matrix=astro_mat, target_matrix=astro_std_mat)

    # Subtract as signed integers; uint8 subtraction would wrap a difference of -1 around to 255
    diff = np.abs(ctrax_corr_img.astype(int) - astro_corr_img.astype(int))
    channel_diffs = np.sum(diff, axis=(0, 1)) / (diff.shape[0] * diff.shape[1])
    # Check for similarity in corrected color: mean absolute color difference less than 2.5 (1% of range)
    assert all(channel_diffs < 3) and np.mean(channel_diffs) < 2.5
    # Both cards carry the same cast, so the two corrections agree up to rounding: recorded value 1
    assert np.max(diff) <= 1
