"""Tests for pcv.analyze.npqfast"""
import pytest
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.photosynthesis.read_cropreporter import read_cropreporter
from plantcv.plantcv.analyze.npq_fast import npqfast as analyze_npqfast
from tests import synthetic


def test_npqfast(tmp_path):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    source_path = synthetic.write_cropreporter(tmp_path, "pmt", ["PMT"])
    ps = read_cropreporter(filename=source_path)
    _ = analyze_npqfast(ps=ps,
                        labeled_mask=(255 * np.ones(ps.pmt.pam_time.shape[0:2])).astype(np.uint8),
                        measurement_labels=["x0", "x1"],
                        label="prefix", min_bin="auto", max_bin="auto")
    # t0 has no Fmp frame; in t1 4.88 / (Fmp / F0p - 1) - 1 = 4.88 / (250 / 125 - 1) - 1
    assert np.isnan(outputs.observations["prefix_1"]["npqfast_mean_x0"]["value"])
    assert np.isclose(outputs.observations["prefix_1"]["npqfast_mean_x1"]["value"], 3.88)


def test_npqfast_bad_labels(tmp_path):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    source_path = synthetic.write_cropreporter(tmp_path, "pmt", ["PMT"])
    ps = read_cropreporter(filename=source_path)
    with pytest.raises(RuntimeError):
        _ = analyze_npqfast(ps=ps,
                            labeled_mask=(255 * np.ones(ps.pmt.pam_time.shape[0:2])).astype(np.uint8),
                            measurement_labels=["only_one"],
                            label="prefix", min_bin="auto", max_bin="auto")


def test_npqfast_bad_frames(tmp_path):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    source_path = synthetic.write_cropreporter(tmp_path, "v441", ["NPQ"])
    ps = read_cropreporter(filename=source_path)
    with pytest.raises(RuntimeError):
        _ = analyze_npqfast(ps=ps,
                            labeled_mask=(255 * np.ones(ps.npq.ojip_light.shape[0:2])).astype(np.uint8),
                            measurement_labels=None,
                            label="prefix", min_bin="auto", max_bin="auto")


def test_npqfast_bad_mask_shape(tmp_path):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    source_path = synthetic.write_cropreporter(tmp_path, "pmt", ["PMT"])
    ps = read_cropreporter(filename=source_path)
    with pytest.raises(RuntimeError):
        _ = analyze_npqfast(ps=ps,
                            labeled_mask=(255 * np.ones((10, 10))).astype(np.uint8),
                            measurement_labels=None,
                            label="prefix", min_bin="auto", max_bin="auto")
