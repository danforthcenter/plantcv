import cv2
import numpy as np
from plantcv.plantcv import sharpen


def test_sharpen_zero_amount(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    sharp_img = sharpen(img, (5, 5), amount = 0, threshold = 0)
    assert np.average(img) == np.average(sharp_img)

def test_sharpen_any_amount(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    sharp_img = sharpen(img, (5, 5), amount = 1, threshold = 0)
    assert np.average(img) != np.average(sharp_img)

def test_sharpen_threshold(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    zero_thresh = sharpen(img, (5, 5), amount = 1, threshold = 0)
    thresh = sharpen(img, (5, 5), amount = 1, threshold = 100)
    assert np.average(thresh) != np.average(zero_thresh)
