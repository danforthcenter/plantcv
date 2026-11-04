"""Tests for deltaE."""
import os
import pytest
import numpy as np
from plantcv.plantcv._globals import outputs, params
from plantcv.plantcv.transform.detect_color_card import deltaE
from tests import synthetic


@pytest.fixture(scope="module", autouse=True)
def clear_function_args():
    """Always clear function arguments after calling deltaE"""
    params.function_args = {}


def test_deltaE_macbeth():
    """Test for PlantCV."""
    outputs.clear()
    params.function_args = {}
    rgb_img = synthetic.color_cast(synthetic.color_card())
    de_matrix = deltaE(rgb_img=rgb_img, obs="testname", color_chip_size="classic")
    assert np.shape(de_matrix) == (6, 4)
    # recorded value
    assert np.max(outputs.metadata["deltaE_testname"]["value"]) == [pytest.approx(np.float64(16.712), 0.001)]


def test_deltaE_astro():
    """Test for PlantCV."""
    outputs.clear()
    rgb_img = synthetic.color_cast(synthetic.astro_card())
    de_matrix = deltaE(rgb_img=rgb_img, color_chip_size="astro")
    assert np.shape(de_matrix) == (3, 5)
    # recorded value
    assert np.max(outputs.metadata["deltaE_calibrated"]["value"]) == [pytest.approx(np.float64(16.277), 0.001)]


def test_deltaE_bad_param(monkeypatch):
    """Test for PlantCV."""
    monkeypatch.setattr(params, "deltaE", "bad_input")
    rgb_img = synthetic.astro_card()
    with pytest.raises(RuntimeError):
        _ = deltaE(rgb_img=rgb_img, color_chip_size="astro")


@pytest.mark.parametrize("debug", ["print", "plot", None])
def test_deltaE_plotting(debug, tmpdir):
    """Test for PlantCV."""
    cache = tmpdir.mkdir("cache")
    debug_outdir = params.debug_outdir
    default_debug = params.debug
    params.debug_outdir = os.path.join(cache)
    params.debug = debug
    rgb_img = synthetic.color_card()
    de_matrix = deltaE(rgb_img=rgb_img, color_chip_size="classic")
    params.debug_outdir = debug_outdir
    params.debug = default_debug
    assert np.shape(de_matrix) == (6, 4)
