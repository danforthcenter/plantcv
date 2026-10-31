"""Tests for pcv.analyze.yii."""
import pytest
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.analyze import yii as analyze_yii
from plantcv.plantcv.photosynthesis.read_cropreporter import read_cropreporter
from tests import synthetic


@pytest.mark.parametrize("frame,data,mlabels,maskval,exp", [
    # test ojip_dark control seq: Fv/Fm = (Fm - F0) / Fm = (1000 - 300) / 1000
    ["psd", "ojip_dark", None, 1, 0.7],
    # test lightadapted control seq and measurement_labels arg: Fq'/Fm' = (Fmp - Fp) / Fmp = (250 - 150) / 250
    ["psl", "ojip_light", ["Fq/Fm"], 255, 0.4],
    # Fv/Fm = (1000 - 300) / 1000
    ["pmd", "pam_dark", None, 1, 0.7],
    # Fq'/Fm' = (250 - 150) / 250
    ["pml", "pam_light", None, 1, 0.4],
    # Fv/Fm of the dark-adapted measurement, (1000 - 300) / 1000
    ["pmt", "pam_time", None, 1, 0.7],
    ["pmt", "pam_time", ["example", "example2"], 255, 0.7],
    # Fq'/Fm' of the light-adapted NPQ frames, (250 - 150) / 250
    ["npq", "ojip_light", None, 255, 0.4]])
def test_yii_cropreporter(frame, data, mlabels, maskval, exp, tmp_path):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    template = {"pmd": "v653", "pml": "v653", "pmt": "pmt"}.get(frame, "v441")
    source_path = synthetic.write_cropreporter(tmp_path, template, [frame.upper()])

    ps = read_cropreporter(filename=source_path)
    ps_frame = getattr(ps, frame, None)
    assert bool(ps_frame)
    ps_da = getattr(ps_frame, data, None)
    shape = ps_da.shape[0:2]

    if mlabels is None:
        label = str(ps_da.measurement.values[0])
        if frame == "pmt":
            label = f"{label}_fvfm"
    else:
        label = mlabels[0]
        if frame == "pmt":
            label = f"{label}_fvfm"
    # run analyze
    _ = analyze_yii(ps=ps,
                    labeled_mask=(maskval * np.ones(shape)).astype(np.uint8),
                    n_labels=1, auto_fm=True,
                    measurement_labels=mlabels)
    assert np.isclose(outputs.observations["default_1"][f"yii_median_{label}"]["value"], exp)


def test_yii_cropreporter_13_frame_pmt(tmp_path):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    # TmPamMeasFvfm=3 adds two measurements of the second dark adaptation, t2 and t3
    inf_dest = synthetic.write_cropreporter(tmp_path, "pmt", {"PMT": synthetic.pmt_frames(n_fvfm=2)},
                                            metadata={"TmPamMeasFvfm": 3})
    ps = read_cropreporter(filename=inf_dest)
    shape = getattr(getattr(ps, "pmt", None), "pam_time", None).shape[0:2]
    # run analyze
    _ = analyze_yii(ps=ps,
                    labeled_mask=np.ones(shape),
                    n_labels=1, auto_fm=True,
                    measurement_labels=None)
    assert "yii_median_t0_fvfmpp" in [key for key, value in outputs.observations["default_1"].items()]
    # Fv''/Fm'' = (Fmpp - F0pp) / Fmpp = (800 - 280) / 800
    assert np.isclose(outputs.observations["default_1"]["yii_median_t2_fvfmpp"]["value"], 0.65)
    with pytest.raises(RuntimeError):
        _ = analyze_yii(ps=ps, labeled_mask=np.ones(shape),
                        measurement_labels=["x", "y", "z"], label="default")


@pytest.mark.parametrize("mlabels, tmask",
                         # test wrong mask shape
                         [[None, np.ones((2, 2))],
                          # test bad measurement_labels
                          [['f', 'm'], np.ones(synthetic.CROPREPORTER_SHAPE, dtype=np.uint8)]])
def test_yii_fatalerror(mlabels, tmask, tmp_path):
    """Test for PlantCV."""
    filename = synthetic.write_cropreporter(tmp_path, "v441", ["PSL"])
    ps = read_cropreporter(filename=filename)
    read_in_worked = bool(getattr(ps, "psl", False))
    assert read_in_worked
    tmask[0, 0] = 255
    with pytest.raises(RuntimeError):
        _ = analyze_yii(ps=ps, labeled_mask=tmask,
                        measurement_labels=mlabels, label="default")


def test_yii_bad_var(tmp_path):
    """Test for PlantCV."""
    ps = read_cropreporter(filename=synthetic.write_cropreporter(tmp_path, "gfp", ["RFP"]))
    read_in_worked = bool(getattr(ps, "rfp", False))
    assert read_in_worked
    with pytest.raises(RuntimeError):
        _ = analyze_yii(ps=ps, labeled_mask=np.ones(ps.rfp.red.shape[0:2]),
                        measurement_labels=None, label="default")


def test_yii_wrong_num_labels(tmp_path):
    """Test for PlantCV."""
    filename = synthetic.write_cropreporter(tmp_path, "v441", ["PSL"])
    ps = read_cropreporter(filename=filename)
    read_in_worked = bool(getattr(ps, "psl", False))
    assert read_in_worked
    with pytest.raises(RuntimeError):
        _ = analyze_yii(ps=ps,
                        labeled_mask=synthetic.psii_mask(),
                        measurement_labels=None, label=["prefix", "prefix"])


def test_yii_pam_time(tmp_path):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    ps = read_cropreporter(filename=synthetic.write_cropreporter(tmp_path, "pmt", ["PMT"]))
    read_in_worked = bool(getattr(ps, "pmt", False))
    assert read_in_worked
    _ = analyze_yii(ps=ps,
                    labeled_mask=np.ones(ps.pmt.pam_time.shape[0:2]),
                    n_labels=1, auto_fm=True,
                    measurement_labels=None)
    assert "yii_median_t0_fvfm" in [key for key, value in outputs.observations["default_1"].items()]
    # (1000 - 300) / 1000
    assert np.isclose(outputs.observations["default_1"]["yii_median_t0_fvfm"]["value"], 0.7)


def test_yii_pam_time_bad_labels(tmp_path):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    filename = synthetic.write_cropreporter(tmp_path, "v441", ["PSL"])
    ps = read_cropreporter(filename=filename)
    read_in_worked = bool(getattr(ps, "psl", False))
    assert read_in_worked
    with pytest.raises(RuntimeError):
        _ = analyze_yii(ps=ps,
                        labeled_mask=np.ones(ps.psl.ojip_light.shape[0:2]),
                        n_labels=1, auto_fm=True,
                        measurement_labels=["bad", "bad1", "bad2"])
