import pytest
import cv2
import numpy as np
from plantcv.plantcv import background_subtraction
from tests import synthetic


def background_img():
    """Background for the synthetic grayscale plant.

    The background level matches the foreground image everywhere except under the plant, which is
    black, so the output has unchanged (0), shadow (127), and foreground (255) pixels.
    """
    bg_img = np.full(synthetic.PLANT_SHAPE, synthetic.BACKGROUND_GRAY, dtype=np.uint8)
    bg_img[synthetic.plant_mask(small_object=False) > 0] = 0
    return bg_img


def test_background_subtraction(synthetic_gray):
    """Test for PlantCV."""
    fg_img = synthetic_gray
    bg_img = background_img()
    fgmask = background_subtraction(background_image=bg_img, foreground_image=fg_img)
    # Assert that the output image has the dimensions of the input image and is binary
    assert fg_img.shape == fgmask.shape and np.array_equal(np.unique(fgmask), np.array([0, 127, 255]))


def test_background_subtraction_bad_img_type(synthetic_rgb, synthetic_gray):
    """Test for PlantCV."""
    fg_color = synthetic_rgb
    bg_gray = synthetic_gray
    with pytest.raises(RuntimeError):
        _ = background_subtraction(background_image=bg_gray, foreground_image=fg_color)


def test_background_subtraction_larger_fg(synthetic_gray):
    """Test for PlantCV."""
    fg_img = synthetic_gray
    bg_img = background_img()
    h, w = fg_img.shape
    fg_img_resized = cv2.resize(fg_img, (int(h / 2), int(w / 2)), interpolation=cv2.INTER_AREA)
    fgmask = background_subtraction(background_image=bg_img, foreground_image=fg_img_resized)
    # Assert that the output image has the dimensions of the input image and is binary
    assert fg_img_resized.shape == fgmask.shape and np.array_equal(np.unique(fgmask), np.array([0, 127, 255]))


def test_background_subtraction_larger_bg(synthetic_gray):
    """Test for PlantCV."""
    fg_img = synthetic_gray
    bg_img = background_img()
    h, w = bg_img.shape
    bg_img_resized = cv2.resize(bg_img, (int(h / 2), int(w / 2)), interpolation=cv2.INTER_AREA)
    fgmask = background_subtraction(background_image=bg_img_resized, foreground_image=fg_img)
    # Assert that the output image has the dimensions of the input image and is binary
    assert bg_img_resized.shape == fgmask.shape and np.array_equal(np.unique(fgmask), np.array([0, 127, 255]))
