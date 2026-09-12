import pytest
import cv2
import numpy as np
from plantcv.plantcv import within_frame
from plantcv.plantcv.within_frame import _over_two_values


@pytest.mark.parametrize('pos,expected', [[0, False], [1, True]])
def test_within_frame(pos, expected):
    """Test for PlantCV."""
    # Create test data
    mask = np.zeros((10, 10), dtype=np.uint8)
    mask[pos:5, pos:5] = 255
    result = within_frame(mask=mask, border_width=1)
    assert result == expected


def test_within_frame_bad_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = within_frame(gray_img)


@pytest.mark.parametrize('values,expected', [
    [[0, 255], False],          # ordinary binary mask
    [[0], False],               # all background
    [[255], False],             # all foreground
    [[0, 1], False],            # binary, but not 0/255
    [[0, 128, 255], True],      # three values
    [[1, 2, 3, 4], True],       # four values, none of them zero
])
def test_over_two_values(values, expected):
    """The binary check agrees with the np.unique test it replaced."""
    mask = np.array(values * 4, dtype=np.uint8).reshape(2, -1)
    assert _over_two_values(mask) is expected
    # The property the check is really asserting, stated the slow but obvious way
    assert _over_two_values(mask) == (len(np.unique(mask)) > 2)


def test_over_two_values_empty():
    """An empty mask has no values to disagree, as np.unique would also report."""
    mask = np.array([], dtype=np.uint8)
    assert _over_two_values(mask) is False
    assert _over_two_values(mask) == (len(np.unique(mask)) > 2)


def test_within_frame_three_values():
    """A mask with three values is rejected, which is what the check exists for."""
    mask = np.zeros((10, 10), dtype=np.uint8)
    mask[1:5, 1:5] = 255
    mask[6, 6] = 128
    with pytest.raises(RuntimeError):
        _ = within_frame(mask=mask)


def test_within_frame_binary_non_255():
    """A 0/1 mask is still binary and must be accepted."""
    mask = np.zeros((10, 10), dtype=np.uint8)
    mask[1:5, 1:5] = 1
    assert within_frame(mask=mask, border_width=1) is True
