"""Tests for filters.color_card."""
import cv2
import numpy as np
from plantcv.plantcv.filters import color_card


def test_filters_color_card(filters_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(filters_test_data.colorcard_img)
    cc_mask = color_card(rgb_img=rgb_img)
    assert np.sum(cc_mask) == 124040160
