import cv2
import numpy as np
from plantcv.plantcv.roi import roi2mask


def test_roi2mask(roi_test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(roi_test_data.small_rgb_img)
    cnt, _ = roi_test_data.load_contours(roi_test_data.small_contours_file)
    mask = roi2mask(img=img, contour=cnt)
    assert np.shape(mask)[0:2] == np.shape(img)[0:2] and np.array_equal(np.unique(mask), np.array([0, 255]))
