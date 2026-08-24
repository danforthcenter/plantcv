"""Tests for pcv.analyze.npqfast"""
import pytest
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.photosynthesis.read_cropreporter import read_cropreporter
from plantcv.plantcv.analyze.npq_fast import npqfast as analyze_npqfast


def test_npqfast(test_data):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    source_path = test_data.photosynthesis.cropreporter_pmt
    ps = read_cropreporter(filename=source_path)
    _ = analyze_npqfast(ps=ps,
                    labeled_mask=(255 * np.ones(ps.pmt.pam_time.shape[0:2])).astype(np.uint8),
                    measurement_labels=["x0", "x1"],
                    label="prefix", min_bin="auto", max_bin="auto")
    assert bool(outputs.observations["prefix_1"]["npqfast_mean_x1"])


def test_npqfast_bad_labels(test_data):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    source_path = test_data.photosynthesis.cropreporter_pmt
    ps = read_cropreporter(filename=source_path)
    with pytest.raises(RuntimeError):
        _ = analyze_npqfast(ps=ps,
                            labeled_mask=(255 * np.ones(ps.pmt.pam_time.shape[0:2])).astype(np.uint8),
                            measurement_labels=["only_one"],
                            label="prefix", min_bin="auto", max_bin="auto")
    

def test_npqfast_bad_frames(test_data):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    source_path = test_data.photosynthesis.cropreporter_npq
    ps = read_cropreporter(filename=source_path)
    with pytest.raises(RuntimeError):
        _ = analyze_npqfast(ps=ps,
                            labeled_mask=(255 * np.ones(ps.npq.ojip_light.shape[0:2])).astype(np.uint8),
                            measurement_labels=None,
                            label="prefix", min_bin="auto", max_bin="auto")


def test_npqfast_bad_mask_shape(test_data):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    source_path = test_data.photosynthesis.cropreporter_pmt
    ps = read_cropreporter(filename=source_path)
    with pytest.raises(RuntimeError):
        _ = analyze_npqfast(ps=ps,
                            labeled_mask=(255 * np.ones((10, 10))).astype(np.uint8),
                            measurement_labels=None,
                            label="prefix", min_bin="auto", max_bin="auto")
