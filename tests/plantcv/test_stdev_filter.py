import numpy as np
from plantcv.plantcv import stdev_filter, Objects


def test_stdev_filter(synthetic_gray):
    """Test for PlantCV."""
    filter_img = stdev_filter(img=synthetic_gray, ksize=11)
    assert synthetic_gray.shape == filter_img.shape


def test_stdev_filter_roi(synthetic_gray):
    """Test for PlantCV."""
    # ROI in the background (rows 20:40, columns 10:30)
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    filter_img = stdev_filter(img=synthetic_gray, ksize=11, roi=roi)
    assert synthetic_gray.shape == filter_img.shape
