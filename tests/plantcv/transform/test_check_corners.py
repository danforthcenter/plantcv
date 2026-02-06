import cv2
import pytest
from plantcv.plantcv.transform.detect_color_card import _check_corners


def test_check_corners(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_gray_img, -1)
    corners = [[10, 10], [100000, 10], [20, 20], [10,20]]
    with pytest.raises(RuntimeError):
        _check_corners(img, corners)
