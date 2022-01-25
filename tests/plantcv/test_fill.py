import pytest
import cv2
import numpy as np
from plantcv.plantcv import fill


def test_fill(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_bin_img, -1)
    fill_img = fill(bin_img=img, size=63632)
    # Assert the image is blank
    assert np.sum(fill_img) == 0


def test_fill_bad_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = fill(bin_img=img, size=1)
