"""Tests for filters.color_card."""
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv.transform.detect_color_card import mask_color_card


def test_mask_color_card(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    params.debug = "plot"
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    cc_mask = mask_color_card(rgb_img=rgb_img)
    assert np.array_equal(np.unique(cc_mask), np.array([0, 255]))


def test_mask_astro_color_card(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    params.debug = "plot"
    rgb_img = cv2.imread(transform_test_data.astrocard_img)
    cc_mask = mask_color_card(rgb_img=rgb_img, card_type="astro")
    assert np.array_equal(np.unique(cc_mask), np.array([0, 255]))
