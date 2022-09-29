import cv2
import numpy as np
from plantcv.plantcv import object_composition, Objects

def test_object_composition(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    objs = Objects(contours=cnt, hierarchy=cnt_str)
    contours, _ = object_composition(img=img, objs=objs)
    expected = test_data.load_composed_contours(test_data.small_composed_contours_file)
    assert np.all(expected) == np.all(contours)


def test_object_composition_grayscale(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    objs = Objects(contours=cnt, hierarchy=cnt_str)
    contours, _ = object_composition(img=img, objs=objs)
    expected = test_data.load_composed_contours(test_data.small_composed_contours_file)
    assert np.all(expected) == np.all(contours)


def test_object_composition_no_contours(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    objs = Objects(contours=[], hierarchy=np.array([]))
    contours, _ = object_composition(img=img, objs=objs)
    assert contours is None


def test_object_composition_nested():
    """Test for PlantCV."""
    # Create test data
    img = np.zeros((100, 100), dtype=np.uint8)
    cnt = [np.array([[[25, 25]], [[25, 49]], [[49, 49]], [[49, 25]]], dtype=np.int32),
           np.array([[[34, 35]], [[35, 34]], [[39, 34]], [[40, 35]], [[40, 39]], [[39, 40]], [[35, 40]], [[34, 39]]],
                    dtype=np.int32)]
    cnt_str = np.array([[[-1, -1,  1, -1], [-1, -1, -1,  0]]], dtype=np.int32)
    objs = Objects(contours=cnt, hierarchy=cnt_str)
    _, mask = object_composition(img=img, objs=objs)
    assert np.count_nonzero(mask) == 600
