import numpy as np
from plantcv.plantcv.transform import rotate


def test_rotate(synthetic_rgb):
    """Test for PlantCV."""
    img = synthetic_rgb
    rotated = rotate(img=img, rotation_deg=45, crop=True)
    imgavg = np.average(img)
    rotateavg = np.average(rotated)
    assert rotateavg != imgavg


def test_rotate_gray(synthetic_gray):
    """Test for PlantCV."""
    img = synthetic_gray
    rotated = rotate(img=img, rotation_deg=45, crop=False)
    imgavg = np.average(img)
    rotateavg = np.average(rotated)
    assert rotateavg != imgavg
