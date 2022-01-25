import cv2
from plantcv.plantcv import laplace_filter


def test_laplace_filter(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    lp_img = laplace_filter(gray_img=img, ksize=1, scale=1)
    # Assert that the output image has the dimensions of the input image
    assert img.shape == lp_img.shape
