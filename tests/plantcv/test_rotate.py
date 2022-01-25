import cv2
import numpy as np
from plantcv.plantcv import rotate


def test_rotate(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    rotated = rotate(img=img, rotation_deg=45, crop=True)
    imgavg = np.average(img)
    rotateavg = np.average(rotated)
    assert rotateavg != imgavg
