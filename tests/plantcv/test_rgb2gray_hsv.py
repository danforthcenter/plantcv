import pytest
from plantcv.plantcv import rgb2gray_hsv


def test_rgb2gray_hsv(synthetic_rgb):
    """Test for PlantCV."""
    gray_img = rgb2gray_hsv(rgb_img=synthetic_rgb, channel="s")
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert synthetic_rgb.shape[:2] == gray_img.shape


def test_rgb2gray_hsv_bad_input(synthetic_rgb):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = rgb2gray_hsv(rgb_img=synthetic_rgb, channel="l")
