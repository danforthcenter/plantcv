import os
import cv2
import random
import pytest
import numpy as np
from plantcv.plantcv._globals import params
from plantcv.plantcv.submask import sub_mask

random.seed(a=123)

def test_sub_mask_success(test_data, tmpdir):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    cache_dir = tmpdir.mkdir("cache")
    debug_state = params.debug
    params.debug = "print"
    params.debug_outdir = str(cache_dir)
    spots = sub_mask(img, mask, 2, 2)
    params.debug = debug_state
    assert len(np.unique(spots)) == 3
    assert len(os.listdir(cache_dir)) == 1


def test_sub_mask_too_large(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    spots = sub_mask(img, mask, 2, 20)
    assert len(np.unique(spots)) == 1


def test_sub_mask_too_many(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    spots = sub_mask(img, mask, 5, 3)
    assert len(np.unique(spots)) == 2


def test_sub_mask_empty(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img, -1)
    mask = np.zeros(img.shape[0:2])
    with pytest.raises(RuntimeError):
        _ = sub_mask(img, mask, 5, 3)

