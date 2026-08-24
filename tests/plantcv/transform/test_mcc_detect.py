"""Test pcv.transform.mcc_detect"""
import cv2
import pytest
import numpy as np
from plantcv.plantcv._globals import params, outputs
from plantcv.plantcv.transform.mcc_detect import mcc_detect


def test_mcc_detect(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    color_matrix = mcc_detect(rgb_img=rgb_img, color_chip_size="classic")
    assert np.shape(color_matrix) == (24, 4)
    assert "mcc_detect" in params.function_args


def test_mcc_detect_no_color_card(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = np.random.randint(0, 255, (1000, 1000, 3)).astype(np.uint8)
    with pytest.raises(RuntimeError):
        _ = mcc_detect(rgb_img=rgb_img, color_chip_size="classic")
