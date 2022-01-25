import cv2
from plantcv.plantcv import rgb2gray


def test_rgb2gray(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    gray_img = rgb2gray(rgb_img=img)
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert img.shape[:2] == gray_img.shape
