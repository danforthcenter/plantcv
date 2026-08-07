"""Tests for pcv.analyze.npq."""
import pytest
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.photosynthesis.read_cropreporter import read_cropreporter
from plantcv.plantcv.analyze import npq as analyze_npq


def test_npq_cropreporter(test_data):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    source_path = test_data.photosynthesis.cropreporter_npq
    ps = read_cropreporter(filename=source_path)
    _ = analyze_npq(ps=ps,
                    labeled_mask=np.ones(ps.ojip_dark.shape[0:2]),
                    auto_fm=False,
                    measurement_labels=["Fq/Fm"],
                    label="prefix", min_bin="auto", max_bin="auto")
    assert np.isclose(outputs.observations["prefix_1"]["npq_median_Fq/Fm"]["value"], 1.09790)


def test_npq_cropreporter_auto(test_data):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    source_path = test_data.photosynthesis.cropreporter_npq
    ps = read_cropreporter(filename=source_path)
    _ = analyze_npq(ps=ps,
                    labeled_mask=(255 * np.ones(ps.ojip_dark.shape[0:2])).astype(np.uint8),
                    auto_fm=True,
                    measurement_labels=["Fq/Fm"],
                    label="prefix", min_bin="auto", max_bin="auto")
    assert np.isclose(outputs.observations["prefix_1"]["npq_median_Fq/Fm"]["value"], 1.09790)


def test_npq_pmt_cropreporter(test_data):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    source_path = test_data.photosynthesis.cropreporter_pmt
    ps = read_cropreporter(filename=source_path)
    _ = analyze_npq(ps=ps,
                    labeled_mask=np.ones(ps.pmt.pam_time.shape[0:2]),
                    auto_fm=False,
                    measurement_labels=["Fq/Fm", "other"],
                    label="prefix", min_bin="auto", max_bin="auto")
    assert bool(outputs.observations["prefix_1"]["npq_median_Fq/Fm"])


@pytest.mark.parametrize("mlabels, tmask",
                         # test wrong mask shape
                         [[None, np.ones((2, 2))],
                          # test bad measurement_labels
                          [['fm', 'fm2'], "mask"]])
def test_npq_fatalerror(mlabels, tmask, test_data):
    """Test for PlantCV."""
    source_path = test_data.photosynthesis.cropreporter_npq
    ps = read_cropreporter(filename=source_path)
    if isinstance(tmask, str):
        tmask = np.ones(ps.ojip_dark.shape[0:2])
    else:
        tmask[0, 0] = 255
    with pytest.raises(RuntimeError):
        _ = analyze_npq(ps=ps,
                        labeled_mask=tmask,
                        measurement_labels=mlabels, label="default")


def test_npq_bad_var(test_data):
    """Test for PlantCV."""
    source_path = test_data.photosynthesis.cropreporter_rfp
    ps = read_cropreporter(filename=source_path)
    with pytest.raises(RuntimeError):
        _ = analyze_npq(ps=ps,
                        labeled_mask=np.ones(ps.rfp.red.shape[0:2]),
                        measurement_labels=None)


def test_npq_wrong_num_labels(test_data):
    """Test for PlantCV."""
    source_path = test_data.photosynthesis.cropreporter_npq
    ps = read_cropreporter(filename=source_path)
    with pytest.raises(RuntimeError):
        _ = analyze_npq(ps=ps,
                        labeled_mask=np.ones(ps.ojip_dark.shape[0:2]),
                        measurement_labels=None, label=["prefix", "prefix2"])
