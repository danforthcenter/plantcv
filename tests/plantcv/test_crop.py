import cv2
import numpy as np
from plantcv.plantcv import crop


def test_plantcv_crop(test_data):
    """Test for PlantCV."""
    # Read test data
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    cropped = crop(img=gray_img, x=10, y=10, h=50, w=50)
    assert np.shape(cropped) == (50, 50)


def test_plantcv_crop_hyperspectral():
    """Test for PlantCV."""
    # Read in test data
    img = np.ones((100, 100))
    img_stacked = cv2.merge((img, img, img, img))
    cropped = crop(img=img_stacked, x=10, y=10, h=50, w=50)
    assert np.shape(cropped) == (50, 50, 4)
