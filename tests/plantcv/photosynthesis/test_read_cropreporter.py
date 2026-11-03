"""Tests for plantcv.photosynthesis.read_cropreporter."""
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


def test_read_cropreporter_pmd(tmp_path):
    """Test for PlantCV."""
    filename = synthetic.write_cropreporter(tmp_path, "v653", ["PMD"])
    ps = read_cropreporter(filename=filename)
    assert isinstance(ps, PSII_data)
    assert ps.pmd.pam_dark.shape == (10, 12, 4, 1)
    assert list(ps.pmd.pam_dark.frame_label.values) == ["Fdark", "F0", "Fm", "Fdarksat"]
    assert np.all(ps.pmd.pam_dark.values == np.array([10, 300, 1000, 500])[:, None])
    assert ps.pmd
    assert "PMD" in repr(ps.pmd)


def test_read_cropreporter_pml(tmp_path):
    """Test for PlantCV."""
    filename = synthetic.write_cropreporter(tmp_path, "v653", ["PML"])
    ps = read_cropreporter(filename=filename)
    assert isinstance(ps, PSII_data)
    assert ps.pml.pam_light.shape == (10, 12, 4, 1)
    assert list(ps.pml.pam_light.frame_label.values) == ["Flight", "Fp", "Fmp", "Flightsat"]
    assert np.all(ps.pml.pam_light.values == np.array([20, 150, 250, 200])[:, None])
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


def test_read_cropreporter_gfp_only(tmp_path):
    """Test GFP import."""
    fluor_filename = synthetic.write_cropreporter(tmp_path, "gfp", ["GFP"])
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data)
    assert ps.gfp
    assert "GFP" in repr(ps.gfp)
    assert ps.gfp.green is not None
    # (rows, cols, frames)
    assert len(ps.gfp.green.shape) == 2
    # GFP is the second to last frame
    assert ps.gfp.green.shape == (10, 12)
    assert np.all(ps.gfp.green == 700)
    # reach other attribute first
    ps = read_cropreporter(filename=fluor_filename)
    assert ps.gfp.auto is not None
    # autofluorescence is the last frame
    assert np.all(ps.gfp.auto == 90)


def test_read_cropreporter_rfp_only(tmp_path):
    """Test RFP import."""
    fluor_filename = synthetic.write_cropreporter(tmp_path, "gfp", ["RFP"])
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data)
    assert ps.rfp
    assert "RFP" in repr(ps.rfp)
    assert ps.rfp.red is not None
    assert len(ps.rfp.red.shape) == 2
    # RFP is the last frame
    assert ps.rfp.red.shape == (10, 12)
    assert np.all(ps.rfp.red == 650)


def test_read_cropreporter_aph_only(tmp_path):
    """Test APH (Red / FarRed reflectance) import."""
    fluor_filename = synthetic.write_cropreporter(tmp_path, "aph", ["APH"])
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data)
    assert ps.aph
    assert "loaded=False" in repr(ps.aph)
    assert hasattr(ps.aph, "red")
    assert hasattr(ps.aph, "farred")
    # red is the second to last frame and far-red the last
    assert np.all(ps.aph.red == 600)
    assert np.all(ps.aph.farred == 800)


def test_read_cropreporter_aph_farred(tmp_path):
    """Test APH (Red / FarRed reflectance) import."""
    fluor_filename = synthetic.write_cropreporter(tmp_path, "aph", ["APH"])
    ps = read_cropreporter(filename=fluor_filename)
    assert hasattr(ps.aph, "farred")
    assert np.all(ps.aph.farred == 800)
    assert np.all(ps.aph.red == 600)


def test_read_cropreporter_pmt_only_9_labels(tmp_path):
    """Test PMT (PAM Time) import with 9 frames."""
    fluor_filename = synthetic.write_cropreporter(tmp_path, "pmt", ["PMT"])
    ps = read_cropreporter(filename=fluor_filename)
    assert isinstance(ps, PSII_data)
    assert ps.pmt.pam_time is not None
    assert ps.pmt
    assert "PMT" in repr(ps.pmt)
    # Check that dimensions include x, y, frame_label, and measurement
    assert "frame_label" in ps.pmt.pam_time.coords
    assert "measurement" in ps.pmt.pam_time.coords

    # Verify the shape (x, y, 9 labels, N measurements)
    # The 9 or 13 comes from 'frame_labels' list in read_cropreporter.py, and depends on the presence of second dark
    # adaptation
    num_labels = len(ps.pmt.pam_time.frame_label)
    assert num_labels == 9
    assert list(ps.pmt.pam_time.frame_label.values) == ["Fdark", "F0", "Fm", "Fdarksat",
                                                        "Flight", "Fp", "Fmp", "Flightsat", "F0p"]

    # TmPamMeasFvfm=1 and TmPamMeasFqfm=1 give one dark-adapted and one light-adapted measurement
    assert "t0" in ps.pmt.pam_time.measurement.values
    assert list(ps.pmt.pam_time.measurement.values) == ["t0", "t1"]

    # Access a value to ensure the loops actually ran
    # This forces the test to "touch" the data assigned inside the loops
    assert ps.pmt.pam_time.sel(frame_label="Fdark", measurement="t0").values.any()
    # Each frame is stored in its own measurement and the rest are zero; F0p goes in the last measurement
    pam_time = ps.pmt.pam_time
    assert np.all(pam_time.sel(measurement="t0").values == [10, 300, 1000, 500, 0, 0, 0, 0, 0])
    assert np.all(pam_time.sel(measurement="t1").values == [0, 0, 0, 0, 20, 150, 250, 200, 125])

    # Verify the F0p (the very last line of your function)
    assert "F0p" in ps.pmt.pam_time.frame_label.values


def test_read_cropreporter_pmt_only_13_labels(tmp_path):
    """Test PMT (PAM Time) import with 13 frames."""
    # TmPamMeasFvfm=3 adds two measurements of the second dark adaptation (17 frames)
    inf_dest = synthetic.write_cropreporter(tmp_path, "pmt", {"PMT": synthetic.pmt_frames(n_fvfm=2)},
                                            metadata={"TmPamMeasFvfm": 3})

    ps = read_cropreporter(filename=inf_dest)
    assert isinstance(ps, PSII_data)
    assert ps.pmt.pam_time is not None
    assert ps.pmt
    assert "PMT" in repr(ps.pmt)
    # Check that dimensions include x, y, frame_label, and measurement
    assert "frame_label" in ps.pmt.pam_time.coords
    assert "measurement" in ps.pmt.pam_time.coords

    # Verify the shape (x, y, 13 labels, N measurements)
    # The 9 or 13 comes from 'frame_labels' list in read_cropreporter.py, and depends on the presence of second dark
    # adaptation
    num_labels = len(ps.pmt.pam_time.frame_label)
    assert num_labels == 13
    assert list(ps.pmt.pam_time.frame_label.values) == ["Fdark", "F0", "Fm", "Fdarksat",
                                                        "Flight", "Fp", "Fmp", "Flightsat",
                                                        "Fdarkpp", "F0pp", "Fmpp", "Fdarksatpp", "F0p"]

    # Check that at least one measurement label was created (t0, t1...)
    assert "t0" in ps.pmt.pam_time.measurement.values
    assert list(ps.pmt.pam_time.measurement.values) == ["t0", "t1", "t2", "t3"]

    # Access a value to ensure the loops actually ran
    # This forces the test to "touch" the data assigned inside the loops
    assert ps.pmt.pam_time.sel(frame_label="Fdark", measurement="t0").values.any()
    pam_time = ps.pmt.pam_time
    assert np.all(pam_time.sel(measurement="t0").values == [10, 300, 1000, 500] + [0] * 9)
    assert np.all(pam_time.sel(measurement="t1").values == [0] * 4 + [20, 150, 250, 200] + [0] * 5)
    assert np.all(pam_time.sel(measurement="t2").values == [0] * 8 + [15, 280, 800, 400, 0])
    assert np.all(pam_time.sel(measurement="t3").values == [0] * 8 + [15, 280, 800, 400, 125])

    # Verify the F0p (the very last line of your function)
    assert "F0p" in ps.pmt.pam_time.frame_label.values
