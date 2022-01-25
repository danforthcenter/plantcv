import cv2
import numpy as np
from plantcv.plantcv.transform import nonuniform_illumination


def test_nonuniform_illumination_rgb(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.small_rgb_img)
    corrected = nonuniform_illumination(img=rgb_img, ksize=11)
    assert np.mean(corrected) < np.mean(rgb_img)


def test_nonuniform_illumination_gray(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    gray_img = cv2.imread(transform_test_data.small_gray_img, -1)
    corrected = nonuniform_illumination(img=gray_img, ksize=11)
    assert corrected.shape == gray_img.shape
