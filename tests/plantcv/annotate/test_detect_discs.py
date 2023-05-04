import cv2
from plantcv.plantcv.annotate import detect_discs


def test_detect_discs(test_data):
    # Read in test data
    mask = cv2.imread(test_data.discs_mask, -1)

    _, coor = detect_discs(bin_img=mask, ecc_thresh=0.3)

    assert len(coor) == 3
