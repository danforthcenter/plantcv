import pytest
import cv2
import numpy as np
from plantcv.plantcv import floodfill, Objects


def test_floodfill(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_bin_fill, -1)
    fill_img = floodfill(bin_img=img, points=[(31, 137), (214, 189), (361, 312)], value=0)
    # Assert that the image has been filled in
    assert np.sum(fill_img) == 0


def test_floodfill_roi(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_bin_fill, -1)
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    fill_img = floodfill(bin_img=img, points=[(1, 1), (10, 10), (15, 15)], value=0, roi=roi)
    # Assert that the image has not been filled in
    assert np.sum(fill_img) > 0


def test_floodfill_bad_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = floodfill(bin_img=img, points=(1, 1), value=0)
