import cv2
import numpy as np
from plantcv.plantcv.filters import obj_area


def test_filters_obj_area(filters_test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(filters_test_data.small_bin_fill, -1)

    filtered_mask = obj_area(bin_img=mask, upper_thresh=2000, lower_thresh=1400)

    assert np.sum(mask) > np.sum(filtered_mask)
