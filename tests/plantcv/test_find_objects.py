import cv2
import numpy as np
from plantcv.plantcv import find_objects


def test_find_objects(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    mask = cv2.imread(test_data.small_bin_img, -1)
    cnt, _ = test_data.load_contours(test_data.small_contours_file)
    contours, _ = find_objects(img=img, mask=mask)
    # Assert contours match test data
    assert np.all(cnt) == np.all(contours)


def test_find_objects_grayscale_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    mask = cv2.imread(test_data.small_bin_img, -1)
    cnt, _ = test_data.load_contours(test_data.small_contours_file)
    contours, _ = find_objects(img=img, mask=mask)
    # Assert contours match test data
    assert np.all(cnt) == np.all(contours)
