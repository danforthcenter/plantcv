import pytest
import numpy as np
from plantcv.plantcv import closing, Objects
from tests import synthetic


def gapped_gray():
    """Synthetic grayscale plant with a 1 px background-level gap down stem column 59."""
    gray_img = synthetic.plant_gray()
    gray_img[:, 59] = synthetic.BACKGROUND_GRAY
    return gray_img


def test_closing(synthetic_mask):
    """Test for PlantCV."""
    filtered_img = closing(gray_img=synthetic_mask)
    # Assert that the output image has the dimensions of the input image and is binary
    assert synthetic_mask.shape == filtered_img.shape and np.array_equal(np.unique(filtered_img), np.array([0, 255]))


def test_closing_roi(synthetic_mask):
    """Test for PlantCV."""
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    filtered_img = closing(gray_img=synthetic_mask, roi=roi)
    # Assert that the output image has the dimensions of the input image and is binary
    assert synthetic_mask.shape == filtered_img.shape and np.array_equal(np.unique(filtered_img), np.array([0, 255]))


def test_closing_grayscale():
    """Test for PlantCV."""
    gray_img = gapped_gray()
    filtered_img = closing(gray_img=gray_img, kernel=np.ones((4, 4), np.uint8))
    # Closing fills the 60 px stem gap from 50 back to 200
    assert np.sum(filtered_img) == np.sum(gray_img) + 60 * 150


def test_closing_grayscale_roi():
    """Test for PlantCV."""
    gray_img = gapped_gray()
    # ROI covering the whole 100 x 120 image
    roi_con = [np.array([[[0, 0]], [[0, 100]], [[120, 100]], [[120, 0]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    filtered_img = closing(gray_img=gray_img, kernel=np.ones((4, 4), np.uint8), roi=roi)
    # Closing fills the 60 px stem gap from 50 back to 200
    assert np.sum(filtered_img) == np.sum(gray_img) + 60 * 150


def test_closing_bad_input(synthetic_rgb):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = closing(gray_img=synthetic_rgb)
