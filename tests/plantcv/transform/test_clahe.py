import numpy as np
from plantcv.plantcv.transform.clahe import clahe


def test_rgb_clahe(synthetic_rgb):
    """Test for PlantCV"""
    img = synthetic_rgb
    corrected_img = clahe(img)
    assert np.shape(corrected_img) == np.shape(img) and np.sum(corrected_img) != np.sum(img)


def test_gray_clahe(synthetic_gray):
    """Test for PlantCV"""
    img = synthetic_gray
    corrected_img = clahe(img)
    assert np.shape(corrected_img) == np.shape(img) and np.sum(corrected_img) != np.sum(img)
