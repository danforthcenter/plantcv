"""Tests for plantcv.plantcv.analyze.alphaL"""

import pytest
import numpy as np
from plantcv.plantcv._globals import outputs, params
from plantcv.plantcv.analyze import alphaL
from plantcv.plantcv.photosynthesis.read_cropreporter import read_cropreporter
from tests import synthetic


def test_analyze_alphaL(tmp_path):
    """Test for PlantCV"""
    outputs.clear()
    # get aph data
    ps = read_cropreporter(synthetic.write_cropreporter(tmp_path, "aph", ["APH"]))
    _ = alphaL(ps, labeled_mask=np.ones(ps.aph.red.shape))
    # 1 - red / far-red = 1 - 600 / 800
    assert np.isclose(outputs.observations["default_1"]["alphaL_median"]["value"], 0.25)


def test_analyze_alphaL_bad_frames(tmp_path):
    """Test for PlantCV"""
    outputs.clear()
    # get aph data
    ps = read_cropreporter(synthetic.write_cropreporter(tmp_path, "pmt", ["PMT"]))
    with pytest.raises(RuntimeError):
        _ = alphaL(ps, labeled_mask=np.ones(ps.pmt.pam_time.shape[0:2]))


def test_analyze_alphaL_bad_mask(tmp_path):
    """Test for PlantCV"""
    outputs.clear()
    # get aph data
    ps = read_cropreporter(synthetic.write_cropreporter(tmp_path, "aph", ["APH"]))
    mask = np.ones((100, 100))
    with pytest.raises(RuntimeError):
        _ = alphaL(ps, labeled_mask=mask)


def test_analyze_alphaL_binary_mask(tmp_path):
    """Test for PlantCV"""
    outputs.clear()
    # get aph data
    ps = read_cropreporter(synthetic.write_cropreporter(tmp_path, "aph", ["APH"]))
    mask = (255 * np.ones(ps.aph.red.shape)).astype(np.uint8)
    _ = alphaL(ps, labeled_mask=mask)
    # 1 - 600 / 800
    assert np.isclose(outputs.observations["default_1"]["alphaL_median"]["value"], 0.25)


def test_analyze_alphaL_out_of_bins(tmp_path, monkeypatch, capsys):
    """Test for PlantCV"""
    outputs.clear()
    monkeypatch.setattr(params, "verbose", True)
    # red three times far-red gives 1 - 900 / 300 = -2, below min_bin = -1
    ps = read_cropreporter(synthetic.write_cropreporter(tmp_path, "aph", {"APH": [900, 300]}))
    _ = alphaL(ps, labeled_mask=np.ones(ps.aph.red.shape))
    assert np.isclose(outputs.observations["default_1"]["alphaL_median"]["value"], -2)
    assert "alphaL values range from -2.0... to -2.0..." in capsys.readouterr().err
