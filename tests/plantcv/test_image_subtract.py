import pytest
import cv2
import numpy as np
from plantcv.plantcv import image_subtract


def test_image_subtract(test_data):
    """Test for PlantCV."""
    # read in images
    img1 = cv2.imread(test_data.small_bin_img, -1)
    img2 = np.copy(img1)
    new_img = image_subtract(img1, img2)
    assert np.count_nonzero(new_img) == 0


def test_image_subtract_fail(test_data):
    """Test for PlantCV."""
    # read in images
    img1 = cv2.imread(test_data.small_bin_img, -1)
    img2 = cv2.imread(test_data.small_rgb_img)
    # test
    with pytest.raises(RuntimeError):
        _ = image_subtract(gray_img1=img1, gray_img2=img2)
