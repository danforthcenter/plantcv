import pytest
import cv2
import numpy as np
from plantcv.plantcv import median_blur


@pytest.mark.parametrize("kernel", [5, (5, 5)])
def test_median_blur(kernel, test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_bin_img, -1)
    blur_img = median_blur(gray_img=img, ksize=kernel)
    # Assert that the output image has the dimensions of the input image and is binary
    assert img.shape == blur_img.shape and np.array_equal(np.unique(blur_img), np.array([0, 255]))


def test_median_blur_bad_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = median_blur(gray_img=img, ksize=5.)
