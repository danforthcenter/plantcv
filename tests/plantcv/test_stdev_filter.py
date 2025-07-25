import cv2
import numpy as np
from plantcv.plantcv import stdev_filter, Objects


def test_stdev_filter(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    filter_img = stdev_filter(img=img, ksize=11)
    assert img.shape == filter_img.shape


def test_stdev_filter_roi(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    filter_img = stdev_filter(img=img, ksize=11, roi=roi)
    assert img.shape == filter_img.shape
