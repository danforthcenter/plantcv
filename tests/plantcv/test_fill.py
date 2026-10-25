import pytest
import cv2
import numpy as np
from plantcv.plantcv import fill, Objects
from plantcv.plantcv._globals import params


def test_fill(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_bin_img, -1)
    fill_img = fill(bin_img=img, size=63632)
    # Assert the image is blank
    assert np.sum(fill_img) == 0


def test_fill_bad_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = fill(bin_img=img, size=1)


def test_fill_roi(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_bin_img, -1)
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    fill_img = fill(bin_img=img, size=63632, roi=roi)
    # Assert the image is not blank
    assert np.sum(fill_img) == 56355


def test_fill_rescaled(test_data):
    """Test for PlantCV."""
    prev_px_height = params.px_height
    prev_px_width = params.px_width
    params.px_height = 0.1
    params.px_width = 0.1
    params.unit = "hectares"
    img = np.zeros((100, 100), dtype=np.uint8)
    img[0:10, 0:10] = 1
    img[11:40, 11:40] = 1
    img[50:99, 50:99] = 1
    fill_img = fill(bin_img=img, size=9, scale_size=True)
    params.px_height = prev_px_height
    params.px_width = prev_px_width
    params.unit = "pixels"
    assert np.sum(fill_img / 255) == 2401
