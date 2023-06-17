import pytest
import cv2
import numpy as np
from plantcv.plantcv import roi_objects
from plantcv.plantcv import Objects


@pytest.mark.parametrize("mode,exp", [["largest", 221], ["cutto", 152], ["partial", 221]])
def test_roi_objects(mode, exp, test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    cnt_Obj = Objects(contours=[cnt], hierarchy=[cnt_str])
    roi = [np.array([[[150, 150]], [[150, 174]], [[249, 174]], [[249, 150]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_Obj = Objects(contours=[roi], hierarchy=[roi_str])
    _, _, area = roi_objects(img=img, roi=roi_Obj, obj=cnt_Obj, roi_type=mode)
    # Assert that the contours were filtered as expected
    assert area == exp

def test_roi_objects_multi(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    cnt_Obj = Objects(contours=[cnt], hierarchy=[cnt_str])
    roi = [np.array([[[150, 150]], [[150, 174]], [[249, 174]], [[249, 150]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    # make a multi-ROI by repeating the same roi twice
    roi_Obj = Objects(contours=[roi, roi], hierarchy=[roi_str, roi_str])
    _, _, area = roi_objects(img=img, roi=roi_Obj, obj=cnt_Obj, roi_type="partial")
    # Assert that the contours were filtered as expected
    assert area == 221


def test_roi_objects_bad_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    cnt_Obj = Objects(contours=[cnt], hierarchy=[cnt_str])
    roi = [np.array([[[150, 150]], [[150, 174]], [[249, 174]], [[249, 150]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_Obj = Objects(contours=[roi], hierarchy=[roi_str])
    with pytest.raises(RuntimeError):
        _ = roi_objects(img=img, roi_type="cut", roi=roi_Obj, obj=cnt_Obj)


def test_roi_objects_grayscale_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    cnt_Obj = Objects(contours=[cnt], hierarchy=[cnt_str])
    roi = [np.array([[[150, 150]], [[150, 174]], [[249, 174]], [[249, 150]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_Obj = Objects(contours=[roi], hierarchy=[roi_str])
    _, _, area = roi_objects(img=img, roi_type="partial", roi=roi_Obj, obj=cnt_Obj)
    # Assert that the contours were filtered as expected
    assert area == 221


def test_roi_objects_no_overlap(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    cnt_Obj = Objects(contours=[cnt], hierarchy=[cnt_str])
    roi = [np.array([[[0, 0]], [[0, 24]], [[24, 24]], [[24, 0]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_Obj = Objects(contours=[roi], hierarchy=[roi_str])
    _, _, area = roi_objects(img=img, roi=roi_Obj, obj=cnt_Obj, roi_type="partial")
    # Assert that the contours were filtered as expected
    assert area == 0


def test_roi_objects_nested():
    """Test for PlantCV."""
    # Create test data
    img = np.zeros((100, 100), dtype=np.uint8)
    cnt = [np.array([[[25, 25]], [[25, 49]], [[49, 49]], [[49, 25]]], dtype=np.int32),
           np.array([[[34, 35]], [[35, 34]], [[39, 34]], [[40, 35]], [[40, 39]], [[39, 40]], [[35, 40]], [[34, 39]]],
                    dtype=np.int32)]
    cnt_str = np.array([[[-1, -1,  1, -1], [-1, -1, -1,  0]]], dtype=np.int32)
    cnt_Obj = Objects(contours=[cnt], hierarchy=[cnt_str])
    roi = [np.array([[[0, 0]], [[0, 99]], [[99, 99]], [[99, 0]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_Obj = Objects(contours=[roi], hierarchy=[roi_str])
    _, _, area = roi_objects(img=img, roi=roi_Obj, obj=cnt_Obj, roi_type="largest")
    assert area == 580
