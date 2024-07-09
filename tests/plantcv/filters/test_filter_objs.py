import cv2
import pytest
from plantcv.plantcv import params
from plantcv.plantcv.filters import obj_props
from plantcv.plantcv import create_labels


def test_filter_objs_upper_na(filters_test_data):
    """Test for PlantCV."""
    params.debug = "plot"
    # Read in test data
    mask = cv2.imread(filters_test_data.barley_example)
    filtered_mask = obj_props(bin_img=mask)
    _, nobjs = create_labels(mask=filtered_mask)
    params.debug = None
    assert nobjs == 20


def test_filter_objs_lower_thresh(filters_test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(filters_test_data.barley_example)
    filtered_mask = obj_props(bin_img=mask, cut_side="lower", thresh=0.6, regprop="solidity")
    _, nobjs = create_labels(mask=filtered_mask)
    assert nobjs == 11


def test_bad_params(filters_test_data):
    """PlantCV Test"""
    mask = cv2.imread(filters_test_data.barley_example)
    with pytest.raises(RuntimeError):
        _ = obj_props(bin_img=mask, cut_side="middle")


def test_bad_property(filters_test_data):
    """PlantCV Test"""
    mask = cv2.imread(filters_test_data.barley_example)
    with pytest.raises(RuntimeError):
        _ = obj_props(bin_img=mask, regprop="bbox")
