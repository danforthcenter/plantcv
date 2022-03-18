import pytest
import cv2
import numpy as np
from plantcv.plantcv import hist_equalization


def test_hist_equalization(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    hist = hist_equalization(gray_img=img)
    assert np.average(hist) != np.average(img)


def test_hist_equalization_bad_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    with pytest.raises(RuntimeError):
        _ = hist_equalization(gray_img=img)
