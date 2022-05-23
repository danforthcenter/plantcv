import pytest
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.photosynthesis import analyze_npq


def test_analyze_npq_cropreporter(photosynthesis_test_data):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    da_dark = photosynthesis_test_data.psii_cropreporter('darkadapted')
    da_light = photosynthesis_test_data.psii_cropreporter('lightadapted')
    _ = analyze_npq(ps_da_light=da_light, ps_da_dark=da_dark, mask=photosynthesis_test_data.create_ps_mask(),
                    measurement_labels=["Fq/Fm"], label="prefix", min_bin="auto", max_bin="auto")
    assert outputs.observations["prefix"]["npq_median_Fq/Fm"]["value"] == 0.25


def test_analyze_npq_waltz(photosynthesis_test_data):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    da_dark = photosynthesis_test_data.psii_walz('darkadapted')
    da_light = photosynthesis_test_data.psii_walz('lightadapted')
    _ = analyze_npq(ps_da_light=da_light, ps_da_dark=da_dark, mask=photosynthesis_test_data.create_ps_mask(),
                    measurement_labels=None, label="prefix", min_bin="auto", max_bin="auto")
    assert outputs.observations["prefix"]["npq_median_t40"]["value"] == float((200 / 185) - 1)


@pytest.mark.parametrize("mlabels, tmask",
                         # test wrong mask shape
                         [[None, np.ones((2, 2))],
                          # test non binary mask or not uint8
                          [None, np.random.random((10, 10))],
                          # test bad measurement_labels
                          ['fm', np.ones((10, 10), dtype=np.uint8)]])
def test_analyze_npq_fatalerror(mlabels, tmask, photosynthesis_test_data):
    """Test for PlantCV."""
    tmask[0, 0] = 255
    with pytest.raises(RuntimeError):
        _ = analyze_npq(ps_da_dark=photosynthesis_test_data.psii_cropreporter('darkadapted'),
                        ps_da_light=photosynthesis_test_data.psii_cropreporter('lightadapted'), mask=tmask,
                        measurement_labels=mlabels, label="default")
