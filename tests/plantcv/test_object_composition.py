import cv2
import numpy as np
from plantcv.plantcv import object_composition


def test_object_composition(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    contours, _ = object_composition(img=img, contours=cnt, hierarchy=cnt_str)
    expected = test_data.load_composed_contours(test_data.small_composed_contours_file)
    assert np.all(expected) == np.all(contours)


def test_object_composition_grayscale(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    contours, _ = object_composition(img=img, contours=cnt, hierarchy=cnt_str)
    expected = test_data.load_composed_contours(test_data.small_composed_contours_file)
    assert np.all(expected) == np.all(contours)


def test_object_composition_no_contours(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    contours, _ = object_composition(img=img, contours=[], hierarchy=np.array([]))
    assert contours is None


def test_object_composition_nested():
    """Test for PlantCV."""
    # Create test data
    img = np.zeros((100, 100), dtype=np.uint8)
    cnt = [np.array([[[25, 25]], [[25, 49]], [[49, 49]], [[49, 25]]], dtype=np.int32),
           np.array([[[34, 35]], [[35, 34]], [[39, 34]], [[40, 35]], [[40, 39]], [[39, 40]], [[35, 40]], [[34, 39]]],
                    dtype=np.int32)]
    cnt_str = np.array([[[-1, -1,  1, -1], [-1, -1, -1,  0]]], dtype=np.int32)
    _, mask = object_composition(img=img, contours=cnt, hierarchy=cnt_str)
    assert np.count_nonzero(mask) == 600
