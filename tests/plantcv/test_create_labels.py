import numpy as np
import cv2
from plantcv.plantcv import create_labels, Objects


def test_create_labels(test_data):
    """Test for PlantCV."""
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    mask = cv2.imread(test_data.small_bin_img, -1)
    cnt_Obj = Objects(contours=[cnt], hierarchy=[cnt_str])
    masks, num = create_labels(mask=mask, rois=cnt_Obj, roi_type="partial")
    assert np.unique(masks).size == (num + 1)


def test_create_labels_no_roi(test_data):
    """Test for PlantCV."""
    # cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    mask = cv2.imread(test_data.small_bin_img, -1)
    masks, num = create_labels(mask=mask)
    assert num == 1
