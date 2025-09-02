"""quick_filter tests module."""
import cv2
import numpy as np
from plantcv.plantcv import Objects
from plantcv.plantcv.roi.quick_filter import quick_filter, _quick_cutto


def test_quick_filter(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    cv2.drawContours(mask, cnt, -1, (255), -1, lineType=8, hierarchy=cnt_str)
    roi = [np.array([[[150, 150]], [[150, 174]], [[249, 174]], [[249, 150]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_obj = Objects(contours=[roi], hierarchy=[roi_str])
    filtered_mask = quick_filter(mask=mask, roi=roi_obj)
    area = cv2.countNonZero(filtered_mask)
    # Assert that the contours were filtered as expected
    assert area == 221


def test_quick_cutto(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    cv2.drawContours(mask, cnt, -1, (255), -1, lineType=8, hierarchy=cnt_str)
    roi = [np.array([[[200, 200]], [[200, 190]], [[249, 190]], [[249, 200]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_obj = Objects(contours=[roi], hierarchy=[roi_str])
    filtered_mask, _, _ = _quick_cutto(mask=mask, roi=roi_obj)
    area = cv2.countNonZero(filtered_mask)
    # Assert that the contours were filtered as expected
    assert area == 7
