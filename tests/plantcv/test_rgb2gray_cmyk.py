import pytest
from plantcv.plantcv import rgb2gray_cmyk


def test_rgb2gray_cmyk(synthetic_rgb):
    """Test for PlantCV."""
    gray_img = rgb2gray_cmyk(rgb_img=synthetic_rgb, channel="c")
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert synthetic_rgb.shape[:2] == gray_img.shape


def test_rgb2gray_cmyk_bad_channel(synthetic_rgb):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        # Channel S is not in CMYK
        _ = rgb2gray_cmyk(rgb_img=synthetic_rgb, channel="s")
