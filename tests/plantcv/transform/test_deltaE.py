"""Tests for deltaE."""
import os
import cv2
import pytest
import numpy as np
from plantcv.plantcv._globals import outputs, params
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


@pytest.mark.parametrize("debug", ["print", "plot", None])
def test_deltaE_plotting(debug, transform_test_data, tmpdir):
    """Test for PlantCV."""
    cache = tmpdir.mkdir("cache")
    debug_outdir = params.debug_outdir
    params.debug_outdir = os.path.join(cache)
    params.debug = debug
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    de_matrix = deltaE(rgb_img=rgb_img, color_chip_size="classic")
    params.debug_outdir = debug_outdir
    assert np.shape(de_matrix) == (6, 4)
