"""Tests for plantcv.plantcv.analyze.alphaL"""

import os
import pytest
import shutil
import numpy as np
from plantcv.plantcv._globals import outputs
from plantcv.plantcv.analyze import alphaL
from plantcv.plantcv.photosynthesis.read_cropreporter import read_cropreporter


def test_analyze_alphaL(test_data):
    """Test for PlantCV"""
    outputs.clear()
    # get aph data
    ps = read_cropreporter(test_data.photosynthesis.cropreporter_aph)
    _ = alphaL(ps, labeled_mask=np.ones(ps.aph.red.shape))
    assert np.isclose(outputs.observations["default_1"]["alphaL_median"]["value"], 0.080645)


def test_analyze_alphaL_bad_frames(test_data):
    """Test for PlantCV"""
    outputs.clear()
    # get aph data
    ps = read_cropreporter(test_data.photosynthesis.cropreporter_pmt)
    with pytest.raises(RuntimeError):
        _ = alphaL(ps, labeled_mask=np.ones(ps.pmt.pam_time.shape[0:2]))


def test_analyze_alphaL_bad_mask(test_data):
    """Test for PlantCV"""
    outputs.clear()
    # get aph data
    ps = read_cropreporter(test_data.photosynthesis.cropreporter_aph)
    mask = np.ones((100, 100))
    with pytest.raises(RuntimeError):
        _ = alphaL(ps, labeled_mask=mask)


def test_analyze_alphaL_binary_mask(test_data):
    """Test for PlantCV"""
    outputs.clear()
    # get aph data
    ps = read_cropreporter(test_data.photosynthesis.cropreporter_aph)
    mask = (255 * np.ones(ps.aph.red.shape)).astype(np.uint8)
    _ = alphaL(ps, labeled_mask=mask)
    assert np.isclose(outputs.observations["default_1"]["alphaL_median"]["value"], 0.080645)
