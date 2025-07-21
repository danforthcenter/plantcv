import cv2
import numpy as np
from plantcv.plantcv import Objects
from plantcv.plantcv._helpers import _rect_filter, _rect_replace

def test_rect_replace(test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(test_data.small_gray_img)
    roi = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_obj = Objects(contours=[roi], hierarchy=[roi_str])
    sub_img = _rect_filter(img=rgb_img, roi = roi_obj)
    new_img = _rect_replace(rgb_img, sub_img, roi = roi_obj)
    assert np.shape(new_img) == np.shape(rgb_img)

def test_rect_replace_no_change(test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(test_data.small_gray_img)
    roi = None
    sub_img = _rect_filter(img=rgb_img, roi = roi)
    new_img = _rect_replace(rgb_img, sub_img, roi = roi)
    assert np.shape(new_img) == np.shape(rgb_img)
