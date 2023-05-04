import cv2
from plantcv.plantcv import get_centroids


def test_get_centroids(test_data):
    # Read in test data
    mask = cv2.imread(test_data.discs_mask, -1)

    coor = get_centroids(bin_img=mask)

    assert len(coor) == 5
