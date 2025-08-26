"""Tests for pcv.analyze.radial"""
import pytest
import cv2
from plantcv.plantcv.analyze.radial import radial_percentile
from plantcv.plantcv import Objects
from plantcv.plantcv._helpers import _cv2_findcontours


def test_radial_RGB(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.rgb_seed)
    mask = cv2.imread(test_data.rgb_seed_mask, -1)
    avgs = radial_percentile(img=img, mask=mask)
    assert int(avgs[0][0]) == 138

def test_radial_gray(test_data):
    """Test for PlantCV."""
    # Read in roi
    circle = cv2.imread(test_data.small_circle, -1)
    roi_contour, roi_hierarchy = _cv2_findcontours(bin_img=circle)
    roi = Objects(contours=[roi_contour], hierarchy=[roi_hierarchy])
    # Read in test data as gray
    img = cv2.imread(test_data.rgb_seed, 0)
    mask = cv2.imread(test_data.rgb_seed_mask, -1)
    avgs = radial_percentile(img=img, mask=mask, roi=roi)
    assert int(avgs[0]) == 96

def test_radial_error(test_data):
    """Test for PlantCV."""
    # Read in incorrect circle
    circle = cv2.imread(test_data.bad_circle, -1)
    roi_contour, roi_hierarchy = _cv2_findcontours(bin_img=circle)
    roi = Objects(contours=[roi_contour], hierarchy=[roi_hierarchy])
    # Read in test data
    img = cv2.imread(test_data.rgb_seed)
    mask = cv2.imread(test_data.rgb_seed_mask, -1)
    # Object is too small
    with pytest.raises(RuntimeError):
        _ = radial_percentile(img=img, mask=mask, roi=roi)