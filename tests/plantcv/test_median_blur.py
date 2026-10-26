import pytest
import numpy as np
from plantcv.plantcv import median_blur, Objects


@pytest.mark.parametrize("kernel", [5, (5, 5)])
def test_median_blur(kernel, synthetic_mask):
    """Test for PlantCV."""
    img = synthetic_mask
    blur_img = median_blur(gray_img=img, ksize=kernel)
    # Assert that the output image has the dimensions of the input image and is binary
    assert img.shape == blur_img.shape and np.array_equal(np.unique(blur_img), np.array([0, 255]))


@pytest.mark.parametrize("kernel", [5, (5, 5)])
def test_median_blur_roi(kernel, synthetic_mask):
    """Test for PlantCV."""
    img = synthetic_mask
    roi_con = [np.array([[[10, 20]], [[10, 39]], [[29, 39]], [[29, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    blur_img = median_blur(gray_img=img, ksize=kernel, roi=roi)
    # Assert that the output image has the dimensions of the input image and is binary
    assert img.shape == blur_img.shape and np.array_equal(np.unique(blur_img), np.array([0, 255]))


def test_median_blur_bad_input(synthetic_gray):
    """Test for PlantCV."""
    img = synthetic_gray
    with pytest.raises(RuntimeError):
        _ = median_blur(gray_img=img, ksize=5.)
