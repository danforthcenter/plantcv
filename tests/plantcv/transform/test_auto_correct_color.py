"""Tests for auto_correct_color."""
import numpy as np
from plantcv.plantcv.transform import auto_correct_color, auto_correct_color_nonlinear
from plantcv.plantcv.transform.detect_color_card import detect_color_card
from plantcv.plantcv.transform.standard_matrices import std_color_matrix, astro_color_matrix
from plantcv.plantcv.classes import Objects
from plantcv.plantcv._globals import params
from tests import synthetic


def _chip_error(corrected_img, std_matrix, color_chip_size=None):
    """Largest difference between the corrected chips and the standard chips, in 8-bit units."""
    color_matrix = detect_color_card(rgb_img=corrected_img, color_chip_size=color_chip_size, delta_E=False)
    params.function_args = {}
    # Each chip is uniform, so its mean is a whole number of 8-bit units
    return np.max(np.abs(np.rint(color_matrix[:, 1:] * 255) - np.rint(std_matrix[:, 1:] * 255)))


def test_auto_correct_color():
    """Test for PlantCV."""
    # The cast scales B, G and R by 0.9, 0.8 and 0.7, which an affine correction undoes up to rounding:
    # recorded value 1 (8-bit units)
    rgb_img = synthetic.color_cast(synthetic.color_card())
    corrected_img = auto_correct_color(rgb_img=rgb_img)
    params.function_args = {}
    assert corrected_img.shape == rgb_img.shape
    assert _chip_error(corrected_img, std_color_matrix(pos=3)) <= 1


def test_auto_correct_color_subset():
    """Test for PlantCV."""
    rgb_img = synthetic.color_cast(synthetic.color_card())
    # Rectangle around the card body (rows and columns 40 to 481 and 341)
    roi = [np.array([[[20, 20]], [[20, 500]], [[360, 500]], [[360, 20]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi_obj = Objects(contours=[roi], hierarchy=[roi_str])
    corrected_img = auto_correct_color(rgb_img=rgb_img, roi=roi_obj)
    params.function_args = {}
    assert corrected_img.shape == rgb_img.shape
    assert _chip_error(corrected_img, std_color_matrix(pos=3)) <= 1


def test_auto_correct_color_astrocard():
    """Test for PlantCV."""
    rgb_img = synthetic.color_cast(synthetic.astro_card())
    corrected_img = auto_correct_color(rgb_img=rgb_img, color_chip_size="ASTRO")
    params.function_args = {}
    assert corrected_img.shape == rgb_img.shape
    assert _chip_error(corrected_img, astro_color_matrix(), color_chip_size="astro") <= 1


def test_auto_correct_color_nonaffine():
    """Test for PlantCV."""
    # A per-channel scale is linear, so it is in the span of the cubic correction model: recorded value 1
    rgb_img = synthetic.color_cast(synthetic.color_card())
    corrected_img = auto_correct_color_nonlinear(rgb_img=rgb_img)
    params.function_args = {}
    assert corrected_img.shape == rgb_img.shape
    assert _chip_error(corrected_img, std_color_matrix(pos=3)) <= 1
