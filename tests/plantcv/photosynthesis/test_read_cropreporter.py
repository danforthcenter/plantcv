"""Tests for plantcv.photosynthesis.read_cropreporter."""
import os
import shutil
import numpy as np
from plantcv.plantcv import PSII_data
from plantcv.plantcv.photosynthesis import read_cropreporter
from tests import synthetic


def test_read_cropreporter_psd(tmp_path):
    """Test for PlantCV."""
    filename = synthetic.write_cropreporter(tmp_path, "v441", ["PSD"])
    ps = read_cropreporter(filename=filename)
    assert isinstance(ps, PSII_data)
    assert ps.psd.ojip_dark.shape == (10, 12, 21, 1)
    # FvFmFrameF0=0 and FvFmFrameFm=5 label frames 1 and 6
    assert list(ps.psd.ojip_dark.frame_label.values) == (["Fdark", "F0"] + [f"PSD{i}" for i in range(2, 6)] +
                                                         ["Fm"] + [f"PSD{i}" for i in range(7, 21)])
    # Frame i + 1 is at FvFmTimePoint{i} = 100 + 50000 * i
    assert list(ps.psd.ojip_dark.frame_num.values) == [0] + [100 + 50000 * i for i in range(20)]
    assert np.all(ps.psd.ojip_dark.values == np.array(synthetic.CROPREPORTER_FRAMES["PSD"])[:, None])
    assert ps.psd
    assert "PSD" in repr(ps.psd)


def test_read_cropreporter_psl(tmp_path):
    """Test for PlantCV."""
    filename = synthetic.write_cropreporter(tmp_path, "v441", ["PSL"])
    ps = read_cropreporter(filename=filename)
    assert isinstance(ps, PSII_data)
    assert ps.psl.ojip_light.shape == (10, 12, 21, 1)
    # FqFmFrameFsp=0 and FqFmFrameFmp=5 label frames 1 and 6
    assert list(ps.psl.ojip_light.frame_label.values) == (["Flight", "Fp"] + [f"PSL{i}" for i in range(2, 6)] +
                                                          ["Fmp"] + [f"PSL{i}" for i in range(7, 21)])
    # Frame i + 1 is at FqFmTimePoint{i} = 100 + 50000 * i
    assert list(ps.psl.ojip_light.frame_num.values) == [0] + [100 + 50000 * i for i in range(20)]
    assert np.all(ps.psl.ojip_light.values == np.array(synthetic.CROPREPORTER_FRAMES["PSL"])[:, None])
    assert ps.psl
    assert "PSL" in repr(ps.psl)


def test_read_cropreporter_pmd(test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only PMD
    shutil.copyfile(test_data.photosynthesis.cropreporter_v653, os.path.join(cache_dir, "HDR_dark_light.INF"))
    pmd_dat = test_data.photosynthesis.cropreporter_v653.replace("HDR", "PMD")
    pmd_dat = pmd_dat.replace("INF", "DAT")
    shutil.copyfile(pmd_dat, os.path.join(cache_dir, "PMD_dark_light.DAT"))
    filename = os.path.join(cache_dir, "HDR_dark_light.INF")
    # Run the test
    ps = read_cropreporter(filename=filename)
    assert isinstance(ps, PSII_data)
    assert ps.pmd.pam_dark.shape == (1500, 2048, 4, 1)
    assert ps.pmd
    assert "PMD" in repr(ps.pmd)


def test_read_cropreporter_pml(test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only PML
    shutil.copyfile(test_data.photosynthesis.cropreporter_v653, os.path.join(cache_dir, "HDR_dark_light.INF"))
    pml_dat = test_data.photosynthesis.cropreporter_v653.replace("HDR", "PML")
    pml_dat = pml_dat.replace("INF", "DAT")
    shutil.copyfile(pml_dat, os.path.join(cache_dir, "PML_dark_light.DAT"))
    filename = os.path.join(cache_dir, "HDR_dark_light.INF")
    # Run the test
    ps = read_cropreporter(filename=filename)
    assert isinstance(ps, PSII_data)
    assert ps.pml.pam_light.shape == (1500, 2048, 4, 1)
    assert ps.pml
    assert "PML" in repr(ps.pml)


def test_read_cropreporter_spc_only(tmp_path):
    """Test for PlantCV."""
    fluor_filename = synthetic.write_cropreporter(tmp_path, "v441", ["SPC"])
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data)
    assert ps.spc
    assert "SPC" in repr(ps.spc)
    assert ps.spc.spectral.array_data.shape == (10, 12, 3)
    assert ps.spc.spectral.wavelength_dict == {540: 0.0, 710: 1.0, 770: 2.0}
    # 13107, 26214 and 39321 are 0.2, 0.4 and 0.6 of 65535
    assert np.allclose(ps.spc.spectral.array_data, [0.2, 0.4, 0.6])


def test_read_cropreporter_spc_full(tmp_path):
    """Test for PlantCV."""
    filename = synthetic.write_cropreporter(tmp_path, "v441", ["CHL", "CLR", "PSD", "PSL", "SPC"])
    ps = read_cropreporter(filename=filename)
    assert isinstance(ps, PSII_data)
    assert ps.spc
    assert "SPC" in repr(ps.spc)
    assert ps.spc.spectral.array_data.shape == (10, 12, 6)
    # CLR is 640, 550 and 475 nm, SPC is 540, 710 and 770 nm; bands are sorted by wavelength
    assert ps.spc.spectral.wavelength_dict == {475: 0.0, 540: 1.0, 550: 2.0, 640: 3.0, 710: 4.0, 770: 5.0}
    expected = np.array([51200, 13107, 38400, 25600, 26214, 39321]) / 65535
    assert np.allclose(ps.spc.spectral.array_data, expected)


def test_read_cropreporter_npq(tmp_path):
    """Test for PlantCV."""
    filename = synthetic.write_cropreporter(tmp_path, "v441", ["NPQ"])
    ps = read_cropreporter(filename=filename)
    assert isinstance(ps, PSII_data) and ps.npq.ojip_dark.shape == (10, 12, 3, 1)
    assert isinstance(ps, PSII_data) and ps.npq.ojip_light.shape == (10, 12, 3, 1)
    # check reverse ordered loading
    ps = read_cropreporter(filename=filename)
    assert isinstance(ps, PSII_data) and ps.npq.ojip_light.shape == (10, 12, 3, 1)
    assert isinstance(ps, PSII_data) and ps.npq.ojip_dark.shape == (10, 12, 3, 1)
    # check shortcut
    ps = read_cropreporter(filename=filename)
    assert isinstance(ps, PSII_data) and ps.ojip_light.shape == (10, 12, 3, 1)
    assert isinstance(ps, PSII_data) and ps.ojip_dark.shape == (10, 12, 3, 1)
    # frames 0-2 are dark-adapted and frames 3-5 light-adapted
    assert list(ps.ojip_dark.frame_label.values) == ["Fdark", "F0", "Fm"]
    assert list(ps.ojip_light.frame_label.values) == ["Flight", "Fp", "Fmp"]
    assert list(ps.ojip_dark.frame_num.values) == [0, 1, 2]
    assert list(ps.ojip_light.frame_num.values) == [3, 4, 5]
    assert np.all(ps.ojip_dark.values == np.array([10, 300, 1000])[:, None])
    assert np.all(ps.ojip_light.values == np.array([20, 150, 250])[:, None])
    # check class traits
    assert ps.npq
    assert "NPQ" in repr(ps.npq)


def test_read_cropreporter_chl_only(tmp_path):
    """Test CHL import."""
    # A frame with a distinct value in every pixel shows the rows and columns are read in place
    chl = np.arange(120).reshape(synthetic.CROPREPORTER_SHAPE)
    fluor_filename = synthetic.write_cropreporter(tmp_path, "v441", {"CHL": [10, chl]})
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data)
    assert ps.chl
    assert "loaded=False" in repr(ps.chl)
    # Check for a 2D NumPy array (Height, Width)
    assert len(ps.chl.chlorophyll.shape) == 2
    assert isinstance(ps.chl.chlorophyll, np.ndarray)
    assert np.array_equal(ps.chl.chlorophyll, chl)


def test_read_cropreporter_clr_only(tmp_path):
    """Test CLR import."""
    fluor_filename = synthetic.write_cropreporter(tmp_path, "v441", ["CLR"])
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data)
    assert ps.clr
    assert "loaded=False" in repr(ps.clr)
    # Check for a 3D NumPy array (Height, Width, Channels)
    assert len(ps.clr.color.shape) == 3
    assert isinstance(ps.clr.color, np.ndarray)
    # Red 25600, green 38400 and blue 51200 become 8-bit BGR (200, 150, 100)
    assert ps.clr.color.dtype == np.uint8
    assert np.all(ps.clr.color == [200, 150, 100])


def test_read_cropreporter_gfp_only(test_data, tmpdir):
    """Test GFP import."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only GFP
    shutil.copyfile(test_data.photosynthesis.cropreporter_gfp, os.path.join(cache_dir, "HDR_DYSeed_20251222191634684.INF"))
    gfp_dat = test_data.photosynthesis.cropreporter_gfp.replace("HDR", "GFP")
    gfp_dat = gfp_dat.replace("INF", "DAT")
    shutil.copyfile(gfp_dat, os.path.join(cache_dir, "GFP_DYSeed_20251222191634684.DAT"))
    fluor_filename = os.path.join(cache_dir, "HDR_DYSeed_20251222191634684.INF")
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data)
    assert ps.gfp
    assert "GFP" in repr(ps.gfp)
    assert ps.gfp.green is not None
    # (rows, cols, frames)
    assert len(ps.gfp.green.shape) == 2
    # reach other attribute first
    ps = read_cropreporter(filename=fluor_filename)
    assert ps.gfp.auto is not None


def test_read_cropreporter_rfp_only(test_data, tmpdir):
    """Test RFP import."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only RFP
    shutil.copyfile(test_data.photosynthesis.cropreporter_rfp, os.path.join(cache_dir, "HDR_DYSeed_20251222191634684.INF"))
    rfp_dat = test_data.photosynthesis.cropreporter_rfp.replace("HDR", "RFP")
    rfp_dat = rfp_dat.replace("INF", "DAT")
    shutil.copyfile(rfp_dat, os.path.join(cache_dir, "RFP_DYSeed_20251222191634684.DAT"))
    fluor_filename = os.path.join(cache_dir, "HDR_DYSeed_20251222191634684.INF")
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data)
    assert ps.rfp
    assert "RFP" in repr(ps.rfp)
    assert ps.rfp.red is not None
    assert len(ps.rfp.red.shape) == 2


def test_read_cropreporter_aph_only(test_data, tmpdir):
    """Test APH (Red / FarRed reflectance) import."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only APH
    shutil.copyfile(test_data.photosynthesis.cropreporter_aph, os.path.join(cache_dir,
                                                                            "HDR_2025-12-12_tob1_20251212205712029.INF"))
    aph_dat = test_data.photosynthesis.cropreporter_aph.replace("HDR", "APH")
    aph_dat = aph_dat.replace("INF", "DAT")
    shutil.copyfile(aph_dat, os.path.join(cache_dir, "APH_2025-12-12_tob1_20251212205712029.DAT"))
    fluor_filename = os.path.join(cache_dir, "HDR_2025-12-12_tob1_20251212205712029.INF")
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data)
    assert ps.aph
    assert "loaded=False" in repr(ps.aph)
    assert hasattr(ps.aph, "red")
    assert hasattr(ps.aph, "farred")


def test_read_cropreporter_aph_farred(test_data, tmpdir):
    """Test APH (Red / FarRed reflectance) import."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only APH
    shutil.copyfile(test_data.photosynthesis.cropreporter_aph, os.path.join(cache_dir,
                                                                            "HDR_2025-12-12_tob1_20251212205712029.INF"))
    aph_dat = test_data.photosynthesis.cropreporter_aph.replace("HDR", "APH")
    aph_dat = aph_dat.replace("INF", "DAT")
    shutil.copyfile(aph_dat, os.path.join(cache_dir, "APH_2025-12-12_tob1_20251212205712029.DAT"))
    fluor_filename = os.path.join(cache_dir, "HDR_2025-12-12_tob1_20251212205712029.INF")
    ps = read_cropreporter(filename=fluor_filename)
    assert hasattr(ps.aph, "farred")


def test_read_cropreporter_pmt_only_9_labels(test_data, tmpdir):
    """Test PMT (PAM Time) import with 9 frames."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only PMT
    shutil.copyfile(test_data.photosynthesis.cropreporter_pmt, os.path.join(cache_dir,
                                                                            "HDR_E0001P0007N0001_GCU24100090_20260226.INF"))
    pmt_dat = test_data.photosynthesis.cropreporter_pmt.replace("HDR", "PMT")
    pmt_dat = pmt_dat.replace("INF", "DAT")
    shutil.copyfile(pmt_dat, os.path.join(cache_dir, "PMT_E0001P0007N0001_GCU24100090_20260226.DAT"))
    fluor_filename = os.path.join(cache_dir, "HDR_E0001P0007N0001_GCU24100090_20260226.INF")
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data)
    assert ps.pmt.pam_time is not None
    assert ps.pmt
    assert "PMT" in repr(ps.pmt)
    # Check that dimensions include x, y, frame_label, and measurement
    assert "frame_label" in ps.pmt.pam_time.coords
    assert "measurement" in ps.pmt.pam_time.coords

    # Verify the shape (x, y, 9 labels, N measurements)
    # The 9 or 13 comes from 'frame_labels' list in read_cropreporter.py, and depends on the presence of second dark adaptation
    num_labels = len(ps.pmt.pam_time.frame_label)
    assert num_labels == 9

    # Check that at least one measurement label was created (t0, t1...)
    assert "t0" in ps.pmt.pam_time.measurement.values

    # Access a value to ensure the loops actually ran
    # This forces the test to "touch" the data assigned inside the loops
    assert ps.pmt.pam_time.sel(frame_label="Fdark", measurement="t0").values.any()

    # Verify the F0p (the very last line of your function)
    assert "F0p" in ps.pmt.pam_time.frame_label.values


def test_read_cropreporter_pmt_only_13_labels(test_data, tmpdir, monkeypatch):
    """Test PMT (PAM Time) import with 13 frames."""
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
    assert isinstance(ps, PSII_data)
    assert ps.pmt.pam_time is not None
    assert ps.pmt
    assert "PMT" in repr(ps.pmt)
    # Check that dimensions include x, y, frame_label, and measurement
    assert "frame_label" in ps.pmt.pam_time.coords
    assert "measurement" in ps.pmt.pam_time.coords

    # Verify the shape (x, y, 13 labels, N measurements)
    # The 9 or 13 comes from 'frame_labels' list in read_cropreporter.py, and depends on the presence of second dark adaptation
    num_labels = len(ps.pmt.pam_time.frame_label)
    assert num_labels == 13

    # Check that at least one measurement label was created (t0, t1...)
    assert "t0" in ps.pmt.pam_time.measurement.values

    # Access a value to ensure the loops actually ran
    # This forces the test to "touch" the data assigned inside the loops
    assert ps.pmt.pam_time.sel(frame_label="Fdark", measurement="t0").values.any()

    # Verify the F0p (the very last line of your function)
    assert "F0p" in ps.pmt.pam_time.frame_label.values
