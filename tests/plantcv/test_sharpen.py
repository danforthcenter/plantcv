import cv2
import numpy as np
from plantcv.plantcv.classes import Objects
from plantcv.plantcv.sharpen import sharpen


def test_sharpen_zero_amount(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    sharp_img = sharpen(img, (5, 5), amount=0, threshold=0)
    assert np.average(img) == np.average(sharp_img)


def test_sharpen_any_amount(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    sharp_img = sharpen(img, (5, 5), amount=1, threshold=0)
    assert np.average(img) != np.average(sharp_img)


def test_sharpen_threshold(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    zero_thresh = sharpen(img, (5, 5), amount=1, threshold=0)
    thresh = sharpen(img, (5, 5), amount=1, threshold=100)
    assert np.average(thresh) != np.average(zero_thresh)


def test_sharpen_grayscale(test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    zero_thresh = sharpen(gray_img, (5, 5), amount=1, threshold=0)
    thresh = sharpen(gray_img, (5, 5), amount=1, threshold=100)
    assert np.average(thresh) != np.average(zero_thresh)


def test_sharpen_roi(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    roi_con = [np.array([[[10, 20]], [[10, 200]], [[200, 200]], [[200, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    sharp_img = sharpen(img, (5, 5), amount=1, threshold=0, roi=roi)
    assert np.average(img) != np.average(sharp_img)


def test_sharpen_grayscale_roi(test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    roi_con = [np.array([[[10, 20]], [[10, 200]], [[200, 200]], [[200, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    sharp_img = sharpen(gray_img, (5, 5), amount=1, threshold=0, roi=roi)
    assert np.average(gray_img) != np.average(sharp_img)
