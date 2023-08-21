"""Tests for pcv.crop."""""
import cv2
import numpy as np
from plantcv.plantcv import crop
from plantcv.plantcv import readimage


def test_plantcv_crop(test_data):
    """Test for PlantCV."""
    # Read test data
    gray_img = cv2.imread(test_data.small_gray_img, -1)
    cropped = crop(img=gray_img, x=10, y=10, h=50, w=50)
    assert np.shape(cropped) == (50, 50)


def test_plantcv_crop_multiarray():
    """Test for PlantCV."""
    # Read in test data
    img = np.ones((100, 100))
    img_stacked = cv2.merge((img, img, img, img))
    cropped = crop(img=img_stacked, x=10, y=10, h=50, w=50)
    assert np.shape(cropped) == (50, 50, 4)


def test_plantcv_crop_hyperspectral(test_data):
    """Test for PlantCV."""
    # Read in test data
    hyperimg = readimage(test_data.envi_sample_data, mode='envi')
    cropped = crop(img=hyperimg, x=0, y=0, h=20, w=20)
    assert np.shape(cropped.array_data) == (20, 20, 580)
