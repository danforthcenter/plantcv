"""Tests for the find_color_card module."""
import pytest
import cv2
from plantcv.plantcv.transform import find_color_card
from plantcv.plantcv import outputs


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
