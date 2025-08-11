import pytest
import cv2
import numpy as np
from plantcv.plantcv import dilate, Objects


def test_dilate(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_bin_img, -1)
    dilate_img = dilate(gray_img=img, ksize=5, i=1)
    # Assert that the output image has the dimensions of the input image and is binary
    assert img.shape == dilate_img.shape and np.array_equal(np.unique(dilate_img), np.array([0, 255]))


def test_dilate_roi(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_bin_img, -1)
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    dilate_img = dilate(gray_img=img, ksize=5, i=1, roi=roi)
    # Assert that the output image has the dimensions of the input image and is binary
    assert img.shape == dilate_img.shape and np.array_equal(np.unique(dilate_img), np.array([0, 255]))


def test_dilate_small_k(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_bin_img, -1)
    with pytest.raises(ValueError):
        _ = dilate(gray_img=img, ksize=1, i=1)
