import pytest
import cv2
import numpy as np
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


@pytest.mark.parametrize("side", ["top", "bottom", "left", "right"])
def test_shift_img_moves_by_number(side, test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    row, col = img.shape[0] // 2, img.shape[1] // 2
    marker = np.zeros_like(img)
    marker[row, col] = 255
    shifted = shift_img(img=marker, number=20, side=side)
    ys, xs = np.nonzero(shifted[:, :, 0])
    expected = {"top": (row + 20, col), "bottom": (row - 20, col),
                "left": (row, col + 20), "right": (row, col - 20)}[side]
    assert len(ys) == 1 and (int(ys[0]), int(xs[0])) == expected


@pytest.mark.parametrize("side", ["top", "bottom", "left", "right"])
def test_shift_img_number_equals_dimension_error(side, test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    number = img.shape[0] if side in ("top", "bottom") else img.shape[1]
    with pytest.raises(RuntimeError):
        _ = shift_img(img=img, number=number, side=side)


def test_shift_img_number_below_dimension(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    # The largest valid shift on each axis still returns the input shape
    assert shift_img(img=img, number=img.shape[0] - 1, side="top").shape == img.shape
    assert shift_img(img=img, number=img.shape[1] - 1, side="right").shape == img.shape


def test_shift_img_non_integer_number(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    with pytest.raises(RuntimeError):
        _ = shift_img(img=img, number=20.5, side="top")
