import cv2
from plantcv.plantcv import scharr_filter


def test_scharr_filter(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    scharr_img = scharr_filter(img=img, dx=1, dy=0, scale=1)
    # Assert that the output image has the dimensions of the input image
    assert img.shape == scharr_img.shape
