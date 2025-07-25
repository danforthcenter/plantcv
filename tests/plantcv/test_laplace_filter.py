import cv2
import numpy as np
from plantcv.plantcv import laplace_filter, Objects


def test_laplace_filter(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    lp_img = laplace_filter(gray_img=img, ksize=1, scale=1)
    # Assert that the output image has the dimensions of the input image
    assert img.shape == lp_img.shape


def test_laplace_filter_roi(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    lp_img = laplace_filter(gray_img=img, ksize=1, scale=1, roi=roi)
    # Assert that the output image has the dimensions of the input image
    assert img.shape == lp_img.shape
