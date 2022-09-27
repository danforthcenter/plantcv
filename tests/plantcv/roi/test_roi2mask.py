import cv2
import numpy as np
from plantcv.plantcv.roi import roi2mask
from plantcv.plantcv import Objects


def test_roi2mask(roi_test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(roi_test_data.small_rgb_img)
    roi_cnt, roi_h = roi_test_data.load_contours(roi_test_data.small_contours_file)
    roi = Objects(contours=[roi_cnt], hierarchy=[roi_h])
    mask = roi2mask(img=img, roi=roi)
    assert np.shape(mask)[0:2] == np.shape(img)[0:2] and np.array_equal(np.unique(mask), np.array([0, 255]))
