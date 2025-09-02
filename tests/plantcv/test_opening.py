import pytest
import cv2
import numpy as np
from plantcv.plantcv import opening, Objects


def test_opening_binary(test_data):
    """Test for PlantCV."""
    # Read in test data
    bin_img = cv2.imread(test_data.small_bin_img, -1)
    filtered_img = opening(gray_img=bin_img)
    # Assert that the output image has the dimensions of the input image and is binary
    assert bin_img.shape == filtered_img.shape and np.array_equal(np.unique(filtered_img), np.array([0, 255]))


def test_opening_binary_roi(test_data):
    """Test for PlantCV."""
    # Read in test data
    bin_img = cv2.imread(test_data.small_bin_img, -1)
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    filtered_img = opening(gray_img=bin_img, roi=roi)
    # Assert that the output image has the dimensions of the input image and is binary
    assert bin_img.shape == filtered_img.shape and np.array_equal(np.unique(filtered_img), np.array([0, 255]))


def test_opening_grayscale(test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    filtered_img = opening(gray_img=gray_img)
    assert gray_img.shape == filtered_img.shape


def test_opening_grayscale_roi(test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    filtered_img = opening(gray_img=gray_img, roi=roi)
    assert gray_img.shape == filtered_img.shape


def test_opening_bad_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    rgb_img = cv2.imread(test_data.small_rgb_img)
    with pytest.raises(RuntimeError):
        _ = opening(gray_img=rgb_img)
