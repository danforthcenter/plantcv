"""Tests for pcv.analyze.npq."""
import pytest
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.analyze import npq as analyze_npq


def test_npq_cropreporter(test_data):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    psdata = test_data.psii_cropreporter_new('ojip_both')
    _ = analyze_npq(ps=psdata, labeled_mask=test_data.create_ps_mask(),
                    auto_fm=False,
                    measurement_labels=["Fq/Fm"], label="prefix", min_bin="auto", max_bin="auto")
    assert np.isclose(outputs.observations["prefix_1"]["npq_median_Fq/Fm"]["value"], 0.25)


def test_npq_cropreporter_auto(test_data):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    psdata = test_data.psii_cropreporter_new('ojip_both')
    _ = analyze_npq(ps=psdata, labeled_mask=test_data.create_ps_mask(),
                    auto_fm=True,
                    measurement_labels=["Fq/Fm"], label="prefix", min_bin="auto", max_bin="auto")
    assert np.isclose(outputs.observations["prefix_1"]["npq_median_Fq/Fm"]["value"], 0.25)

    
@pytest.mark.parametrize("mlabels, tmask",
                         # test wrong mask shape
                         [[None, np.ones((2, 2))],
                          # test bad measurement_labels
                          ['fm', np.ones((10, 10), dtype=np.uint8)]])
def test_npq_fatalerror(mlabels, tmask, test_data):
    """Test for PlantCV."""
    tmask[0, 0] = 255
    with pytest.raises(RuntimeError):
        _ = analyze_npq(ps=test_data.psii_cropreporter_new('ojip_both'),
                        labeled_mask=tmask,
                        measurement_labels=mlabels, label="default")


def test_npq_bad_var(test_data):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = analyze_npq(ps=test_data.psii_cropreporter_new('ojip_bad'),
                        labeled_mask=test_data.create_ps_mask(),
                        measurement_labels=None)


def test_npq_wrong_num_labels(test_data):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = analyze_npq(ps=test_data.psii_cropreporter_new('ojip_both'),
                        labeled_mask=test_data.create_ps_mask(),
                        measurement_labels=None, label=["prefix", "prefix"])
