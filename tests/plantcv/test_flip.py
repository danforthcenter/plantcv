import pytest
import cv2
from plantcv.plantcv import flip


def test_flip(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    flipped_img = flip(img=img, direction="horizontal")
    assert img.shape == flipped_img.shape


def test_flip_grayscale(test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    flipped_img = flip(img=gray_img, direction="vertical")
    assert gray_img.shape == flipped_img.shape


def test_flip_bad_input(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    with pytest.raises(RuntimeError):
        _ = flip(img=img, direction="vert")
