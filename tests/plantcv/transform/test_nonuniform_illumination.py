import numpy as np
from plantcv.plantcv.transform import nonuniform_illumination


def test_nonuniform_illumination_rgb(synthetic_rgb):
    """Test for PlantCV."""
    rgb_img = synthetic_rgb
    corrected = nonuniform_illumination(img=rgb_img, ksize=11)
    assert np.mean(corrected) < np.mean(rgb_img)


def test_nonuniform_illumination_gray(synthetic_gray):
    """Test for PlantCV."""
    gray_img = synthetic_gray
    corrected = nonuniform_illumination(img=gray_img, ksize=11)
    assert corrected.shape == gray_img.shape
