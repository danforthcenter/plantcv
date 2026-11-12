import numpy as np
from plantcv.plantcv import gaussian_blur, Objects


def test_gaussian_blur(synthetic_rgb):
    """Test for PlantCV."""
    img = synthetic_rgb
    gaussian_img = gaussian_blur(img=img, ksize=(51, 51), sigma_x=0, sigma_y=None)
    assert np.average(img) != np.average(gaussian_img)


def test_gaussian_blur_roi(synthetic_rgb):
    """Test for PlantCV."""
    img = synthetic_rgb
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    gaussian_img = gaussian_blur(img=img, ksize=(5, 5), sigma_x=0, sigma_y=None, roi=roi)
    assert np.average(img) == np.average(gaussian_img)


def test_gaussian_blur_grayscale(synthetic_gray):
    """Test for PlantCV."""
    gray_img = synthetic_gray
    gaussian_img = gaussian_blur(img=gray_img, ksize=(51, 51), sigma_x=0, sigma_y=None)
    assert np.average(gray_img) != np.average(gaussian_img)


def test_gaussian_blur_grayscale_roi(synthetic_gray):
    """Test for PlantCV."""
    gray_img = synthetic_gray
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    gaussian_img = gaussian_blur(img=gray_img, ksize=(5, 5), sigma_x=0, sigma_y=None, roi=roi)
    assert np.average(gray_img) == np.average(gaussian_img)
