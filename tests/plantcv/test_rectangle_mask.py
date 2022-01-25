import pytest
import cv2
import numpy as np
from plantcv.plantcv import rectangle_mask


@pytest.mark.parametrize("color,expected", [["white", 255], ["gray", 192], ["black", 0]])
def test_rectangle_mask(color, expected, test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    masked, _, _, _ = rectangle_mask(img=img, p1=(0, 0), p2=(10, 10), color=color)
    assert np.unique(masked[0:11, 0:11, :]) == expected


def test_rectangle_mask_grayscale(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    masked, _, _, _ = rectangle_mask(img=img, p1=(0, 0), p2=(10, 10), color="black")
    assert np.unique(masked[0:11, 0:11]) == 0


def test_rectangle_mask_bad_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = rectangle_mask(img=img, p1=(0, 0), p2=(2454, 2056), color="whit")
