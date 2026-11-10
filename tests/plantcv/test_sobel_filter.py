import numpy as np
from plantcv.plantcv import sobel_filter, Objects


def test_sobel_filter(synthetic_gray):
    """Test for PlantCV."""
    sobel_img = sobel_filter(gray_img=synthetic_gray, dx=1, dy=0, ksize=1)
    # Assert that the output image has the dimensions of the input image
    assert synthetic_gray.shape == sobel_img.shape


def test_sobel_filter_roi(synthetic_gray):
    """Test for PlantCV."""
    # ROI in the background (rows 20:40, columns 10:30)
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    sobel_img = sobel_filter(gray_img=synthetic_gray, dx=1, dy=0, ksize=1, roi=roi)
    # Assert that the output image has the dimensions of the input image
    assert synthetic_gray.shape == sobel_img.shape
