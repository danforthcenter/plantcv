import pytest
import numpy as np
import cv2
from plantcv.plantcv import apply_mask


def test_apply_mask_white(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    masked_img = apply_mask(img=img, mask=mask, mask_color="white")
    assert np.unique(masked_img[np.where(mask == 0)]) == 255


def test_apply_mask_black(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    masked_img = apply_mask(img=img, mask=mask, mask_color="black")
    assert np.unique(masked_img[np.where(mask == 0)]) == 0


def test_apply_mask_hyperspectral(test_data):
    """Test for PlantCV."""
    # Read in test data
    hsi = test_data.load_hsi(test_data.hsi_file)
    mask = cv2.imread(test_data.hsi_mask_file, -1)
    masked_array = apply_mask(img=hsi.array_data, mask=mask, mask_color="black")
    assert np.unique(masked_array[np.where(mask == 0)]) == 0


def test_apply_mask_bad_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    with pytest.raises(RuntimeError):
        _ = apply_mask(img=img, mask=mask, mask_color="wite")
