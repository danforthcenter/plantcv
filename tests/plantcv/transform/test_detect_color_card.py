"""Tests for detect_color_card."""
import cv2
import pytest
import numpy as np
from plantcv.plantcv._globals import params
from plantcv.plantcv.transform.detect_color_card import detect_color_card


def test_detect_color_card(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    color_matrix = detect_color_card(rgb_img=rgb_img, color_chip_size="classic")
    params.function_args = {}
    assert np.shape(color_matrix) == (24, 4)


def test_detect_color_card_set_size(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    color_matrix = detect_color_card(rgb_img=rgb_img, color_chip_size=(40, 40))
    params.function_args = {}
    assert np.shape(color_matrix) == (24, 4)


def test_draw_nonuniform_color_chips(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    radii = [3*(i+1) for i in range(24)]
    color_matrix = detect_color_card(rgb_img=rgb_img, color_chip_size=(40, 40), radius=radii)
    params.function_args = {}
    assert np.shape(color_matrix) == (24, 4)


def test_draw_nonuniform_color_chips_len_mismatch(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    radii = [3*(i+1) for i in range(5)]
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, color_chip_size=(40, 40), radius=radii)
    params.function_args = {}


def test_detect_color_card_none_found(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.target_img)
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img)
    params.function_args = {}


def test_detect_color_card_incorrect_block_size(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, block_size=2)
    params.function_args = {}


def test_detect_color_card_partial_card(transform_test_data):
    """Test for PlantCV."""
    # load rgb image
    rgb_img = cv2.imread(transform_test_data.partial_card_rgb_img)
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, aspect_ratio=2, solidity=0.5)
    params.function_args = {}


def test_detect_color_card_incorrect_card_size(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, color_chip_size=100)
    params.function_args = {}


def test_detect_color_card_incorrect_card_type(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, color_chip_size="pantone")
    params.function_args = {}


def test_detect_color_card_masked_aruco_tags(transform_test_data, capsys):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.astrocard_img)
    _ = detect_color_card(rgb_img=rgb_img)
    params.function_args = {}
    captured = capsys.readouterr()
    assert captured.err == "Warning: Image contains an ArUco tag, should you be using color_chip_size='astro'?\n"


def test_detect_astro_card(transform_test_data):
    """Test for PlantCV."""
    rgb_img = cv2.imread(transform_test_data.astrocard_img)
    color_matrix = detect_color_card(rgb_img=rgb_img, color_chip_size="astro")
    params.function_args = {}
    assert np.shape(color_matrix) == (15, 4)


def test_detect_astro_card_missing_aruco_tags(transform_test_data):
    """Test for PlantCV."""
    rgb_img = cv2.imread(transform_test_data.astrocard_missing_tags)
    color_matrix = detect_color_card(rgb_img=rgb_img, color_chip_size="astro")
    params.function_args = {}
    assert np.shape(color_matrix) == (15, 4)


def test_detect_astro_card_duplicate_aruco_tags(transform_test_data):
    """Test for PlantCV."""
    rgb_img = cv2.imread(transform_test_data.duplicate_aruco_tags)
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, color_chip_size="astro")
    params.function_args = {}


def test_detect_astro_card_no_aruco_tags(transform_test_data):
    """Test for PlantCV."""
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, color_chip_size="astro")
    params.function_args = {}


def test_detect_astro_card_wrong_aruco_tags(transform_test_data):
    """Test for PlantCV."""
    rgb_img = cv2.imread(transform_test_data.wrong_aruco_tags)
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, color_chip_size="astro")
    params.function_args = {}
