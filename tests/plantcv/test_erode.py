import pytest
import numpy as np
from plantcv.plantcv import erode, Objects


def test_erode(synthetic_mask):
    """Test for PlantCV."""
    img = synthetic_mask
    erode_img = erode(gray_img=img, ksize=5, i=1)
    # Assert that the output image has the dimensions of the input image and is binary
    assert img.shape == erode_img.shape and np.array_equal(np.unique(erode_img), np.array([0, 255]))


def test_erode_roi(synthetic_mask):
    """Test for PlantCV."""
    img = synthetic_mask
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    erode_img = erode(gray_img=img, ksize=5, i=1, roi=roi)
    # Assert that the output image has the dimensions of the input image and is binary
    assert img.shape == erode_img.shape and np.array_equal(np.unique(erode_img), np.array([0, 255]))


def test_erode_small_k(synthetic_mask):
    """Test for PlantCV."""
    img = synthetic_mask
    with pytest.raises(ValueError):
        _ = erode(gray_img=img, ksize=1, i=1)
