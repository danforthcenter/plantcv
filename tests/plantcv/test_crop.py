"""Tests for pcv.crop."""""
import cv2
import numpy as np
from plantcv.plantcv import crop
from plantcv.plantcv import readimage
from tests import synthetic


def test_plantcv_crop(synthetic_gray):
    """Test for PlantCV."""
    cropped = crop(img=synthetic_gray, x=10, y=10, h=50, w=50)
    assert np.shape(cropped) == (50, 50)


def test_plantcv_crop_multiarray():
    """Test for PlantCV."""
    # Read in test data
    img = np.ones((100, 100))
    img_stacked = cv2.merge((img, img, img, img))
    cropped = crop(img=img_stacked, x=10, y=10, h=50, w=50)
    assert np.shape(cropped) == (50, 50, 4)


def test_plantcv_crop_hyperspectral(tmpdir):
    """Test for PlantCV."""
    # Wavelengths that span the blue, green and red pseudo-rgb targets
    filename = synthetic.write_envi(outdir=tmpdir, filename="crop", wavelengths=[450, 500, 550, 600, 650])
    hyperimg = readimage(filename, mode='envi')
    cropped = crop(img=hyperimg, x=1, y=0, h=2, w=2)
    assert np.array_equal(cropped.array_data, synthetic.envi_array()[0:2, 1:3, :])
