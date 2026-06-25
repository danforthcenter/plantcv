"""fast_filter tests module."""
import cv2
import pytest
import numpy as np
from plantcv.plantcv import Objects
from plantcv.plantcv.roi.fast_filter import fast_filter
from plantcv.plantcv import roi as pcv_roi


@pytest.mark.parametrize("mode,exp", [["largest", 221], ["cutto", 152], ["partial", 221], ["within", 0]])
def test_fast_filter(mode, exp, test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    cv2.drawContours(mask, cnt, -1, (255), -1, lineType=8, hierarchy=cnt_str)
    roi = [np.array([[[150, 150]], [[150, 174]], [[249, 174]], [[249, 150]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_obj = Objects(contours=[roi], hierarchy=[roi_str])
    filtered_mask = fast_filter(mask=mask, roi=roi_obj, roi_type=mode)
    area = cv2.countNonZero(filtered_mask)
    assert area == exp


def test_fast_filter_namespace():
    """Test that fast_filter is available in the PlantCV ROI namespace."""
    assert pcv_roi.fast_filter == fast_filter


def test_fast_filter_within(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    cv2.drawContours(mask, cnt, -1, (255), -1, lineType=8, hierarchy=cnt_str)
    roi = [np.array([[[100, 100]], [[100, 224]], [[249, 224]], [[249, 100]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_obj = Objects(contours=[roi], hierarchy=[roi_str])
    filtered_mask = fast_filter(mask=mask, roi=roi_obj, roi_type="within")
    area = cv2.countNonZero(filtered_mask)
    assert area == 221


def test_fast_filter_multi(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    cv2.drawContours(mask, cnt, -1, (255), -1, lineType=8, hierarchy=cnt_str)
    roi = [np.array([[[150, 150]], [[150, 174]], [[249, 174]], [[249, 150]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_obj = Objects(contours=[roi, roi], hierarchy=[roi_str, roi_str])
    filtered_mask = fast_filter(mask=mask, roi=roi_obj, roi_type="partial")
    area = cv2.countNonZero(filtered_mask)
    assert area == 221


def test_fast_filter_bad_input(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    cv2.drawContours(mask, cnt, -1, (255), -1, lineType=8, hierarchy=cnt_str)
    roi = [np.array([[[150, 150]], [[150, 174]], [[249, 174]], [[249, 150]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_obj = Objects(contours=[roi], hierarchy=[roi_str])
    with pytest.raises(RuntimeError):
        _ = fast_filter(mask=mask, roi=roi_obj, roi_type="cut")


def test_fast_filter_no_overlap(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    cv2.drawContours(mask, cnt, -1, (255), -1, lineType=8, hierarchy=cnt_str)
    roi = [np.array([[[0, 0]], [[0, 24]], [[24, 24]], [[24, 0]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_obj = Objects(contours=[roi], hierarchy=[roi_str])
    filtered_mask = fast_filter(mask=mask, roi=roi_obj, roi_type="partial")
    area = cv2.countNonZero(filtered_mask)
    assert area == 0


def test_fast_filter_nested():
    """Test for PlantCV."""
    img = np.zeros((100, 100), dtype=np.uint8)
    mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
    cnt = [np.array([[[25, 25]], [[25, 49]], [[49, 49]], [[49, 25]]], dtype=np.int32),
           np.array([[[34, 35]], [[35, 34]], [[39, 34]], [[40, 35]], [[40, 39]], [[39, 40]], [[35, 40]], [[34, 39]]],
                    dtype=np.int32)]
    cnt_str = np.array([[[-1, -1, 1, -1], [-1, -1, -1, 0]]], dtype=np.int32)
    cv2.drawContours(mask, cnt, -1, (255), -1, lineType=8, hierarchy=cnt_str)
    area_pre = cv2.countNonZero(mask)
    mask = cv2.rectangle(mask, (5, 5), (7, 7), 255, -1)
    area_total = cv2.countNonZero(mask)

    roi = [np.array([[[0, 0]], [[0, 99]], [[99, 99]], [[99, 0]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_obj = Objects(contours=[roi], hierarchy=[roi_str])
    filtered_mask = fast_filter(mask=mask, roi=roi_obj, roi_type="largest")
    filtered_area = cv2.countNonZero(filtered_mask)
    assert area_pre == filtered_area
    assert area_total > filtered_area
