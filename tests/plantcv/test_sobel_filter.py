import cv2
from plantcv.plantcv import sobel_filter


def test_sobel_filter(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    sobel_img = sobel_filter(gray_img=img, dx=1, dy=0, ksize=1)
    # Assert that the output image has the dimensions of the input image
    assert img.shape == sobel_img.shape
