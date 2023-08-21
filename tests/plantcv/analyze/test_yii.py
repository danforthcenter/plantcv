"""Tests for pcv.analyze.yii."""
import pytest
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.analyze import yii as analyze_yii


@pytest.mark.parametrize("prot,mlabels,exp", [
    # test ojip_dark control seq
    ["ojip_dark", None, 0.8],
    # test lightadapted control seq and measurement_labels arg
    ["ojip_light", ["Fq/Fm"], 0.8]])
def test_yii_cropreporter(prot, mlabels, exp, test_data):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    _ = analyze_yii(ps_da=test_data.psii_cropreporter(prot),
                    labeled_mask=test_data.create_ps_mask(),
                    n_labels=1, auto_fm=True,
                    measurement_labels=mlabels)
    label = "t0" if mlabels is None else mlabels[0]
    assert np.isclose(outputs.observations["default1"][f"yii_median_{label}"]["value"], exp)


@pytest.mark.parametrize("prot,mlabels,exp", [
    # test ojip_dark control seq
    ["ojip_dark", ["Fv/Fm"], float(np.around((200 - 30) / 200, decimals=4))],
    # test lightadapted control seq and measurement_labels arg
    ["ojip_light", [f't{i*40}' for i in np.arange(1, 3)], float((185 - 32) / 185)]])
def test_yii_waltz(prot, mlabels, exp, test_data):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    _ = analyze_yii(ps_da=test_data.psii_walz(prot),
                    labeled_mask=test_data.create_ps_mask(),
                    n_labels=1, auto_fm=False,
                    measurement_labels=mlabels, label="default")
    label = "t0" if mlabels is None else mlabels[0]
    assert np.isclose(outputs.observations["default1"][f"yii_median_{label}"]["value"], exp)


@pytest.mark.parametrize("mlabels, tmask",
                         # test wrong mask shape
                         [[None, np.ones((2, 2))],
                          # test bad measurement_labels
                          [['f', 'm'], np.ones((10, 10), dtype=np.uint8)]])
def test_yii_fatalerror(mlabels, tmask, test_data):
    """Test for PlantCV."""
    tmask[0, 0] = 255
    with pytest.raises(RuntimeError):
        _ = analyze_yii(ps_da=test_data.psii_cropreporter('ojip_dark'), labeled_mask=tmask,
                        measurement_labels=mlabels, label="default")


def test_yii_bad_var(test_data):
    """Test for PlantCV."""
    da = test_data.psii_cropreporter('ojip_dark')
    da.name = 'bad'
    with pytest.raises(RuntimeError):
        _ = analyze_yii(ps_da=da, labeled_mask=test_data.create_ps_mask(),
                        measurement_labels=None, label="default")
