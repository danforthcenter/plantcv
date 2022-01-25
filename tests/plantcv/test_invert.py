import cv2
import numpy as np
from plantcv.plantcv import invert


def test_invert(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_bin_img, -1)
    inverted_img = invert(gray_img=img)
    total_px = img.shape[0] * img.shape[1]
    expected = total_px - np.count_nonzero(img)
    assert np.count_nonzero(inverted_img) == expected
