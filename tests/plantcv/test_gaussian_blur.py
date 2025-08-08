import cv2
import numpy as np
from plantcv.plantcv import gaussian_blur, Objects


def test_gaussian_blur(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    gaussian_img = gaussian_blur(img=img, ksize=(51, 51), sigma_x=0, sigma_y=None)
    assert np.average(img) != np.average(gaussian_img)


def test_gaussian_blur_roi(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    gaussian_img = gaussian_blur(img=img, ksize=(5, 5), sigma_x=0, sigma_y=None, roi=roi)
    assert np.average(img) == np.average(gaussian_img)


def test_gaussian_blur_grayscale(test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    gaussian_img = gaussian_blur(img=gray_img, ksize=(51, 51), sigma_x=0, sigma_y=None)
    assert np.average(gray_img) != np.average(gaussian_img)


def test_gaussian_blur_grayscale_roi(test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    gaussian_img = gaussian_blur(img=gray_img, ksize=(5, 5), sigma_x=0, sigma_y=None, roi=roi)
    assert np.average(gray_img) == np.average(gaussian_img)
