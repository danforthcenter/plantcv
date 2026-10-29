import pytest
import numpy as np
from plantcv.plantcv._globals import params
from plantcv.plantcv.hyperspectral import read_data
from tests import synthetic


def test_read_data_default(hyperspectral_test_data):
    """Test for PlantCV."""
    array_data = read_data(filename=hyperspectral_test_data.envi_bil_file)
    # making an example of wavelengths not covering expected pseudo RGB range
    array_data.default_bands = None
    array_data.wavelength_dict = {k: k for k in range(491, 500)}
    ps = array_data.pseudo_rgb()
    assert np.shape(array_data.array_data) == (1, 1600, 978)
    assert len(np.shape(ps)) == 3


def test_read_data_default_bands(hyperspectral_test_data):
    """Test for PlantCV."""
    array_data = read_data(filename=hyperspectral_test_data.envi_no_default)
    ps = array_data.pseudo_rgb()
    assert np.shape(array_data.array_data) == (1, 1600, 978)
    assert len(np.shape(ps)) == 3


def test_read_data_approx_pseudo_rgb(hyperspectral_test_data):
    """Test for PlantCV."""
    array_data = read_data(filename=hyperspectral_test_data.envi_appox_pseudo)
    assert np.shape(array_data.array_data) == (1, 1600, 978)


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


def test_read_data_bad_interleave(hyperspectral_test_data):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = read_data(filename=hyperspectral_test_data.envi_bad_interleave)


def test_read_data_bad_filename(hyperspectral_test_data):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = read_data(filename=hyperspectral_test_data.bad_filename)


def test_read_data_parse_arcgis(hyperspectral_test_data):
    """Test for PlantCV."""
    array_data = read_data(filename=hyperspectral_test_data.arcgis, mode="arcgis")
    assert np.shape(array_data.array_data) == (1, 1600, 978)
