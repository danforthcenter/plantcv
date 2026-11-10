import os
import pytest
import numpy as np
from plantcv.plantcv._globals import params
from plantcv.plantcv.hyperspectral import read_data
from tests import synthetic


def test_read_data_default(tmpdir):
    """Test for PlantCV."""
    filename = synthetic.write_envi(outdir=tmpdir, filename="default", default_bands="0,2,4")
    array_data = read_data(filename=filename)
    assert np.array_equal(array_data.array_data, synthetic.envi_array())
    assert array_data.default_bands == ["0", "2", "4"]
    # making an example of wavelengths not covering expected pseudo RGB range
    array_data.default_bands = None
    array_data.wavelength_dict = {k: k for k in range(495, 500)}
    ps = array_data.pseudo_rgb()
    assert np.shape(ps) == (2, 3, 3)


def test_read_data_default_bands(tmpdir):
    """Test for PlantCV."""
    # No default bands, no wavelength units, and every band at the same wavelength
    filename = synthetic.write_envi(outdir=tmpdir, filename="no_default", wavelengths=[513.342] * 5,
                                    wavelength_units=None)
    array_data = read_data(filename=filename)
    ps = array_data.pseudo_rgb()
    assert np.array_equal(array_data.array_data, synthetic.envi_array())
    assert array_data.wavelength_units == "nm"
    assert len(np.shape(ps)) == 3


def test_read_data_approx_pseudo_rgb(tmpdir):
    """Test for PlantCV."""
    # No default bands, and wavelengths that span the blue, green and red pseudo-rgb targets
    filename = synthetic.write_envi(outdir=tmpdir, filename="approx", wavelengths=[450, 500, 550, 600, 650])
    array_data = read_data(filename=filename)
    assert np.array_equal(array_data.array_data, synthetic.envi_array())
    assert np.shape(array_data.pseudo_rgb()) == (2, 3, 3)


def test_read_data_one_default_band(tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    filename = synthetic.write_envi(outdir=cache_dir, filename="one_band", default_bands="2")
    debug_outdir = params.debug_outdir
    default_debug = params.debug
    params.debug_outdir = str(cache_dir)
    params.debug = "plot"
    array_data = read_data(filename=filename)
    params.debug_outdir = debug_outdir
    params.debug = default_debug
    # One default band is repeated in each channel, so the pseudo-rgb image is grayscale
    ps = array_data.pseudo_rgb()
    assert np.array_equal(ps[:, :, 0], ps[:, :, 1]) and np.array_equal(ps[:, :, 1], ps[:, :, 2])


def test_read_data_two_default_bands(tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    filename = synthetic.write_envi(outdir=cache_dir, filename="two_bands", default_bands="1,3")
    obj = read_data(filename=filename)
    with pytest.raises(RuntimeError):
        _ = obj.pseudo_rgb()


def test_read_data_empty_default_bands(tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    filename = synthetic.write_envi(outdir=cache_dir, filename="empty_bands", default_bands="")
    array_data = read_data(filename=filename)
    assert array_data.default_bands is None


def test_read_data_out_of_range_default_bands(tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    filename = synthetic.write_envi(outdir=cache_dir, filename="bad_bands", default_bands="700")
    obj = read_data(filename=filename)
    with pytest.raises(RuntimeError):
        _ = obj.pseudo_rgb()


def test_read_data_bad_interleave(tmpdir):
    """Test for PlantCV."""
    filename = synthetic.write_envi(outdir=tmpdir, filename="bad_interleave", interleave="bup")
    with pytest.raises(RuntimeError):
        _ = read_data(filename=filename)


def test_read_data_bad_filename(tmpdir):
    """Test for PlantCV."""
    # No header file exists for this name
    with pytest.raises(RuntimeError):
        _ = read_data(filename=os.path.join(str(tmpdir), "missing"))


def test_read_data_parse_arcgis(tmpdir):
    """Test for PlantCV."""
    filename = synthetic.write_arcgis(outdir=tmpdir, filename="arcgis")
    array_data = read_data(filename=filename, mode="arcgis")
    assert np.array_equal(array_data.array_data, synthetic.envi_array())
    assert list(array_data.wavelength_dict) == [500.0, 550.0, 600.0, 650.0, 700.0]
