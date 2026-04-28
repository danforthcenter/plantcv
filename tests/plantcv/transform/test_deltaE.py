"""Tests for deltaE."""
import cv2
import numpy as np
from plantcv.plantcv._globals import outputs
from plantcv.plantcv.transform.detect_color_card import deltaE


def test_deltaE_macbeth(transform_test_data):
    """Test for PlantCV."""
    outputs.clear()
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    de_matrix = deltaE(rgb_img=rgb_img, color_chip_size="classic")
    assert np.shape(de_matrix) == (6, 4)
    assert outputs.metadata["max_deltaE_calibrated"]["value"] == np.float64(40.10999900620317)


def test_deltaE_astro(transform_test_data):
    """Test for PlantCV."""
    outputs.clear()
    rgb_img = cv2.imread(transform_test_data.astrocard_img)
    de_matrix = deltaE(rgb_img=rgb_img, color_chip_size="astro")
    assert np.shape(de_matrix) == (3, 5)
    assert outputs.metadata["max_deltaE_calibrated"]["value"] == np.float64(78.00042935949308)
