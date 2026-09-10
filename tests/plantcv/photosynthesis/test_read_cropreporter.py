"""Tests for plantcv.photosynthesis.read_cropreporter."""
import os
import shutil
import numpy as np
from plantcv.plantcv import PSII_data
from plantcv.plantcv.photosynthesis import read_cropreporter


def test_read_cropreporter_psd(test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only PSD
    shutil.copyfile(test_data.photosynthesis.cropreporter, os.path.join(cache_dir, "PSII_HDR_test.INF"))
    psd_dat = test_data.photosynthesis.cropreporter.replace("HDR", "PSD")
    psd_dat = psd_dat.replace("INF", "DAT")
    shutil.copyfile(psd_dat, os.path.join(cache_dir, "PSII_PSD_test.DAT"))
    filename = os.path.join(cache_dir, "PSII_HDR_test.INF")

    # Run the test
    ps = read_cropreporter(filename=filename)
    assert isinstance(ps, PSII_data)
    assert ps.psd.ojip_dark.shape == (966, 1296, 21, 1)
    assert ps.psd
    assert "PSD" in repr(ps.psd)


def test_read_cropreporter_psl(test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only PSL
    shutil.copyfile(test_data.photosynthesis.cropreporter, os.path.join(cache_dir, "PSII_HDR_test.INF"))
    psl_dat = test_data.photosynthesis.cropreporter.replace("HDR", "PSL")
    psl_dat = psl_dat.replace("INF", "DAT")
    shutil.copyfile(psl_dat, os.path.join(cache_dir, "PSII_PSL_test.DAT"))
    filename = os.path.join(cache_dir, "PSII_HDR_test.INF")

    # Run the test
    ps = read_cropreporter(filename=filename)
    assert isinstance(ps, PSII_data)
    assert ps.psl.ojip_light.shape == (966, 1296, 21, 1)
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


def test_read_cropreporter_spc_only(test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only SPC
    shutil.copyfile(test_data.photosynthesis.cropreporter, os.path.join(cache_dir, "PSII_HDR_test.INF"))
    spc_dat = test_data.photosynthesis.cropreporter.replace("HDR", "SPC")
    spc_dat = spc_dat.replace("INF", "DAT")
    shutil.copyfile(spc_dat, os.path.join(cache_dir, "PSII_SPC_test.DAT"))
    fluor_filename = os.path.join(cache_dir, "PSII_HDR_test.INF")
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data)
    assert ps.spc
    assert "SPC" in repr(ps.spc)
    assert ps.spc.spectral.array_data.shape == (966, 1296, 3)


def test_read_cropreporter_spc_full(test_data, tmpdir):
    """Test for PlantCV."""
    ps = read_cropreporter(filename=os.path.join(test_data.photosynthesis.cropreporter))
    assert isinstance(ps, PSII_data)
    assert ps.spc
    assert "SPC" in repr(ps.spc)
    assert ps.spc.spectral.array_data.shape == (966, 1296, 6)


def test_read_cropreporter_npq(test_data):
    """Test for PlantCV."""
    ps = read_cropreporter(filename=test_data.photosynthesis.cropreporter_npq)
    assert isinstance(ps, PSII_data) and ps.npq.ojip_dark.shape == (966, 1296, 3, 1)
    assert isinstance(ps, PSII_data) and ps.npq.ojip_light.shape == (966, 1296, 3, 1)
    # check reverse ordered loading
    ps = read_cropreporter(filename=test_data.photosynthesis.cropreporter_npq)
    assert isinstance(ps, PSII_data) and ps.npq.ojip_light.shape == (966, 1296, 3, 1)
    assert isinstance(ps, PSII_data) and ps.npq.ojip_dark.shape == (966, 1296, 3, 1)
    # check shortcut
    ps = read_cropreporter(filename=test_data.photosynthesis.cropreporter_npq)
    assert isinstance(ps, PSII_data) and ps.ojip_light.shape == (966, 1296, 3, 1)
    assert isinstance(ps, PSII_data) and ps.ojip_dark.shape == (966, 1296, 3, 1)
    # check class traits
    assert ps.npq
    assert "NPQ" in repr(ps.npq)


def test_read_cropreporter_chl_only(test_data, tmpdir):
    """Test CHL import."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only CHL
    shutil.copyfile(test_data.photosynthesis.cropreporter,
                    os.path.join(cache_dir,
                                 os.path.basename(test_data.photosynthesis.cropreporter)))
    chl_dat = test_data.photosynthesis.cropreporter.replace("HDR", "CHL")
    chl_dat = chl_dat.replace("INF", "DAT")
    shutil.copyfile(chl_dat, os.path.join(cache_dir, os.path.basename(chl_dat)))
    fluor_filename = os.path.join(cache_dir, os.path.basename(test_data.photosynthesis.cropreporter))
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data)
    assert ps.chl
    assert "loaded=False" in repr(ps.chl)
    # Check for a 2D NumPy array (Height, Width)
    assert len(ps.chl.chlorophyll.shape) == 2
    assert isinstance(ps.chl.chlorophyll, np.ndarray)


def test_read_cropreporter_clr_only(test_data, tmpdir):
    """Test CLR import."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only CLR
    shutil.copyfile(test_data.photosynthesis.cropreporter,
                    os.path.join(cache_dir,
                                 os.path.basename(test_data.photosynthesis.cropreporter)))
    clr_dat = test_data.photosynthesis.cropreporter.replace("HDR", "CLR")
    clr_dat = clr_dat.replace("INF", "DAT")
    shutil.copyfile(clr_dat, os.path.join(cache_dir, os.path.basename(clr_dat)))
    fluor_filename = os.path.join(cache_dir, os.path.basename(test_data.photosynthesis.cropreporter))
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data)
    assert ps.clr
    assert "loaded=False" in repr(ps.clr)
    # Check for a 3D NumPy array (Height, Width, Channels)
    assert len(ps.clr.color.shape) == 3
    assert isinstance(ps.clr.color, np.ndarray)


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
