"""Tests for auto_correct_color."""
import numpy as np
import cv2
from plantcv.plantcv.transform import auto_correct_color
from plantcv.plantcv import Objects


def test_auto_correct_color(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    corrected_img = auto_correct_color(rgb_img=rgb_img)
    assert np.shape(corrected_img) == np.shape(rgb_img) and np.sum(corrected_img) != np.sum(rgb_img)


def test_auto_correct_color_subset(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.colorcard_img)
    roi = [np.array([[[750, 250]], [[750, 1249]], [[1499, 1249]], [[1499, 250]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_obj = Objects(contours=[roi], hierarchy=[roi_str])
    corrected_img = auto_correct_color(rgb_img=rgb_img, roi=roi_obj)
    assert np.shape(corrected_img) == np.shape(rgb_img) and np.sum(corrected_img) != np.sum(rgb_img)


def test_auto_correct_color_astrocard(transform_test_data):
    """Test for PlantCV."""
    # Load rgb image
    rgb_img = cv2.imread(transform_test_data.astrocard_img)
    corrected_img = auto_correct_color(rgb_img=rgb_img, color_chip_size="ASTRO")
    assert np.shape(corrected_img) == np.shape(rgb_img) and np.sum(corrected_img) != np.sum(rgb_img)
