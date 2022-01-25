import pytest
import cv2
import numpy as np
from plantcv.plantcv import fill_holes


def test_fill_holes(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_bin_img, -1)
    fill_img = fill_holes(bin_img=img)
    # Assert that the output image has the dimensions of the input image and is binary
    assert img.shape == fill_img.shape and np.array_equal(np.unique(fill_img), np.array([0, 255]))


def test_fill_holes_bad_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = fill_holes(bin_img=img)
