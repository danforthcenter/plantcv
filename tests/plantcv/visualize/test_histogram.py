"""Tests for pcv.visualize.histogram."""
import pytest
import cv2
import numpy as np
from altair.vegalite.v5.api import Chart
from pandas.core.frame import DataFrame
from plantcv.plantcv.visualize import histogram


@pytest.mark.parametrize("bins,lb,ub,title", [[200, 0, 255, "Include Title"], [100, None, None, None]])
def test_histogram(bins, lb, ub, title, visualize_test_data):
    """Test for PlantCV."""
    # Read test data
    img = cv2.imread(visualize_test_data.small_gray_img, -1)
    mask = cv2.imread(visualize_test_data.small_bin_img, -1)
    fig_hist, hist_df = histogram(img=img, mask=mask, bins=bins, lower_bound=lb, upper_bound=ub, title=title, hist_data=True)
    assert all([isinstance(fig_hist, Chart), isinstance(hist_df, DataFrame)])


def test_histogram_no_mask(visualize_test_data):
    """Test for PlantCV."""
    # Read test data
    img = cv2.imread(visualize_test_data.small_gray_img, -1)
    fig_hist = histogram(img=img, mask=None)
    assert isinstance(fig_hist, Chart)


def test_histogram_rgb_img(visualize_test_data):
    """Test for PlantCV."""
    # Test RGB input image
    img_rgb = cv2.imread(visualize_test_data.small_rgb_img)
    fig_hist = histogram(img=img_rgb)
    assert isinstance(fig_hist, Chart)


def test_histogram_multispectral_img(visualize_test_data):
    """Test for PlantCV."""
    # Test multi-spectral image
    img_rgb = cv2.imread(visualize_test_data.small_rgb_img)
    img_multi = np.concatenate((img_rgb, img_rgb), axis=2)
    fig_hist = histogram(img=img_multi)
    assert isinstance(fig_hist, Chart)


def test_histogram_no_img():
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = histogram(img=None)


def test_histogram_array(visualize_test_data):
    """Test for PlantCV."""
    # Read test data
    img = cv2.imread(visualize_test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = histogram(img=img[0, :])
