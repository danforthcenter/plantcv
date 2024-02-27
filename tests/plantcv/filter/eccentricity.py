import cv2
import pytest
import numpy as np
from plantcv.plantcv.filter import eccentricity

def test_filter_eccentricity(filter_test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(filter_test_data.small_bin_fill, -1)

    filtered_mask = eccentricity(bin_img=mask, ecc_thresh=0.05)

    assert np.sum(mask) == np.sum(filtered_mask)
