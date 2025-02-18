"""Tests for auto_correct_color."""
import cv2
import numpy as np
from plantcv.plantcv.transform import auto_correct_color


def test_auto_correct_color(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    corrected_img = auto_correct_color(rgb_img=rgb_img)
    assert np.shape(corrected_img) == np.shape(rgb_img) and np.sum(corrected_img) != np.sum(rgb_img)
