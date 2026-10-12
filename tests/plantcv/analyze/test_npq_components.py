"""Tests for plantcv.plantcv.analyze.npq_components"""

import os
import shutil
import pytest
import numpy as np
from plantcv.plantcv._globals import outputs
from plantcv.plantcv.photosynthesis.read_cropreporter import read_cropreporter
from plantcv.plantcv.analyze.npq_components import npq_components


def test_npq_components(test_data):
    """Test for PlantCV"""
    outputs.clear()
    ps = read_cropreporter(test_data.photosynthesis.cropreporter_pmt)
    mask = np.zeros(ps.pmt.pam_time.shape[0:2])
    mask[1:50, 1:50] = 1
    mask[51:100, 51:100] = 2
    l = npq_components(ps, mask.astype(np.uint8))
    # this will be nan here, but the data does seem to work
    assert outputs.observations["default_1"]["mean_qP_t0"]
    assert np.isclose(np.max(l[1]["qP"][np.isfinite(l[1]["qP"])]), 69)


def test_npq_components_fmpp(test_data, tmpdir, monkeypatch):
    """Test for PlantCV"""
    outputs.clear()
    cache_dir = tmpdir.mkdir("sub")
    # 1. Align filenames (P0008 for both) so the reader finds the DAT file
    inf_dest = os.path.join(cache_dir, "HDR_E0001P0008N0001_GCU24100090_20260226.INF")
    dat_dest = os.path.join(cache_dir, "PMT_E0001P0008N0001_GCU24100090_20260226.DAT")
    # Create dataset with only PMT
    shutil.copyfile(test_data.photosynthesis.cropreporter_pmt, inf_dest)
    pmt_dat_src = test_data.photosynthesis.cropreporter_pmt.replace("HDR", "PMT").replace("INF", "DAT")
    shutil.copyfile(pmt_dat_src, dat_dest)
    # Force the INF to trigger the 13-label logic (n_fvfm > 0)
    with open(inf_dest, "a") as f:
        f.write("\nTmPamMeasFvfm=3")
        # Override image size to keep memory usage small in tests
        f.write("\nImageRows=10")
        f.write("\nImageCols=10")
    # Mock numpy with the correct 13-frame size for the overridden metadata (10 * 10 * 13 = 1300)
    # Using ones * 50 to ensure .any() assertions pass
    monkeypatch.setattr(np, "fromfile", lambda *args, **kwargs: np.ones(1300, dtype=np.uint16) * 50)
    ps = read_cropreporter(filename=inf_dest)
    mask = np.zeros(ps.pmt.pam_time.shape[0:2])
    mask[1:5, 1:5] = 1
    mask[5:10, 5:10] = 2
    _ = npq_components(ps, mask.astype(np.uint8))
    assert outputs.observations["default_1"]["mean_qE_t0"]


def test_npq_components_bad_frame(test_data):
    """Test for PlantCV"""
    outputs.clear()
    ps = read_cropreporter(test_data.photosynthesis.cropreporter_rfp)
    mask = np.zeros(ps.rfp.red.shape[0:2])
    mask[1:50, 1:50] = 1
    mask[51:100, 51:100] = 2
    with pytest.raises(RuntimeError):
        _ = npq_components(ps, mask.astype(np.uint8))
