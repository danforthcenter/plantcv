import pytest
import cv2
import numpy as np
from plantcv.plantcv import floodfill


def test_floodfill(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.floodfill, -1)
    fill_img = floodfill(bin_img=img,(137,31),0)
    fill_img = floodfill(bin_img=fill_img,(189,214),0)
    fill_img = floodfill(bin_img=fill_img,(312,361),0)
    # Assert that the image has been filled in
    assert np.sum(fill_img)==0


def test_floodfill_bad_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    with pytest.raises(RuntimeError):
        _ = floodfill(bin_img=img)
