"""Tests for the color_correction module."""
import pytest
import os
import cv2
import numpy as np
from altair.vegalite.v5.api import Chart
from plantcv.plantcv.transform import (get_color_matrix, get_matrix_m, calc_transformation_matrix, apply_transformation_matrix,
                                       save_matrix, load_matrix, correct_color, create_color_card_mask, quick_color_check,
                                       find_color_card, std_color_matrix, affine_color_correction)
from plantcv.plantcv import outputs


def test_affine_color_correction(transform_test_data):
    """Test for Plantcv."""
    # apply affine color correction to an image and check that the chip colors
    # get closer to the standard values
    img = cv2.imread(transform_test_data.colorcard_img)
    # parameters hard coded for the image used
    mask = create_color_card_mask(rgb_img=img, radius=20, start_coord=(1000, 400),
                                  spacing=(145, 145), nrows=6, ncols=4)
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


def test_affine_color_correction_bad_shape(transform_test_data):
    """Test for PlantCV."""
    img = cv2.imread(transform_test_data.colorcard_img)
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


def test_get_color_matrix(transform_test_data):
    """Test for PlantCV."""
    # load in target_matrix
    matrix_compare = transform_test_data.load_npz(transform_test_data.target_matrix_file)
    # Read in rgb_img and gray-scale mask
    rgb_img = cv2.imread(transform_test_data.target_img)
    mask = cv2.imread(transform_test_data.colorcard_mask, -1)
    # The result should be a len(np.unique(mask))-1 x 4 matrix
    _, matrix = get_color_matrix(rgb_img, mask)
    assert np.array_equal(matrix, matrix_compare)


def test_get_color_matrix_img(transform_test_data):
    """Test for PlantCV."""
    # Read in two gray-scale images
    rgb_img = cv2.imread(transform_test_data.colorcard_mask, -1)
    mask = cv2.imread(transform_test_data.colorcard_mask, -1)
    # The input for rgb_img needs to be an RGB image
    with pytest.raises(RuntimeError):
        _, _ = get_color_matrix(rgb_img, mask)


def test_get_color_matrix_mask(transform_test_data):
    """Test for PlantCV."""
    # Read in two gray-scale images
    rgb_img = cv2.imread(transform_test_data.target_img)
    mask = cv2.imread(transform_test_data.colorcard_mask)
    # The input for rgb_img needs to be an RGB image
    with pytest.raises(RuntimeError):
        _, _ = get_color_matrix(rgb_img, mask)


def test_get_matrix_m(transform_test_data):
    """Test for PlantCV."""
    # load in comparison matrices
    matrix_compare_m = transform_test_data.load_npz(transform_test_data.matrix_m1_file)
    matrix_compare_b = transform_test_data.load_npz(transform_test_data.matrix_b1_file)
    # read in matrices
    t_matrix = transform_test_data.load_npz(transform_test_data.target_matrix_file)
    s_matrix = transform_test_data.load_npz(transform_test_data.source1_matrix_file)
    # apply matrices to function
    _, matrix_m, matrix_b = get_matrix_m(t_matrix, s_matrix)
    matrix_compare_m = np.rint(matrix_compare_m)
    matrix_compare_b = np.rint(matrix_compare_b)
    matrix_m = np.rint(matrix_m)
    matrix_b = np.rint(matrix_b)
    assert np.array_equal(matrix_m, matrix_compare_m) and np.array_equal(matrix_b, matrix_compare_b)


def test_get_matrix_m_unequal_data(transform_test_data):
    """Test for PlantCV."""
    # load in comparison matrices
    matrix_compare_m = transform_test_data.load_npz(transform_test_data.matrix_m2_file)
    matrix_compare_b = transform_test_data.load_npz(transform_test_data.matrix_b2_file)
    # read in matrices
    t_matrix = transform_test_data.load_npz(transform_test_data.target_matrix_file)
    s_matrix = transform_test_data.load_npz(transform_test_data.source2_matrix_file)
    # apply matrices to function
    _, matrix_m, matrix_b = get_matrix_m(t_matrix, s_matrix)
    matrix_compare_m = np.rint(matrix_compare_m)
    matrix_compare_b = np.rint(matrix_compare_b)
    matrix_m = np.rint(matrix_m)
    matrix_b = np.rint(matrix_b)
    assert np.array_equal(matrix_m, matrix_compare_m) and np.array_equal(matrix_b, matrix_compare_b)


def test_calc_transformation_matrix(transform_test_data):
    """Test for PlantCV."""
    # load in comparison matrices
    matrix_compare = transform_test_data.load_npz(transform_test_data.transformation_matrix_file)
    # read in matrices
    matrix_m = transform_test_data.load_npz(transform_test_data.matrix_m1_file)
    matrix_b = transform_test_data.load_npz(transform_test_data.matrix_b1_file)
    # apply to function
    _, matrix_t = calc_transformation_matrix(matrix_m, matrix_b)
    matrix_t = np.rint(matrix_t)
    matrix_compare = np.rint(matrix_compare)
    assert np.array_equal(matrix_t, matrix_compare)


def test_calc_transformation_matrix_b_incorrect(transform_test_data):
    """Test for PlantCV."""
    # read in matrices
    matrix_m = transform_test_data.load_npz(transform_test_data.matrix_m1_file)
    matrix_b = transform_test_data.load_npz(transform_test_data.matrix_b1_file)
    matrix_b = np.asmatrix(matrix_b, float)
    with pytest.raises(RuntimeError):
        _, _ = calc_transformation_matrix(matrix_m, matrix_b.T)


def test_calc_transformation_matrix_not_mult(transform_test_data):
    """Test for PlantCV."""
    # read in matrices
    matrix_m = transform_test_data.load_npz(transform_test_data.matrix_m1_file)
    matrix_b = transform_test_data.load_npz(transform_test_data.matrix_b1_file)
    with pytest.raises(RuntimeError):
        _, _ = calc_transformation_matrix(matrix_m, matrix_b[:3])


def test_calc_transformation_matrix_not_mat(transform_test_data):
    """Test for PlantCV."""
    # read in matrices
    matrix_m = transform_test_data.load_npz(transform_test_data.matrix_m1_file)
    matrix_b = transform_test_data.load_npz(transform_test_data.matrix_b1_file)
    with pytest.raises(RuntimeError):
        _, _ = calc_transformation_matrix(matrix_m[:, 1], matrix_b[:, 1])


def test_apply_transformation(transform_test_data):
    """Test for PlantCV."""
    # load corrected image to compare
    corrected_compare = cv2.imread(transform_test_data.source_corrected)
    # read in matrices
    matrix_t = transform_test_data.load_npz(transform_test_data.transformation_matrix_file)
    # read in images
    target_img = cv2.imread(transform_test_data.target_img)
    source_img = cv2.imread(transform_test_data.source1_img)
    corrected_img = apply_transformation_matrix(source_img, target_img, matrix_t)
    # assert source and corrected have same shape
    assert np.array_equal(corrected_img, corrected_compare)


def test_apply_transformation_incorrect_t(transform_test_data):
    """Test for PlantCV."""
    # read in matrices
    matrix_t = transform_test_data.load_npz(transform_test_data.matrix_b1_file)
    # read in images
    target_img = cv2.imread(transform_test_data.target_img)
    source_img = cv2.imread(transform_test_data.source1_img)
    with pytest.raises(RuntimeError):
        _ = apply_transformation_matrix(source_img, target_img, matrix_t)


def test_apply_transformation_incorrect_img(transform_test_data):
    """Test for PlantCV."""
    # read in matrices
    matrix_t = transform_test_data.load_npz(transform_test_data.transformation_matrix_file)
    # read in images
    target_img = cv2.imread(transform_test_data.target_img)
    source_img = cv2.imread(transform_test_data.colorcard_mask, -1)
    with pytest.raises(RuntimeError):
        _ = apply_transformation_matrix(source_img, target_img, matrix_t)


def test_save_matrix(transform_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    # read in matrix
    matrix_t = transform_test_data.load_npz(transform_test_data.transformation_matrix_file)
    # .npz filename
    filename = os.path.join(cache_dir, 'test.npz')
    save_matrix(matrix_t, filename)
    assert os.path.exists(filename) is True


def test_save_matrix_incorrect_filename(transform_test_data):
    """Test for PlantCV."""
    # read in matrix
    matrix_t = transform_test_data.load_npz(transform_test_data.transformation_matrix_file)
    # .npz filename
    filename = "test"
    with pytest.raises(RuntimeError):
        save_matrix(matrix_t, filename)


def test_load_matrix(transform_test_data):
    """Test for PlantCV."""
    # read in matrix_t
    matrix_t = transform_test_data.load_npz(transform_test_data.transformation_matrix_file)
    # test load function with matrix_t
    matrix_t_loaded = load_matrix(transform_test_data.transformation_matrix_file)
    assert np.array_equal(matrix_t, matrix_t_loaded)


def test_correct_color(transform_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    # load corrected image to compare
    corrected_compare = cv2.imread(transform_test_data.source_corrected)
    # Read in target, source, and gray-scale mask
    target_img = cv2.imread(transform_test_data.target_img)
    source_img = cv2.imread(transform_test_data.source1_img)
    mask = cv2.imread(transform_test_data.colorcard_mask, -1)
    _, _, _, corrected_img = correct_color(target_img, mask, source_img, mask, cache_dir)
    # assert source and corrected have same shape
    assert all([np.array_equal(corrected_img, corrected_compare),
                os.path.exists(os.path.join(cache_dir, "target_matrix.npz")) is True,
                os.path.exists(os.path.join(cache_dir, "source_matrix.npz")) is True,
                os.path.exists(os.path.join(cache_dir, "transformation_matrix.npz")) is True])


def test_correct_color_output_dne(transform_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    cache_dir = os.path.join(tmp_dir, "outputs")
    # load corrected image to compare
    corrected_compare = cv2.imread(transform_test_data.source_corrected)
    # Read in target, source, and gray-scale mask
    target_img = cv2.imread(transform_test_data.target_img)
    source_img = cv2.imread(transform_test_data.source1_img)
    mask = cv2.imread(transform_test_data.colorcard_mask, -1)
    _, _, _, corrected_img = correct_color(target_img, mask, source_img, mask, cache_dir)
    # assert source and corrected have same shape
    assert all([np.array_equal(corrected_img, corrected_compare),
                os.path.exists(os.path.join(cache_dir, "target_matrix.npz")) is True,
                os.path.exists(os.path.join(cache_dir, "source_matrix.npz")) is True,
                os.path.exists(os.path.join(cache_dir, "transformation_matrix.npz")) is True])


def test_create_color_card_mask(transform_test_data):
    """Test for PlantCV."""
    # Load target image
    rgb_img = cv2.imread(transform_test_data.target_img)
    mask = create_color_card_mask(rgb_img=rgb_img, radius=6, start_coord=(166, 166), spacing=(21, 21), nrows=6, ncols=4,
                                  exclude=[20, 0])
    assert all([i == j] for i, j in zip(np.unique(mask), np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110,
                                                                   120, 130, 140, 150, 160, 170, 180, 190, 200, 210,
                                                                   220], dtype=np.uint8)))


def test_quick_color_check(transform_test_data):
    """Test for PlantCV."""
    # Load target image
    target_matrix = transform_test_data.load_npz(transform_test_data.target_matrix_file)
    source_matrix = transform_test_data.load_npz(transform_test_data.source1_matrix_file)
    chart = quick_color_check(target_matrix, source_matrix, num_chips=22)
    assert isinstance(chart, Chart)


def test_find_color_card(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.target_img)
    _ = find_color_card(rgb_img=rgb_img, threshold_type='adaptgauss', blurry=False, threshvalue=90)
    assert int(outputs.observations["default"]["color_chip_size"]["value"] / 100) == 2


def test_find_color_card_optional_parameters(transform_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    # Test with threshold ='normal'
    _, _, _ = find_color_card(rgb_img=rgb_img, threshold_type='normal', blurry=True, background='light',
                              threshvalue=90, label="prefix")
    assert int(outputs.observations["prefix"]["color_chip_size"]["value"] / 1000) == 15


def test_find_color_card_otsu(transform_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    # Test with threshold ='normal'
    _, _, _ = find_color_card(rgb_img=rgb_img, threshold_type='otsu', blurry=True, background='light',
                              threshvalue=90, label="prefix")
    assert int((outputs.observations["prefix"]["color_chip_size"]["value"] / 1000) + 0.5) == 15


def test_find_color_card_optional_size_parameters(transform_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    _, _, _ = find_color_card(rgb_img=rgb_img, record_chip_size="mean")
    assert int(outputs.observations["default"]["color_chip_size"]["value"] / 1000) == 15


def test_find_color_card_optional_size_parameters_none(transform_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    _, _, _ = find_color_card(rgb_img=rgb_img, record_chip_size=None)
    assert outputs.observations.get("default") is None


def test_find_color_card_bad_record_chip_size(transform_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.target_img)
    _, _, _ = find_color_card(rgb_img=rgb_img, record_chip_size='averageeeed')
    assert outputs.observations["default"]["color_chip_size"]["value"] is None


def test_find_color_card_bad_thresh_input(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.target_img)
    with pytest.raises(RuntimeError):
        _, _, _ = find_color_card(rgb_img=rgb_img, threshold_type='gaussian')


def test_find_color_card_bad_background_input(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.target_img)
    with pytest.raises(RuntimeError):
        _, _, _ = find_color_card(rgb_img=rgb_img, background='lite')


def test_find_color_card_none_found(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.target_img)
    with pytest.raises(RuntimeError):
        _, _, _ = find_color_card(rgb_img=rgb_img, threshold_type="otsu")
