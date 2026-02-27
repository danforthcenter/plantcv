"""Tests for plantcv.photosynthesis.read_cropreporter."""
import os
import shutil
from plantcv.plantcv import PSII_data
from plantcv.plantcv.photosynthesis import read_cropreporter


def test_read_cropreporter(photosynthesis_test_data, tmpdir):
    """Test for PlantCV."""
    ps = read_cropreporter(filename=photosynthesis_test_data.cropreporter)
    assert isinstance(ps, PSII_data) and ps.ojip_dark.shape == (966, 1296, 21, 1)

    # Check with different naming conventioned of phenovation
    ps = read_cropreporter(filename=photosynthesis_test_data.cropreporter_v653)
    assert isinstance(ps, PSII_data) and ps.ojip_dark.shape == (1500, 2048, 7, 1)
    # check labels
    true_labels = ['Fdark', 'F0', 'PSD2', 'PSD3', 'Fm', 'PSD5', 'PSD6']
    assert all(a == b for a, b in zip(ps.ojip_dark.coords['frame_label'].to_dict()['data'], true_labels))

    # Create dataset with only 3 frames
    cache_dir = os.path.join(tmpdir, "sub")
    shutil.copytree(os.path.dirname(photosynthesis_test_data.cropreporter_v653), cache_dir)
    inffilename = os.path.join(cache_dir, photosynthesis_test_data.cropreporter_v653.split(os.sep)[-1])

    # Modify the inf file
    metadata_dict = {}
    with open(inffilename, "r") as fp:
        for line in fp:
            if "=" in line:
                key, value = line.rstrip("\n").split("=")
                metadata_dict[key] = value
    metadata_dict['SaveAllFrames'] = 0
    new_text = ""
    for key, value in metadata_dict.items():
        new_text = new_text + f"{key}={value}\n"
    with open(inffilename, "w") as fp:
        fp.writelines(new_text)
    # run test
    ps = read_cropreporter(filename=inffilename)
    # check labels
    true_dark_labels = ['Fdark', 'F0', 'Fm', 'PSD3', 'PSD4', 'PSD5', 'PSD6']
    assert all(a == b for a, b in zip(ps.ojip_dark.coords['frame_label'].to_dict()['data'], true_dark_labels))
    true_light_labels = ['Flight', 'Fp', 'Fmp', 'PSL3', 'PSL4', 'PSL5', 'PSL6']
    assert all(a == b for a, b in zip(ps.ojip_light.coords['frame_label'].to_dict()['data'], true_light_labels))
    true_pam_dark_labels = ["Fdark", "F0", "Fm", "Fdarksat"]
    assert all(a == b for a, b in zip(ps.pam_dark.coords['frame_label'].to_dict()['data'], true_pam_dark_labels))
    true_pam_light_labels = ["Flight", "Fp", "Fmp", "Flightsat"]
    assert all(a == b for a, b in zip(ps.pam_light.coords['frame_label'].to_dict()['data'], true_pam_light_labels))


def test_read_cropreporter_spc_only(photosynthesis_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only SPC
    shutil.copyfile(photosynthesis_test_data.cropreporter, os.path.join(cache_dir, "PSII_HDR_test.INF"))
    spc_dat = photosynthesis_test_data.cropreporter.replace("HDR", "SPC")
    spc_dat = spc_dat.replace("INF", "DAT")
    shutil.copyfile(spc_dat, os.path.join(cache_dir, "PSII_SPC_test.DAT"))
    fluor_filename = os.path.join(cache_dir, "PSII_HDR_test.INF")
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data) and ps.spectral.array_data.shape == (966, 1296, 3)


def test_read_cropreporter_npq(photosynthesis_test_data, tmpdir):
    """Test for PlantCV."""
    ps = read_cropreporter(filename=photosynthesis_test_data.cropreporter_npq)
    assert isinstance(ps, PSII_data) and ps.ojip_dark.shape == (966, 1296, 3, 1)
    assert isinstance(ps, PSII_data) and ps.ojip_light.shape == (966, 1296, 3, 1)


def test_read_cropreporter_gfp_only(photosynthesis_test_data, tmpdir):
    """Test GFP import."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only GFP
    shutil.copyfile(photosynthesis_test_data.cropreporter_gfp, os.path.join(cache_dir, "HDR_DYSeed_20251222191634684.INF"))
    gfp_dat = photosynthesis_test_data.cropreporter_gfp.replace("HDR", "GFP")
    gfp_dat = gfp_dat.replace("INF", "DAT")
    shutil.copyfile(gfp_dat, os.path.join(cache_dir, "GFP_DYSeed_20251222191634684.DAT"))
    fluor_filename = os.path.join(cache_dir, "HDR_DYSeed_20251222191634684.INF")
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data)
    assert ps.gfp is not None
    # (rows, cols, frames)
    assert ps.gfp.shape[2] in [2, 3]


def test_read_cropreporter_rfp_only(photosynthesis_test_data, tmpdir):
    """Test RFP import."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only RFP
    shutil.copyfile(photosynthesis_test_data.cropreporter_rfp, os.path.join(cache_dir, "HDR_DYSeed_20251222191634684.INF"))
    rfp_dat = photosynthesis_test_data.cropreporter_rfp.replace("HDR", "RFP")
    rfp_dat = rfp_dat.replace("INF", "DAT")
    shutil.copyfile(rfp_dat, os.path.join(cache_dir, "RFP_DYSeed_20251222191634684.DAT"))
    fluor_filename = os.path.join(cache_dir, "HDR_DYSeed_20251222191634684.INF")
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data)
    assert ps.rfp is not None
    assert ps.rfp.shape[2] in [1, 2]


def test_read_cropreporter_aph_only(photosynthesis_test_data, tmpdir):
    """Test APH (Red / FarRed reflectance) import."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only APH
    shutil.copyfile(photosynthesis_test_data.cropreporter_aph, os.path.join(cache_dir,
                                                                            "HDR_2025-12-12_tob1_20251212205712029.INF"))
    aph_dat = photosynthesis_test_data.cropreporter_aph.replace("HDR", "APH")
    aph_dat = aph_dat.replace("INF", "DAT")
    shutil.copyfile(aph_dat, os.path.join(cache_dir, "APH_2025-12-12_tob1_20251212205712029.DAT"))
    fluor_filename = os.path.join(cache_dir, "HDR_2025-12-12_tob1_20251212205712029.INF")
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data)
    assert ps.aph is not None
    assert ps.aph.shape[2] == 2  # Red + FarRed


def test_read_cropreporter_pmt_only(photosynthesis_test_data, tmpdir):
    """Test PMT (PAM Time) import."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only PMT
    shutil.copyfile(photosynthesis_test_data.cropreporter_pmt, os.path.join(cache_dir,
                                                                            "HDR_E0001P0008N0001_GCU24100090_20260226.INF"))
    pmt_dat = photosynthesis_test_data.cropreporter_pmt.replace("HDR", "PMT")
    pmt_dat = pmt_dat.replace("INF", "DAT")
    shutil.copyfile(pmt_dat, os.path.join(cache_dir, "PMT_E0001P0007N0001_GCU24100090_20260226.DAT"))
    fluor_filename = os.path.join(cache_dir, "HDR_E0001P0008N0001_GCU24100090_20260226.INF")
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data)
    assert ps.pam_time is not None
    # Check that dimensions include x, y, frame_label, and measurement
    assert "frame_label" in ps.pam_time.coords
    assert "measurement" in ps.pam_time.coords
    
    # Verify the shape (x, y, 9 or 13 labels, N measurements)
    # The 9 or 13 comes from 'frame_labels' list in read_cropreporter.py, and depends on the presence of second dark adaptation
    num_labels = len(ps.pam_time.frame_label)
    assert num_labels in [9, 13]

    # If Fdarkpp exists, we must have 13 labels
    if "Fdarkpp" in ps.pam_time.frame_label.values:
        assert num_labels == 13
    else:
        assert num_labels == 9
    
    # Check that at least one measurement label was created (t0, t1...)
    assert "t0" in ps.pam_time.measurement.values
    
    # Access a value to ensure the loops actually ran
    # This forces the test to "touch" the data assigned inside the loops
    assert ps.pam_time.sel(frame_label="Fdark", measurement="t0").any()
    
    # Verify the F0p (the very last line of your function)
    assert "F0p" in ps.pam_time.frame_label.values