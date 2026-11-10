import pytest
import numpy as np
from plantcv.plantcv import dilate, Objects


def test_dilate(synthetic_mask):
    """Test for PlantCV."""
    img = synthetic_mask
    dilate_img = dilate(gray_img=img, ksize=5, i=1)
    # Assert that the output image has the dimensions of the input image and is binary
    assert img.shape == dilate_img.shape and np.array_equal(np.unique(dilate_img), np.array([0, 255]))


def test_dilate_roi(synthetic_mask):
    """Test for PlantCV."""
    img = synthetic_mask
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    dilate_img = dilate(gray_img=img, ksize=5, i=1, roi=roi)
    # Assert that the output image has the dimensions of the input image and is binary
    assert img.shape == dilate_img.shape and np.array_equal(np.unique(dilate_img), np.array([0, 255]))


def test_dilate_small_k(synthetic_mask):
    """Test for PlantCV."""
    img = synthetic_mask
    with pytest.raises(ValueError):
        _ = dilate(gray_img=img, ksize=1, i=1)
