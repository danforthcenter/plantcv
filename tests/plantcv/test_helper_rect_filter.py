import cv2
import numpy as np
from plantcv.plantcv._helpers import _rect_filter

def test_rect_filter(test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(test_data.small_gray_img)
    roi = rectangle(rgb_img, x = 10, y = 20, h = 20, w = 20)
    sub_img = _rect_filter(img=rgb_img, roi = roi)
    assert np.shape(sub_img) != np.shape(rgb_img)
