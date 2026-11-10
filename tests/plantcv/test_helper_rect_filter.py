import numpy as np
from plantcv.plantcv import Objects
from plantcv.plantcv._helpers import _rect_filter


def test_rect_filter(synthetic_rgb):
    """Test for PlantCV."""
    rgb_img = synthetic_rgb
    roi = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_obj = Objects(contours=[roi], hierarchy=[roi_str])
    sub_img = _rect_filter(img=rgb_img, roi = roi_obj)
    assert np.shape(sub_img) != np.shape(rgb_img)
