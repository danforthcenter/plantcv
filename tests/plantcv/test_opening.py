import pytest
import numpy as np
from plantcv.plantcv import opening, Objects


def test_opening_binary(synthetic_mask):
    """Test for PlantCV."""
    filtered_img = opening(gray_img=synthetic_mask)
    # Assert that the output image has the dimensions of the input image and is binary
    assert synthetic_mask.shape == filtered_img.shape and np.array_equal(np.unique(filtered_img), np.array([0, 255]))


def test_opening_binary_roi(synthetic_mask):
    """Test for PlantCV."""
    # ROI in the background (rows 20:40, columns 10:30)
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    filtered_img = opening(gray_img=synthetic_mask, roi=roi)
    # Assert that the output image has the dimensions of the input image and is binary
    assert synthetic_mask.shape == filtered_img.shape and np.array_equal(np.unique(filtered_img), np.array([0, 255]))


def test_opening_grayscale(synthetic_gray):
    """Test for PlantCV."""
    filtered_img = opening(gray_img=synthetic_gray)
    assert synthetic_gray.shape == filtered_img.shape


def test_opening_grayscale_roi(synthetic_gray):
    """Test for PlantCV."""
    # ROI in the background (rows 20:40, columns 10:30)
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    filtered_img = opening(gray_img=synthetic_gray, roi=roi)
    assert synthetic_gray.shape == filtered_img.shape


def test_opening_bad_input(synthetic_rgb):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = opening(gray_img=synthetic_rgb)
