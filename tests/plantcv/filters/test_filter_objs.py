import numpy as np
import pytest
from plantcv.plantcv import params
from plantcv.plantcv import Objects
from plantcv.plantcv.filters import obj_props
from plantcv.plantcv import create_labels
from tests import synthetic


def test_filter_objs_upper_na():
    """Test for PlantCV."""
    params.debug = "plot"
    mask = synthetic.squares_mask()
    filtered_mask = obj_props(bin_img=mask)
    _, nobjs = create_labels(mask=filtered_mask)
    params.debug = None
    # Every square has area > 0
    assert nobjs == 7


def test_filter_objs_lower_thresh():
    """Test for PlantCV."""
    mask = synthetic.squares_mask()
    filtered_mask = obj_props(bin_img=mask, cut_side="lower", thresh=0.6, regprop="solidity")
    _, nobjs = create_labels(mask=filtered_mask)
    # Solidity < 0.6: the frames with solidity 0.5556, 0.36, 0.19 and 0.0975
    assert nobjs == 4


def test_filter_objs_in_thresh():
    """Test for PlantCV."""
    mask = synthetic.squares_mask()
    filtered_mask = obj_props(bin_img=mask, cut_side="in", thresh=(0.1, 0.6), regprop="solidity")
    _, nobjs = create_labels(mask=filtered_mask)
    # 0.1 < solidity < 0.6: the frames with solidity 0.5556, 0.36 and 0.19
    assert nobjs == 3


def test_filter_objs_out_thresh():
    """Test for PlantCV."""
    mask = synthetic.squares_mask()
    filtered_mask = obj_props(bin_img=mask, cut_side="out", thresh=(0.6, 0.8), regprop="solidity")
    _, nobjs = create_labels(mask=filtered_mask)
    # Every square except the frame with solidity 0.64
    assert nobjs == 6


def test_filter_objs_lower_thresh_roi():
    """Test for PlantCV."""
    mask = synthetic.squares_mask()
    # The ROI (columns 55:245) holds the five frames and leaves out the two filled squares
    roi_con = [np.array([[[55, 5]], [[55, 55]], [[245, 55]], [[245, 5]]], dtype=np.int32)]
    roi_str = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_con], hierarchy=[roi_str])
    filtered_mask = obj_props(bin_img=mask, cut_side="lower", thresh=0.6, regprop="solidity", roi=roi)
    _, nobjs = create_labels(mask=filtered_mask)
    # Four frames inside the ROI pass, and the two filled squares outside the ROI are kept
    assert nobjs == 6


def test_bad_params():
    """PlantCV Test"""
    mask = synthetic.squares_mask()
    with pytest.raises(RuntimeError):
        _ = obj_props(bin_img=mask, cut_side="middle")


def test_bad_thresh_lower():
    """PlantCV Test"""
    mask = synthetic.squares_mask()
    with pytest.raises(RuntimeError):
        _ = obj_props(bin_img=mask, cut_side="lower", thresh=(1, 2))


def test_bad_thresh_in():
    """PlantCV Test"""
    mask = synthetic.squares_mask()
    with pytest.raises(RuntimeError):
        _ = obj_props(bin_img=mask, cut_side="in", thresh=1)


def test_bad_property():
    """PlantCV Test"""
    mask = synthetic.squares_mask()
    with pytest.raises(RuntimeError):
        _ = obj_props(bin_img=mask, regprop="bbox")


def test_empty_mask():
    """PlantCV Test"""
    mask = np.zeros((100, 100))
    fmask = obj_props(bin_img=mask, regprop="solidity")
    assert np.sum(fmask) == 0


def test_filter_objs_upper_thresh():
    """Test for PlantCV."""
    mask = synthetic.squares_mask()
    filtered_mask = obj_props(bin_img=mask, cut_side="upper", thresh=300, regprop="area")
    _, nobjs = create_labels(mask=filtered_mask)
    # Area > 300: the 400 px filled square and the 500 px frame
    assert nobjs == 2


def test_filter_objs_none_pass():
    """Test for PlantCV."""
    mask = synthetic.squares_mask()
    filtered_mask = obj_props(bin_img=mask, cut_side="upper", thresh=1000000, regprop="area")
    _, nobjs = create_labels(mask=filtered_mask)
    assert nobjs == 0
