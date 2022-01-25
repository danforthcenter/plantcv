import pytest
import cv2
import numpy as np
from plantcv.plantcv import canny_edge_detect


@pytest.mark.parametrize('color', ["white", "black"])
def test_canny_edge_detect(color, test_data):
    """Test for PlantCV."""
    # Read in test data
    rgb_img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    edge_img = canny_edge_detect(img=rgb_img, mask=mask, thickness=2, mask_color=color)
    # Assert that the output image has the dimensions of the input image and is binary
    assert rgb_img.shape[:2] == edge_img.shape and np.array_equal(np.unique(edge_img), np.array([0, 255]))


def test_canny_edge_detect_grayscale(test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(test_data.small_bin_img, -1)
    edge_img = canny_edge_detect(img=gray_img)
    # Assert that the output image has the dimensions of the input image and is binary
    assert gray_img.shape == edge_img.shape and np.array_equal(np.unique(edge_img), np.array([0, 255]))


def test_canny_edge_detect_bad_input(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_bin_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    with pytest.raises(RuntimeError):
        _ = canny_edge_detect(img=img, mask=mask, mask_color="gray")
