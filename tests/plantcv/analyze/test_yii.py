"""Tests for pcv.analyze.yii."""
import os
import pytest
import shutil
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.analyze import yii as analyze_yii
from plantcv.plantcv.photosynthesis.read_cropreporter import read_cropreporter


@pytest.mark.parametrize("frame,data,mlabels,maskval,exp", [
    # test ojip_dark control seq
    ["psd", "ojip_dark", None, 1, 0.80874],
    # test lightadapted control seq and measurement_labels arg
    ["psl", "ojip_light", ["Fq/Fm"], 255, 0.80874],
    ["pmd", "pam_dark", None, 1, 0.95238],
    ["pml", "pam_light", None, 1, 0.95238],
    ["pmt", "pam_time", None, 1, 0.75],
    ["pmt", "pam_time", ["example", "example2"], 255, 0.75],
    ["npq", "ojip_light", None, 255, 0.80874]])
def test_yii_cropreporter(frame, data, mlabels, maskval, exp, test_data):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    label = "t0" if mlabels is None else mlabels[0]
    if frame in ["psd", "psl"]:
        source_path = test_data.photosynthesis.cropreporter
    elif frame in ["pmd", "pml"]:
        source_path = test_data.photosynthesis.cropreporter_v653
    elif frame == "pmt":
        source_path = test_data.photosynthesis.cropreporter_pmt
        label = "t0_fvfm" if mlabels is None else mlabels[0] + "_fvfm"
    else:
        source_path = test_data.photosynthesis.cropreporter_npq

    ps = read_cropreporter(filename=source_path)
    shape = getattr(getattr(ps, frame, None), data, None).shape[0:2]
    read_in_worked = bool(getattr(ps, frame, None))
    assert read_in_worked
    # run analyze
    _ = analyze_yii(ps=ps,
                    labeled_mask=(maskval * np.ones(shape)).astype(np.uint8),
                    n_labels=1, auto_fm=True,
                    measurement_labels=mlabels)
    assert np.isclose(outputs.observations["default_1"][f"yii_median_{label}"]["value"], exp)


def test_yii_cropreporter_13_frame_pmt(test_data, tmpdir, monkeypatch):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    # Create a test tmp directory
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
    shape = getattr(getattr(ps, "pmt", None), "pam_time", None).shape[0:2]
    # run analyze
    _ = analyze_yii(ps=ps,
                    labeled_mask=np.ones(shape),
                    n_labels=1, auto_fm=True,
                    measurement_labels=None)
    assert "yii_median_t0_fvfmpp" in [key for key, value in outputs.observations["default_1"].items()]
    with pytest.raises(RuntimeError):
        _ = analyze_yii(ps=ps, labeled_mask=np.ones(shape),
                        measurement_labels=["x", "y", "z"], label="default")

    
@pytest.mark.parametrize("mlabels, tmask",
                         # test wrong mask shape
                         [[None, np.ones((2, 2))],
                          # test bad measurement_labels
                          [['f', 'm'], np.ones((10, 10), dtype=np.uint8)]])
def test_yii_fatalerror(mlabels, tmask, test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only PSD
    shutil.copyfile(test_data.photosynthesis.cropreporter, os.path.join(cache_dir, "PSII_HDR_test.INF"))
    dat = test_data.photosynthesis.cropreporter.replace("HDR", "PSL")
    dat = dat.replace("INF", "DAT")
    shutil.copyfile(dat, os.path.join(cache_dir, "PSII_PSL_test.DAT"))
    filename = os.path.join(cache_dir, "PSII_HDR_test.INF")
    ps = read_cropreporter(filename=filename)
    read_in_worked = bool(getattr(ps, "psl", False))
    assert read_in_worked
    tmask[0, 0] = 255
    with pytest.raises(RuntimeError):
        _ = analyze_yii(ps=ps, labeled_mask=tmask,
                        measurement_labels=mlabels, label="default")


def test_yii_bad_var(test_data):
    """Test for PlantCV."""
    ps = read_cropreporter(filename=test_data.photosynthesis.cropreporter_rfp)
    read_in_worked = bool(getattr(ps, "rfp", False))
    assert read_in_worked
    with pytest.raises(RuntimeError):
        _ = analyze_yii(ps=ps, labeled_mask=np.ones(ps.rfp.red.shape[0:2]),
                        measurement_labels=None, label="default")


def test_yii_wrong_num_labels(test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only PSD
    shutil.copyfile(test_data.photosynthesis.cropreporter, os.path.join(cache_dir, "PSII_HDR_test.INF"))
    dat = test_data.photosynthesis.cropreporter.replace("HDR", "PSL")
    dat = dat.replace("INF", "DAT")
    shutil.copyfile(dat, os.path.join(cache_dir, "PSII_PSL_test.DAT"))
    filename = os.path.join(cache_dir, "PSII_HDR_test.INF")
    ps = read_cropreporter(filename=filename)
    read_in_worked = bool(getattr(ps, "psl", False))
    assert read_in_worked
    with pytest.raises(RuntimeError):
        _ = analyze_yii(ps=ps,
                        labeled_mask=test_data.create_ps_mask(),
                        measurement_labels=None, label=["prefix", "prefix"])


def test_yii_pam_time(test_data, tmpdir):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only PMT
    shutil.copyfile(test_data.photosynthesis.cropreporter_pmt, os.path.join(cache_dir, "HDR_E0001P0007N0001_GCU24100090_20260226.INF"))
    pmt_dat = test_data.photosynthesis.cropreporter_pmt.replace("HDR", "PMT")
    pmt_dat = pmt_dat.replace("INF", "DAT")
    shutil.copyfile(pmt_dat, os.path.join(cache_dir, "PMT_E0001P0007N0001_GCU24100090_20260226.DAT"))
    fluor_filename = os.path.join(cache_dir, "HDR_E0001P0007N0001_GCU24100090_20260226.INF")
    ps = read_cropreporter(filename=fluor_filename)
    read_in_worked = bool(getattr(ps, "pmt", False))
    assert read_in_worked
    _ = analyze_yii(ps=ps,
                    labeled_mask=np.ones(ps.pmt.pam_time.shape[0:2]),
                    n_labels=1, auto_fm=True,
                    measurement_labels=None)
    assert "yii_median_t0_fvfm" in [key for key, value in outputs.observations["default_1"].items()]


def test_yii_pam_time_bad_labels(test_data, tmpdir):
    """Test for PlantCV."""
    # Clear results
    outputs.clear()
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only PSD
    shutil.copyfile(test_data.photosynthesis.cropreporter,
                    os.path.join(cache_dir, "PSII_HDR_test.INF"))
    dat = test_data.photosynthesis.cropreporter.replace("HDR", "PSL")
    dat = dat.replace("INF", "DAT")
    shutil.copyfile(dat, os.path.join(cache_dir, "PSII_PSL_test.DAT"))
    filename = os.path.join(cache_dir, "PSII_HDR_test.INF")
    ps = read_cropreporter(filename=filename)
    read_in_worked = bool(getattr(ps, "psl", False))
    assert read_in_worked
    with pytest.raises(RuntimeError):
        _ = analyze_yii(ps=ps,
                        labeled_mask=np.ones(ps.psl.ojip_light.shape[0:2]),
                        n_labels=1, auto_fm=True,
                        measurement_labels=["bad", "bad1", "bad2"])
