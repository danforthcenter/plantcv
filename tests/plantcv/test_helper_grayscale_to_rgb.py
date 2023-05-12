import cv2
from plantcv.plantcv._helpers import _grayscale_to_rgb


def test_grayscale_to_rgb(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_gray_img, -1)
    img = _grayscale_to_rgb(img=img)
    assert len(img.shape) == 3
