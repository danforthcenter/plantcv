import cv2
from plantcv.plantcv.annotate import get_centroids


def test_get_centroids(annotate_test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(annotate_test_data.discs_mask, -1)

    coor = get_centroids(bin_img=mask)

    assert len(coor) == 5
