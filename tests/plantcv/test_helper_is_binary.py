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


def test_is_binary_grayscale(synthetic_gray):
    """Test for PlantCV."""
    img = synthetic_gray
    assert _is_binary(img=img) is False


def test_is_binary_bin_img(synthetic_mask):
    """Test for PlantCV."""
    img = synthetic_mask
    assert _is_binary(img=img) is True


def test_is_binary_raise_error_on_dimensions():
    """Test for PlantCV."""
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    with pytest.raises(RuntimeError):
        _ = _is_binary(img=img, dimCheck=True, raiseError=True)


def test_is_binary_raise_error(synthetic_gray):
    """Test for PlantCV."""
    img = synthetic_gray
    with pytest.raises(RuntimeError):
        _ = _is_binary(img=img, raiseError=True)
