import pytest
import cv2
import numpy as np
from plantcv.plantcv import background_subtraction


def test_background_subtraction(test_data):
    """Test for PlantCV."""
    fg_img = cv2.imread(test_data.small_gray_img, -1)
    bg_img = cv2.imread(test_data.small_bin_img, -1)
    fgmask = background_subtraction(background_image=bg_img, foreground_image=fg_img)
    # Assert that the output image has the dimensions of the input image and is binary
    assert fg_img.shape == fgmask.shape and np.array_equal(np.unique(fgmask), np.array([0, 127, 255]))


def test_background_subtraction_bad_img_type(test_data):
    """Test for PlantCV."""
    fg_color = cv2.imread(test_data.small_rgb_img)
    bg_gray = cv2.imread(test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = background_subtraction(background_image=bg_gray, foreground_image=fg_color)


def test_background_subtraction_larger_fg(test_data):
    """Test for PlantCV."""
    fg_img = cv2.imread(test_data.small_gray_img, -1)
    bg_img = cv2.imread(test_data.small_bin_img, -1)
    h, w = fg_img.shape
    fg_img_resized = cv2.resize(fg_img, (int(h / 2), int(w / 2)), interpolation=cv2.INTER_AREA)
    fgmask = background_subtraction(background_image=bg_img, foreground_image=fg_img_resized)
    # Assert that the output image has the dimensions of the input image and is binary
    assert fg_img_resized.shape == fgmask.shape and np.array_equal(np.unique(fgmask), np.array([0, 127, 255]))


def test_background_subtraction_larger_bg(test_data):
    """Test for PlantCV."""
    fg_img = cv2.imread(test_data.small_gray_img, -1)
    bg_img = cv2.imread(test_data.small_bin_img, -1)
    h, w = bg_img.shape
    bg_img_resized = cv2.resize(bg_img, (int(h / 2), int(w / 2)), interpolation=cv2.INTER_AREA)
    fgmask = background_subtraction(background_image=bg_img_resized, foreground_image=fg_img)
    # Assert that the output image has the dimensions of the input image and is binary
    assert bg_img_resized.shape == fgmask.shape and np.array_equal(np.unique(fgmask), np.array([0, 127, 255]))
