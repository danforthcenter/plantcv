import cv2
import numpy as np
from plantcv.plantcv.submask import sub_mask

def test_sub_mask_success(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    spots = sub_mask(img, mask, 2, 2)
    assert len(np.unique(spots)) == 3


def test_sub_mask_too_large(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    spots = sub_mask(img, mask, 2, 20)
    assert len(np.unique(spots)) == 1


def test_sub_mask_too_many(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    spots = sub_mask(img, mask, 5, 3)
    assert len(np.unique(spots)) == 2
