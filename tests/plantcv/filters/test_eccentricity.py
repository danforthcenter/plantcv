import cv2
import numpy as np
from plantcv.plantcv.filters import eccentricity


def test_filters_eccentricity(filters_test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(filters_test_data.small_bin_fill, -1)

    filtered_mask = eccentricity(bin_img=mask, ecc_thresh=0.5)

    assert np.sum(mask) > np.sum(filtered_mask)
