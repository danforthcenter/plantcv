"""Tests for detect_color_card."""
import cv2
import pytest
import numpy as np
from plantcv.plantcv.transform import detect_color_card


def test_detect_color_card(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    labeled_mask = detect_color_card(rgb_img=rgb_img, color_chip_size="classic")
    assert len(np.unique(labeled_mask)) == 25


def test_detect_color_card_set_size(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    labeled_mask = detect_color_card(rgb_img=rgb_img, color_chip_size=(40, 40))
    assert len(np.unique(labeled_mask)) == 25


def test_draw_nonuniform_color_chips(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    radii = [3*(i+1) for i in range(24)]
    labeled_mask = detect_color_card(rgb_img=rgb_img, color_chip_size=(40, 40), radius=radii)
    assert len(np.unique(labeled_mask)) == 25


def test_draw_nonuniform_color_chips_len_mismatch(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    radii = [3*(i+1) for i in range(5)]
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, color_chip_size=(40, 40), radius=radii)


def test_detect_color_card_none_found(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.target_img)
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img)


def test_detect_color_card_incorrect_block_size(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, block_size=2)


def test_detect_color_card_partial_card(transform_test_data):
    """Test for PlantCV."""
    # load rgb image
    rgb_img = cv2.imread(transform_test_data.partial_card_rgb_img)
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img)


def test_detect_color_card_incorrect_card_size(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, color_chip_size=100)


def test_detect_color_card_incorrect_card_type(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, color_chip_size="pantone")


def test_detect_astro_card(transform_test_data):
    """Test for PlantCV."""
    rgb_img = cv2.imread(transform_test_data.astrocard_img)
    labeled_mask = detect_color_card(rgb_img=rgb_img, color_chip_size="astro")
    assert len(np.unique(labeled_mask)) == 16


def test_detect_astro_card_missing_aruco_tags(transform_test_data):
    """Test for PlantCV."""
    rgb_img = cv2.imread(transform_test_data.astrocard_missing_tags)
    labeled_mask = detect_color_card(rgb_img=rgb_img, color_chip_size="astro")
    assert len(np.unique(labeled_mask)) == 16


def test_detect_astro_card_duplicate_aruco_tags(transform_test_data):
    """Test for PlantCV."""
    rgb_img = cv2.imread(transform_test_data.duplicate_aruco_tags)
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, color_chip_size="astro")


def test_detect_astro_card_no_aruco_tags(transform_test_data):
    """Test for PlantCV."""
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, color_chip_size="astro")


def test_detect_astro_card_wrong_aruco_tags(transform_test_data):
    """Test for PlantCV."""
    rgb_img = cv2.imread(transform_test_data.wrong_aruco_tags)
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, color_chip_size="astro")
