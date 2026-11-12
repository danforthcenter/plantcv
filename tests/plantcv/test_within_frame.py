import pytest
import numpy as np
from plantcv.plantcv import within_frame


@pytest.mark.parametrize('pos,expected', [[0, False], [1, True]])
def test_within_frame(pos, expected):
    """Test for PlantCV."""
    # Create test data
    mask = np.zeros((10, 10), dtype=np.uint8)
    mask[pos:5, pos:5] = 255
    result = within_frame(mask=mask, border_width=1)
    assert result == expected


def test_within_frame_bad_input(synthetic_gray):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = within_frame(synthetic_gray)


@pytest.mark.parametrize('value', [1, 255])
def test_within_frame_binary_values(value):
    """Test for PlantCV."""
    # Create test data
    mask = np.zeros((10, 10), dtype=np.uint8)
    mask[1:5, 1:5] = value
    result = within_frame(mask=mask, border_width=1)
    assert result is True


def test_within_frame_all_background():
    """Test for PlantCV."""
    # Create test data
    mask = np.zeros((10, 10), dtype=np.uint8)
    result = within_frame(mask=mask, border_width=1)
    assert result is True
