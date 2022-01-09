import cv2
import numpy as np
from plantcv.plantcv import object_composition


def test_object_composition(test_data):
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    contours, _ = object_composition(img=img, contours=cnt, hierarchy=cnt_str)
    expected = test_data.load_composed_contours(test_data.small_composed_contours_file)
    assert np.all(expected) == np.all(contours)


def test_object_composition_grayscale(test_data):
    # Read in test data
    img = cv2.imread(test_data.small_gray_img, -1)
    cnt, cnt_str = test_data.load_contours(test_data.small_contours_file)
    contours, _ = object_composition(img=img, contours=cnt, hierarchy=cnt_str)
    expected = test_data.load_composed_contours(test_data.small_composed_contours_file)
    assert np.all(expected) == np.all(contours)


def test_object_composition_no_contours(test_data):
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    contours, _ = object_composition(img=img, contours=[], hierarchy=np.array([]))
    assert contours is None


# TODO: test contours with a hole
