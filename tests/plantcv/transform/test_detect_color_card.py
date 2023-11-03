"""Tests for detect_color_card."""
import cv2
import pytest
import numpy as np
from plantcv.plantcv.transform import detect_color_card


def test_detect_color_card(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    labeled_mask = detect_color_card(rgb_img=rgb_img)
    assert len(np.unique(labeled_mask)) == 25


def test_detect_color_card_none_found(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.target_img)
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img)
