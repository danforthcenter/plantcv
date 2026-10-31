"""Tests for pcv.analyze.npq."""
import os
import pytest
import numpy as np
from plantcv.plantcv._globals import params, outputs
from plantcv.plantcv.photosynthesis.read_cropreporter import read_cropreporter
from plantcv.plantcv.analyze import npq as analyze_npq
from tests import synthetic


def test_npq_cropreporter(monkeypatch, tmpdir):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    # set up for printing
    cache_dir = tmpdir.mkdir("cache")
    monkeypatch.setattr(params, "debug", "print")
    monkeypatch.setattr(params, "device", 1)
    monkeypatch.setattr(params, "debug_outdir", cache_dir)
    source_path = synthetic.write_cropreporter(tmpdir, "v441", ["NPQ"])
    ps = read_cropreporter(filename=source_path)
    _ = analyze_npq(ps=ps,
                    labeled_mask=np.ones(ps.ojip_dark.shape[0:2]),
                    auto_fm=False,
                    measurement_labels=["Fq/Fm"],
                    label="prefix", min_bin="auto", max_bin="auto")
    # npq divides F0 by Fmp (#2104): 300 / 250 - 1; Fm / Fmp - 1 would be 3
    assert np.isclose(outputs.observations["prefix_1"]["npq_median_Fq/Fm"]["value"], 0.2)
    assert os.path.exists(os.path.join(cache_dir, "2_NPQ_dataarray.png"))


def test_npq_cropreporter_auto(tmp_path):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    source_path = synthetic.write_cropreporter(tmp_path, "v441", ["NPQ"])
    ps = read_cropreporter(filename=source_path)
    _ = analyze_npq(ps=ps,
                    labeled_mask=(255 * np.ones(ps.ojip_dark.shape[0:2])).astype(np.uint8),
                    auto_fm=True,
                    measurement_labels=["Fq/Fm"],
                    label="prefix", min_bin="auto", max_bin="auto")
    # npq divides F0 by Fmp (#2104): 300 / 250 - 1
    assert np.isclose(outputs.observations["prefix_1"]["npq_median_Fq/Fm"]["value"], 0.2)


def test_npq_pml_pmd_cropreporter(tmp_path):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    source_path = synthetic.write_cropreporter(tmp_path, "v653", ["PMD", "PML"])
    ps = read_cropreporter(filename=source_path)
    ps.ojip_dark = None
    ps.ojip_light = None
    _ = analyze_npq(ps=ps,
                    labeled_mask=(255 * np.ones(ps.pml.pam_light.shape[0:2])).astype(np.uint8),
                    auto_fm=True,
                    measurement_labels=["Fq/Fm"],
                    label="prefix", min_bin="auto", max_bin="auto")
    # npq divides F0 by Fmp (#2104): 300 / 250 - 1
    assert np.isclose(outputs.observations["prefix_1"]["npq_median_Fq/Fm"]["value"], 0.2)


def test_npq_pmt_cropreporter(tmp_path):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    source_path = synthetic.write_cropreporter(tmp_path, "pmt", ["PMT"])
    ps = read_cropreporter(filename=source_path)
    _ = analyze_npq(ps=ps,
                    labeled_mask=np.ones(ps.pmt.pam_time.shape[0:2]),
                    auto_fm=False,
                    measurement_labels=["Fq/Fm", "other"],
                    label="prefix", min_bin="auto", max_bin="auto")
    # t0 has no Fmp frame; in t1 npq divides F0 by Fmp (#2104): 300 / 250 - 1
    assert np.isnan(outputs.observations["prefix_1"]["npq_median_Fq/Fm"]["value"])
    assert np.isclose(outputs.observations["prefix_1"]["npq_median_other"]["value"], 0.2)


@pytest.mark.parametrize("mlabels, tmask",
                         # test wrong mask shape
                         [[None, np.ones((2, 2))],
                          # test bad measurement_labels
                          [['fm', 'fm2'], "mask"]])
def test_npq_fatalerror(mlabels, tmask, tmp_path):
    """Test for PlantCV."""
    source_path = synthetic.write_cropreporter(tmp_path, "v441", ["NPQ"])
    ps = read_cropreporter(filename=source_path)
    if isinstance(tmask, str):
        tmask = np.ones(ps.ojip_dark.shape[0:2])
    else:
        tmask[0, 0] = 255
    with pytest.raises(RuntimeError):
        _ = analyze_npq(ps=ps,
                        labeled_mask=tmask,
                        measurement_labels=mlabels, label="default")


def test_npq_bad_var(tmp_path):
    """Test for PlantCV."""
    source_path = synthetic.write_cropreporter(tmp_path, "gfp", ["RFP"])
    ps = read_cropreporter(filename=source_path)
    with pytest.raises(RuntimeError):
        _ = analyze_npq(ps=ps,
                        labeled_mask=np.ones(ps.rfp.red.shape[0:2]),
                        measurement_labels=None)


def test_npq_wrong_num_labels(tmp_path):
    """Test for PlantCV."""
    source_path = synthetic.write_cropreporter(tmp_path, "v441", ["NPQ"])
    ps = read_cropreporter(filename=source_path)
    with pytest.raises(RuntimeError):
        _ = analyze_npq(ps=ps,
                        labeled_mask=np.ones(ps.ojip_dark.shape[0:2]),
                        measurement_labels=None, label=["prefix", "prefix2"])
