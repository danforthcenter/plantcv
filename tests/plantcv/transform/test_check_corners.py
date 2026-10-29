import pytest
from plantcv.plantcv.transform.detect_color_card import _check_corners


def test_check_corners(synthetic_gray):
    """Test for PlantCV."""
    img = synthetic_gray
    corners = [[10, 10], [100000, 10], [20, 20], [10,20]]
    with pytest.raises(RuntimeError):
        _check_corners(img, corners)
