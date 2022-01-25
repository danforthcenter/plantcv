import pytest
import cv2
import numpy as np
from plantcv.plantcv.transform import rescale


def test_rescale(transform_test_data):
    """Test for PlantCV."""
    gray_img = cv2.imread(transform_test_data.small_gray_img, -1)
    rescaled_img = rescale(gray_img=gray_img, min_value=0, max_value=100)
    assert max(np.unique(rescaled_img)) == 100


def test_rescale_bad_input(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.small_rgb_img)
    with pytest.raises(RuntimeError):
        _ = rescale(gray_img=rgb_img)
