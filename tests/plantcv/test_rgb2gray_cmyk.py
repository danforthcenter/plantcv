import pytest
import cv2
from plantcv.plantcv import rgb2gray_cmyk


def test_rgb2gray_cmyk(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    gray_img = rgb2gray_cmyk(rgb_img=img, channel="c")
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert img.shape[:2] == gray_img.shape


def test_rgb2gray_cmyk_bad_channel(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    with pytest.raises(RuntimeError):
        # Channel S is not in CMYK
        _ = rgb2gray_cmyk(rgb_img=img, channel="s")
