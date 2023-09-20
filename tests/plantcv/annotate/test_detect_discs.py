import cv2
from plantcv.plantcv.annotate import detect_discs


def test_detect_discs(annotate_test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(annotate_test_data.discs_mask, -1)

    _, coor = detect_discs(bin_img=mask, ecc_thresh=0.3)

    assert len(coor) == 3
