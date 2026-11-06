"""Test pcv.transform.mcc_detect"""
import pytest
import numpy as np
from plantcv.plantcv._globals import params
from plantcv.plantcv.transform.mcc_detect import mcc_detect
from plantcv.plantcv.transform.standard_matrices import std_color_matrix
from tests import synthetic


def test_mcc_detect():
    """Test for PlantCV."""
    rgb_img = synthetic.color_card()
    color_matrix = mcc_detect(rgb_img=rgb_img, color_chip_size="classic")
    assert np.allclose(color_matrix, std_color_matrix(pos=3), rtol=0, atol=1e-12)
    assert "mcc_detect" in params.function_args


def test_mcc_detect_no_color_card():
    """Test for PlantCV."""
    rgb_img = synthetic.random_image((200, 200, 3))
    with pytest.raises(RuntimeError):
        _ = mcc_detect(rgb_img=rgb_img, color_chip_size="classic")
