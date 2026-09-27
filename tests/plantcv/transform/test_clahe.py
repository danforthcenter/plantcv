import cv2
import numpy as np
from plantcv.plantcv.transform.clahe import clahe


def test_rgb_clahe(test_data):
    """Test for PlantCV"""
    img = cv2.imread(test_data.small_rgb_img)
    corrected_img = clahe(img)
    assert np.shape(corrected_img) == np.shape(img) and np.sum(corrected_img) != np.sum(img)


def test_gray_clahe(test_data):
    """Test for PlantCV"""
    img = cv2.imread(test_data.small_gray_img, -1)
    corrected_img = clahe(img)
    assert np.shape(corrected_img) == np.shape(img) and np.sum(corrected_img) != np.sum(img)
