import pytest
import cv2
import numpy as np
from plantcv.plantcv import within_frame


@pytest.mark.parametrize('pos,expected', [[0, False], [1, True]])
def test_within_frame(pos, expected):
    # Create test data
    mask = np.zeros((10, 10), dtype=np.uint8)
    mask[pos:5, pos:5] = 255
    # mask_ib = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
    # mask_oob = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK_OOB), -1)
    # in_bounds_ib = pcv.within_frame(mask=mask_ib, border_width=1, label="prefix")
    # in_bounds_oob = pcv.within_frame(mask=mask_oob, border_width=1)
    result = within_frame(mask=mask, border_width=1)
    assert result == expected


def test_within_frame_bad_input(test_data):
    # Read in test data
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = within_frame(gray_img)
