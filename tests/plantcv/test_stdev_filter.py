import cv2
from plantcv.plantcv import stdev_filter


def test_stdev_filter(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    filter_img = stdev_filter(img=img, ksize=11)
    assert img.shape == filter_img.shape
