"""Tests for pcv.analyze.npq."""
import pytest
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.analyze import npq as analyze_npq


def test_npq_cropreporter(test_data):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    da_dark = test_data.psii_cropreporter('ojip_dark')
    da_light = test_data.psii_cropreporter('ojip_light')
    _ = analyze_npq(ps_da_light=da_light, ps_da_dark=da_dark, labeled_mask=test_data.create_ps_mask(),
                    auto_fm=False,
                    measurement_labels=["Fq/Fm"], label="prefix", min_bin="auto", max_bin="auto")
    assert np.isclose(outputs.observations["prefix1"]["npq_median_Fq/Fm"]["value"], 0.25)


def test_npq_waltz(test_data):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    da_dark = test_data.psii_walz('ojip_dark')
    da_light = test_data.psii_walz('ojip_light')
    _ = analyze_npq(ps_da_light=da_light, ps_da_dark=da_dark, labeled_mask=test_data.create_ps_mask(), auto_fm=True,
                    measurement_labels=None, label="prefix", min_bin="auto", max_bin="auto")
    assert np.isclose(outputs.observations["prefix1"]["npq_median_t40"]["value"], float((200 / 185) - 1))


@pytest.mark.parametrize("mlabels, tmask",
                         # test wrong mask shape
                         [[None, np.ones((2, 2))],
                          # test bad measurement_labels
                          ['fm', np.ones((10, 10), dtype=np.uint8)]])
def test_npq_fatalerror(mlabels, tmask, test_data):
    """Test for PlantCV."""
    tmask[0, 0] = 255
    with pytest.raises(RuntimeError):
        _ = analyze_npq(ps_da_dark=test_data.psii_cropreporter('ojip_dark'),
                        ps_da_light=test_data.psii_cropreporter('ojip_light'), labeled_mask=tmask,
                        measurement_labels=mlabels, label="default")


def test_npq_bad_var(test_data):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = analyze_npq(ps_da_dark=test_data.psii_cropreporter('ojip_light'),
                        ps_da_light=test_data.psii_cropreporter('ojip_dark'),
                        labeled_mask=test_data.create_ps_mask(),
                        measurement_labels=None)
