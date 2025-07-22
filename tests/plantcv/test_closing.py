import pytest
import cv2
import numpy as np
from plantcv.plantcv import closing, Objects


def test_closing(test_data):
    """Test for PlantCV."""
    # Read in test data
    bin_img = cv2.imread(test_data.small_bin_img, -1)
    filtered_img = closing(gray_img=bin_img)
    # Assert that the output image has the dimensions of the input image and is binary
    assert bin_img.shape == filtered_img.shape and np.array_equal(np.unique(filtered_img), np.array([0, 255]))


def test_closing_roi(test_data):
    """Test for PlantCV."""
    # Read in test data
    bin_img = cv2.imread(test_data.small_bin_img, -1)
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    filtered_img = closing(gray_img=bin_img, roi=roi)
    # Assert that the output image has the dimensions of the input image and is binary
    assert bin_img.shape == filtered_img.shape and np.array_equal(np.unique(filtered_img), np.array([0, 255]))


def test_closing_grayscale(test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    filtered_img = closing(gray_img=gray_img, kernel=np.ones((4, 4), np.uint8))
    assert np.sum(filtered_img) > np.sum(gray_img)


def test_closing_grayscale_roi(test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    roi_con = [np.array([[[0, 0]], [[0, 400]], [[355, 400]], [[355, 0]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    filtered_img = closing(gray_img=gray_img, kernel=np.ones((4, 4), np.uint8), roi=roi)
    assert np.sum(filtered_img) > np.sum(gray_img)


def test_closing_bad_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    rgb_img = cv2.imread(test_data.small_rgb_img)
    with pytest.raises(RuntimeError):
        _ = closing(gray_img=rgb_img)
