import cv2
import numpy as np
from plantcv.plantcv.filters import solidity


def test_filters_solidity(filters_test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(filters_test_data.small_bin, -1)

    filtered_mask = solidity(bin_img=mask, thresh=0.9)

    assert np.sum(mask) > np.sum(filtered_mask)
