"""Tests for plantcv.plantcv.analyze.npq_components"""

import pytest
import numpy as np
from plantcv.plantcv._globals import outputs
from plantcv.plantcv.photosynthesis.read_cropreporter import read_cropreporter
from plantcv.plantcv.analyze.npq_components import npq_components
from tests import synthetic


def test_npq_components(tmp_path):
    """Test for PlantCV"""
    outputs.clear()
    ps = read_cropreporter(synthetic.write_cropreporter(tmp_path, "pmt", ["PMT"]))
    mask = np.zeros(ps.pmt.pam_time.shape[0:2])
    mask[1:5, 1:6] = 1
    mask[5:10, 6:12] = 2
    comps = npq_components(ps, mask.astype(np.uint8))
    # qP = (Fmp - Fp) / (Fmp - F0p) = (250 - 150) / (250 - 125)
    assert np.isclose(outputs.observations["default_1"]["mean_qP_t1"]["value"], 0.8)
    assert np.allclose(comps[0]["qP"][mask == 1], 0.8)
    # Only label 1 is analyzed (n_labels=1)
    assert np.all(comps[0]["qP"][mask != 1] == 0)


def test_npq_components_fmpp(tmp_path):
    """Test for PlantCV"""
    outputs.clear()
    # TmPamMeasFvfm=3 adds two measurements of the second dark adaptation, t2 and t3
    inf_dest = synthetic.write_cropreporter(tmp_path, "pmt", {"PMT": synthetic.pmt_frames(n_fvfm=2)},
                                            metadata={"TmPamMeasFvfm": 3})
    ps = read_cropreporter(filename=inf_dest)
    mask = np.zeros(ps.pmt.pam_time.shape[0:2])
    mask[1:5, 1:5] = 1
    mask[5:10, 5:10] = 2
    _ = npq_components(ps, mask.astype(np.uint8))
    # qE = Fm * (Fmpp - Fmp) / (Fmpp * Fmp) = 1000 * (800 - 250) / (800 * 250)
    assert np.isclose(outputs.observations["default_1"]["mean_qE_t2"]["value"], 2.75)
    assert np.isclose(outputs.observations["default_1"]["mean_qE_t3"]["value"], 2.75)


def test_npq_components_bad_frame(tmp_path):
    """Test for PlantCV"""
    outputs.clear()
    ps = read_cropreporter(synthetic.write_cropreporter(tmp_path, "gfp", ["RFP"]))
    mask = np.zeros(ps.rfp.red.shape[0:2])
    mask[1:5, 1:6] = 1
    mask[5:10, 6:12] = 2
    with pytest.raises(RuntimeError):
        _ = npq_components(ps, mask.astype(np.uint8))


def test_npq_components_no_light_measurements(tmp_path):
    """Test for PlantCV."""
    outputs.clear()
    ps = read_cropreporter(synthetic.write_cropreporter(tmp_path, "pmt", ["PMT"]))
    ps.pmt.pam_time.coords["frame_label"] = [
        "frame_" + str(i) for i in range(len(ps.pmt.pam_time.frame_label))
    ]
    mask = np.ones(synthetic.CROPREPORTER_SHAPE, dtype=np.uint8)
    with pytest.raises(RuntimeError):
        _ = npq_components(ps, mask)


def test_npq_components_frame_pairing(tmp_path):
    """Test that frames are paired across measurements"""
    outputs.clear()
    # t0 = dark-adapted baseline, t1 = light, t2 = recovery (also holds F0p)
    inf_dest = synthetic.write_cropreporter(tmp_path, "pmt", {"PMT": synthetic.pmt_frames(n_fvfm=1)},
                                            metadata={"TmPamMeasFvfm": 2})
    ps = read_cropreporter(filename=inf_dest)
    mask = np.ones(synthetic.CROPREPORTER_SHAPE, dtype=np.uint8)
    out = npq_components(ps, mask)
    obs = outputs.observations["default_1"]
    # light components are only reported for the light measurement (t1)
    assert "mean_qP_t0" not in obs
    assert np.isclose(obs["mean_qP_t1"]["value"], (250 - 150) / (250 - 125))
    assert np.isclose(obs["mean_qN_t1"]["value"], 1 - (250 - 125) / (1000 - 300))
    # recovery components use Fm from t0 and Fmp from t1
    assert np.isclose(obs["mean_qI_t2"]["value"], (1000 - 800) / 800)
    assert np.isclose(obs["mean_qE_t2"]["value"], 1000 * (800 - 250) / (800 * 250))
    assert [d["measurement"] for d in out] == ["t1", "t2"]
