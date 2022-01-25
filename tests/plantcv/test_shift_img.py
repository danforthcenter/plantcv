import pytest
import cv2
from plantcv.plantcv import shift_img


@pytest.mark.parametrize("side", ["top", "bottom", "left", "right"])
def test_shift_img(side, test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    shifted = shift_img(img=img, number=300, side=side)
    assert img.shape == shifted.shape


def test_shift_img_grayscale(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    shifted = shift_img(img=img, number=300, side="top")
    assert img.shape == shifted.shape


def test_shift_img_bad_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img)
    with pytest.raises(RuntimeError):
        _ = shift_img(img=img, number=-300, side="top")


def test_shift_img_bad_side_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img)
    with pytest.raises(RuntimeError):
        _ = shift_img(img=img, number=300, side="starboard")
