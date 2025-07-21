import cv2
import numpy as np
import plantcv as pcv
from plantcv.plantcv._helpers import _rect_filter, _rect_replace

def test_rect_replace(test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(test_data.small_gray_img)
    roi = pcv.roi.rectangle(rgb_img, x = 10, y = 20, h = 20, w = 20)
    sub_img = _rect_filter(img=rgb_img, roi = roi)
    new_img = _rect_replace(rgb_img, sub_img, roi = roi)
    assert np.shape(new_img) == np.shape(rgb_img)

def test_rect_replace_no_change(test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(test_data.small_gray_img)
    roi = None
    sub_img = _rect_filter(img=rgb_img, roi = roi)
    new_img = _rect_replace(rgb_img, sub_img, roi = roi)
    assert np.shape(new_img) == np.shape(rgb_img)
