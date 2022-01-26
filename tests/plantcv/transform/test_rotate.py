import cv2
import numpy as np
from plantcv.plantcv.transform import rotate


def test_rotate(transform_test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(transform_test_data.small_rgb_img)
    rotated = rotate(img=img, rotation_deg=45, crop=True)
    imgavg = np.average(img)
    rotateavg = np.average(rotated)
    assert rotateavg != imgavg


def test_rotate_gray(transform_test_data):
    """Test for PlantCV."""
    img = cv2.imread(transform_test_data.small_gray_img, -1)
    rotated = rotate(img=img, rotation_deg=45, crop=False)
    imgavg = np.average(img)
    rotateavg = np.average(rotated)
    assert rotateavg != imgavg
