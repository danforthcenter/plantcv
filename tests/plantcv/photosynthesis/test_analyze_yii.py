import pytest
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.photosynthesis import analyze_yii


@pytest.mark.parametrize("prot,mlabels,exp", [
    # test darkadapted control seq
    ["darkadapted", None, 0.8],
    # test lightadapted control seq and measurement_labels arg
    ["lightadapted", ["Fq/Fm"], 0.75]])
def test_analyze_yii_cropreporter(prot, mlabels, exp, photosynthesis_test_data):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    _ = analyze_yii(ps_da=photosynthesis_test_data.psii_cropreporter(prot),
                    mask=photosynthesis_test_data.create_ps_mask(),
                    measurement_labels=mlabels, label="default")
    label = "t0" if mlabels is None else mlabels[0]
    assert outputs.observations["default"][f"yii_median_{label}"]["value"] == exp


@pytest.mark.parametrize("prot,mlabels,exp", [
    # test darkadapted control seq
    ["darkadapted", ["Fv/Fm"], float(np.around((200 - 30) / 200, decimals=4))],
    # test lightadapted control seq and measurement_labels arg
    ["lightadapted", [f't{i*40}' for i in np.arange(1, 3)], float((185 - 32) / 185)]])
def test_analyze_yii_waltz(prot, mlabels, exp, photosynthesis_test_data):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    _ = analyze_yii(ps_da=photosynthesis_test_data.psii_walz(prot),
                    mask=photosynthesis_test_data.create_ps_mask(),
                    measurement_labels=mlabels, label="default")
    label = "t0" if mlabels is None else mlabels[0]
    assert outputs.observations["default"][f"yii_median_{label}"]["value"] == exp


@pytest.mark.parametrize("mlabels, tmask",
                         # test wrong mask shape
                         [[None, np.ones((2, 2))],
                          # test non binary mask
                          [None, np.random.random((10, 10))],
                          # test bad measurement_labels
                          [['f', 'm'], np.ones((10, 10), dtype=np.uint8)]])
def test_analyze_yii_fatalerror(mlabels, tmask, photosynthesis_test_data):
    """Test for PlantCV."""
    tmask[0, 0] = 255
    with pytest.raises(RuntimeError):
        _ = analyze_yii(ps_da=photosynthesis_test_data.psii_cropreporter('darkadapted'), mask=tmask,
                        measurement_labels=mlabels, label="default")
