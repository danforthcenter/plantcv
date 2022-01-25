import pytest
import cv2
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


def test_within_frame_bad_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = within_frame(gray_img)
