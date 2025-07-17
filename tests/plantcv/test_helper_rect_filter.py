import pytest
import cv2
import numpy as np
from plantcv.plantcv._helpers import _rect_filter

def test_rect_filter(test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(test_data.small_gray_img)
    sub_img = _rect_filter(img=rgb_img, xstart = 10, ystart = 10, height = 20, width = 20)
    assert np.shape(sub_img) != np.shape(rgb_img)
