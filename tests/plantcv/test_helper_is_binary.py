import cv2
import numpy as np
import pytest
from plantcv.plantcv._helpers import _is_binary


@pytest.mark.parametrize('values,expected', [
    [[0, 255], True],
    [[0, 1], True],
    [[0], True],
    [[255], True],
    [[0, 128, 255], False],
    [[1, 2, 3, 4], False],
])
def test_is_binary(values, expected):
    """Test for PlantCV."""
    img = np.array(values * 4, dtype=np.uint8).reshape(2, -1)
    assert _is_binary(img=img) is expected


def test_is_binary_zero_size():
    """Test for PlantCV."""
    img = np.array([], dtype=np.uint8)
    assert _is_binary(img=img) is True


def test_is_binary_grayscale(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_gray_img, -1)
    assert _is_binary(img=img) is False


def test_is_binary_bin_img(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_bin_img, -1)
    assert _is_binary(img=img) is True
