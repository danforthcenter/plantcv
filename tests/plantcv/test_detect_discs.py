import cv2
import numpy as np 
from plantcv.plantcv import detect_discs


def test_detect_discs(test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(test_data.small_bin_img, -1)

    filtered_mask = detect_discs(bin_img=mask, ecc_thresh=0.3)

    assert  np.sum(mask) < np.sum(filtered_mask) 
