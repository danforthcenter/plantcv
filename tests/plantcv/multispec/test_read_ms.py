"""Test pcv.multispec.read_ms"""
import os
import cv2
import pytest
import numpy as np
from plantcv.plantcv.multispec.read_ms import read_ms
from plantcv.plantcv.classes import MS_data


def test_read_ms_file(tmpdir):
    """Test for PlantCV"""
    cache_dir = tmpdir.mkdir("cache")
    img0 = np.zeros((10, 10), dtype=np.uint8)
    filename0 = os.path.join(cache_dir, "MS450_BP0_img0.png")
    img1 = np.ones((10, 10), dtype=np.uint8)
    filename1 = os.path.join(cache_dir, "MS600_BP0_img1.png")
    img2 = np.ones((10, 10), dtype=np.uint8)
    filename2 = os.path.join(cache_dir, "MS750_BP0_img2.png")
    img3 = np.ones((10, 10), dtype=np.uint8)
    filename3 = os.path.join(cache_dir, "MS900_BP0_img3.png")
    cv2.imwrite(filename0, img0)
    cv2.imwrite(filename1, img1)
    cv2.imwrite(filename2, img2)
    cv2.imwrite(filename3, img3)
    # Read one of the images with read_ms
    ms = read_ms(filename1, wavelengths=[450, 600, 750, 900])
    assert isinstance(ms, MS_data)
    assert len(ms.wavelengths) == 4
    sub_ms = ms.select(450)
    assert isinstance(sub_ms, MS_data)
    assert len(sub_ms.wavelengths) == 1
    sub_ms2 = ms.select(450, ms=False)
    assert isinstance(sub_ms2, np.ndarray)
    assert sub_ms2.shape == (10, 10, 1)
    


def test_read_ms_dir(tmpdir):
    """Test for PlantCV"""
    cache_dir = tmpdir.mkdir("cache")
    img0 = np.zeros((10, 10), dtype=np.uint8)
    filename0 = os.path.join(cache_dir, "MS500_BP0_img0.png")
    img1 = np.ones((10, 10), dtype=np.uint8)
    filename1 = os.path.join(cache_dir, "MS560_BP0_img1.png")
    img2 = np.ones((10, 10), dtype=np.uint8)
    filename2 = os.path.join(cache_dir, "MS570_BP0_img2.png")
    img3 = np.ones((10, 10), dtype=np.uint8)
    filename3 = os.path.join(cache_dir, "MS580_BP50_img3.png")
    cv2.imwrite(filename0, img0)
    cv2.imwrite(filename1, img1)
    cv2.imwrite(filename2, img2)
    cv2.imwrite(filename3, img3)
    # Read one of the images with read_ms
    ms = read_ms(cache_dir)
    assert isinstance(ms, MS_data)
    assert len(ms.wavelengths) == 3


def test_read_ms_list(tmpdir):
    """Test for PlantCV"""
    cache_dir = tmpdir.mkdir("cache")
    img0 = np.zeros((10, 10), dtype=np.uint8)
    filename0 = os.path.join(cache_dir, "MS450_BP0_img0.png")
    img1 = np.ones((10, 10), dtype=np.uint8)
    filename1 = os.path.join(cache_dir, "MS600_BP0_img1.png")
    img2 = np.ones((10, 10), dtype=np.uint8)
    filename2 = os.path.join(cache_dir, "MS750_BP0_img2.png")
    img3 = np.ones((10, 10), dtype=np.uint8)
    filename3 = os.path.join(cache_dir, "MS900_BP50_img3.png")
    cv2.imwrite(filename0, img0)
    cv2.imwrite(filename1, img1)
    cv2.imwrite(filename2, img2)
    cv2.imwrite(filename3, img3)
    # Here the BP0 filter will not be enforced.
    ms = read_ms([filename0, filename1, filename2, filename3])
    assert isinstance(ms, MS_data)
    assert len(ms.wavelengths) == 4


def test_read_ms_bad_shape(tmpdir):
    """Test for PlantCV"""
    cache_dir = tmpdir.mkdir("cache")
    img0 = np.zeros((10, 10), dtype=np.uint8)
    filename0 = os.path.join(cache_dir, "MS450_BP0_img0.png")
    img1 = np.ones((15, 15), dtype=np.uint8)
    filename1 = os.path.join(cache_dir, "MS600_BP0_img1.png")
    img2 = np.ones((10, 10), dtype=np.uint8)
    filename2 = os.path.join(cache_dir, "MS750_BP0_img2.png")
    img3 = np.ones((10, 10), dtype=np.uint8)
    filename3 = os.path.join(cache_dir, "MS900_BP50_img3.png")
    cv2.imwrite(filename0, img0)
    cv2.imwrite(filename1, img1)
    cv2.imwrite(filename2, img2)
    cv2.imwrite(filename3, img3)
    with pytest.raises(RuntimeError):
        _ = read_ms(cache_dir)
