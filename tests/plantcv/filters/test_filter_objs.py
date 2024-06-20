import cv2
import pytest
import plantcv.plantcv as pcv
from plantcv.plantcv.filters import filter_objs
from plantcv.plantcv import create_labels


def test_filter_objs_upper_na(filters_test_data):
    """Test for PlantCV."""
    pcv.params.debug = "plot"
    # Read in test data
    mask = cv2.imread(filters_test_data.barley_example)
    filtered_mask = filter_objs(bin_img=mask)
    _, nobjs = create_labels(mask=filtered_mask)
    assert nobjs == 7

def test_filter_objs_lower_thresh(filters_test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(filters_test_data.barley_example)
    filtered_mask = filter_objs(bin_img=mask, cut_side="lower", thresh=0.6, regprop="solidity")
    _, nobjs = create_labels(mask=filtered_mask)
    assert nobjs == 11

def test_bad_params(filters_test_data):
    """PlantCV Test"""
    mask = cv2.imread(filters_test_data.barley_example)
    with pytest.raises(RuntimeError):
        _ = filter_objs(bin_img=mask, cut_side="middle")

def test_bad_property(filters_test_data):
    """PlantCV Test"""
    mask = cv2.imread(filters_test_data.barley_example)
    with pytest.raises(RuntimeError):
        _ = filter_objs(bin_img=mask, regprop="bbox")
