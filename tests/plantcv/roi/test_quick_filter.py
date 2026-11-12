"""quick_filter tests module."""
import cv2
import pytest
import numpy as np
from plantcv.plantcv import Objects
from plantcv.plantcv.roi.quick_filter import quick_filter


@pytest.mark.parametrize("mode,exp", [["partial", 800], ["cutto", 25], ["within", 0], ["largest", 800]])
def test_quick_filter(synthetic_mask, mode, exp):
    """Test for PlantCV."""
    # ROI rows 60:71 and columns 85:100 overlaps the right leaf tip (rows 60:65, columns 85:90, 5 x 5 = 25 px);
    # partial and largest keep the whole 800 px plant, within keeps nothing, and the small object is always removed
    roi = [np.array([[[85, 70]], [[85, 60]], [[99, 60]], [[99, 70]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_obj = Objects(contours=[roi], hierarchy=[roi_str])
    filtered_mask = quick_filter(mask=synthetic_mask, roi=roi_obj, roi_type=mode)
    area = cv2.countNonZero(filtered_mask)
    # Assert that the contours were filtered as expected
    assert area == exp


def test_quick_filter_bad_type(synthetic_mask):
    """Test for PlantCV."""
    roi = [np.array([[[85, 70]], [[85, 60]], [[99, 60]], [[99, 70]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_obj = Objects(contours=[roi], hierarchy=[roi_str])
    with pytest.raises(RuntimeError):
        _ = quick_filter(mask=synthetic_mask, roi=roi_obj, roi_type="bad")


@pytest.mark.parametrize("mode,exp", [["partial", 0], ["cutto", 0], ["within", 0], ["largest", 0]])
def test_quick_filter_empty(mode, exp):
    """Test for PlantCV."""
    # Read in test data
    mask = np.zeros((20, 20), dtype=np.uint8)
    roi = [np.array([[[10, 10]], [[10, 0]], [[15, 0]], [[15, 10]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_obj = Objects(contours=[roi], hierarchy=[roi_str])
    filtered_mask = quick_filter(mask=mask, roi=roi_obj, roi_type=mode)
    area = cv2.countNonZero(filtered_mask)
    # Assert that the contours were filtered as expected
    assert area == exp
