"""Tests for pcv.visualize.histogram."""
import pytest
import numpy as np
from altair.vegalite.v5.api import Chart
from pandas.core.frame import DataFrame
from plantcv.plantcv.visualize import histogram


@pytest.mark.parametrize("bins,lb,ub,title", [[200, 0, 255, "Include Title"], [100, None, None, None]])
def test_histogram(bins, lb, ub, title, synthetic_gray, synthetic_mask):
    """Test for PlantCV."""
    img = synthetic_gray
    mask = synthetic_mask
    fig_hist, hist_df = histogram(img=img, mask=mask, bins=bins, lower_bound=lb, upper_bound=ub, title=title, hist_data=True)
    assert all([isinstance(fig_hist, Chart), isinstance(hist_df, DataFrame)])


def test_histogram_no_mask(synthetic_gray):
    """Test for PlantCV."""
    img = synthetic_gray
    fig_hist = histogram(img=img, mask=None)
    assert isinstance(fig_hist, Chart)


def test_histogram_rgb_img(synthetic_rgb):
    """Test for PlantCV."""
    img_rgb = synthetic_rgb
    fig_hist = histogram(img=img_rgb)
    assert isinstance(fig_hist, Chart)


def test_histogram_multispectral_img(synthetic_rgb):
    """Test for PlantCV."""
    # Test multi-spectral image
    img_rgb = synthetic_rgb
    img_multi = np.concatenate((img_rgb, img_rgb), axis=2)
    fig_hist = histogram(img=img_multi)
    assert isinstance(fig_hist, Chart)


def test_histogram_no_img():
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = histogram(img=None)


def test_histogram_array(synthetic_gray):
    """Test for PlantCV."""
    img = synthetic_gray
    with pytest.raises(RuntimeError):
        _ = histogram(img=img[0, :])
