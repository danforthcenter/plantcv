"""Tests for pcv.visualize.hyper_histogram."""
import pytest
import numpy as np
from altair.vegalite.v5.api import Chart
from plantcv.plantcv.visualize import hyper_histogram
from tests import synthetic


# Ultraviolet (below 445 nm), visible and near-infrared wavelengths
@pytest.mark.parametrize("wavelengths", [[], [410, 500, 640, 992, 990]])
def test_hyper_histogram(wavelengths):
    """Test for PlantCV."""
    hsi = synthetic.spectral_data()
    mask = np.zeros(hsi.array_data.shape[:2], dtype=np.uint8)
    mask += 255
    fig_hist = hyper_histogram(hsi=hsi, mask=mask, wvlengths=wavelengths, title="Hyper Histogram Test")
    assert isinstance(fig_hist, Chart)


def test_hyper_histogram_wv_out_range():
    """Test for PlantCV."""
    hsi = synthetic.spectral_data()
    with pytest.raises(RuntimeError):
        _ = hyper_histogram(hsi=hsi, wvlengths=[200,  550])


def test_hyper_histogram_extreme_wvs():
    """Test for PlantCV."""
    hsi = synthetic.spectral_data()
    mask = np.zeros(hsi.array_data.shape[:2], dtype=np.uint8)
    mask += 255
    wv_keys = list(hsi.wavelength_dict.keys())
    wavelengths = [250, 270, 1800, 2500]
    # change first 4 keys
    for (k_, k) in zip(wv_keys[0:5], wavelengths):
        hsi.wavelength_dict[k] = hsi.wavelength_dict.pop(k_)
    hsi.min_wavelength, hsi.max_wavelength = min(hsi.wavelength_dict), max(hsi.wavelength_dict)
    fig_hist = hyper_histogram(hsi=hsi, mask=mask, wvlengths=wavelengths)
    assert isinstance(fig_hist, Chart)


def test_hyper_histogram_no_wvs():
    """Test for PlantCV."""
    hsi = synthetic.spectral_data()
    mask = np.zeros(hsi.array_data.shape[:2], dtype=np.uint8)
    mask += 255
    wavelengths = None
    fig_hist = hyper_histogram(hsi=hsi, mask=mask, wvlengths=wavelengths)
    assert isinstance(fig_hist, Chart)
