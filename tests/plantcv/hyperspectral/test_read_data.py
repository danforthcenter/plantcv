import pytest
import numpy as np
from plantcv.plantcv.hyperspectral import read_data


def test_read_data_default(hyperspectral_test_data):
    """Test for PlantCV."""
    array_data = read_data(filename=hyperspectral_test_data.envi_bil_file)
    assert np.shape(array_data.array_data) == (1, 1600, 978)


def test_read_data_default_bands(hyperspectral_test_data):
    """Test for PlantCV."""
    array_data = read_data(filename=hyperspectral_test_data.envi_no_default)
    assert np.shape(array_data.array_data) == (1, 1600, 978)


def test_read_data_approx_pseudorgb(hyperspectral_test_data):
    """Test for PlantCV."""
    array_data = read_data(filename=hyperspectral_test_data.envi_appox_pseudo)
    assert np.shape(array_data.array_data) == (1, 1600, 978)


def test_read_data_one_default_band(hyperspectral_test_data, tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    filename = hyperspectral_test_data.create_envi_data(outdir=cache_dir, filename="one_band", default_bands="2")
    array_data = read_data(filename=filename)
    # One default band is repeated in each channel, so the pseudo-rgb image is grayscale
    assert np.array_equal(array_data.pseudo_rgb[:, :, 0], array_data.pseudo_rgb[:, :, 1]) and \
        np.array_equal(array_data.pseudo_rgb[:, :, 1], array_data.pseudo_rgb[:, :, 2])


def test_read_data_two_default_bands(hyperspectral_test_data, tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    filename = hyperspectral_test_data.create_envi_data(outdir=cache_dir, filename="two_bands", default_bands="1,3")
    with pytest.raises(RuntimeError):
        _ = read_data(filename=filename)


def test_read_data_empty_default_bands(hyperspectral_test_data, tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    filename = hyperspectral_test_data.create_envi_data(outdir=cache_dir, filename="empty_bands", default_bands="")
    array_data = read_data(filename=filename)
    assert array_data.default_bands is None


def test_read_data_out_of_range_default_bands(hyperspectral_test_data, tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    filename = hyperspectral_test_data.create_envi_data(outdir=cache_dir, filename="bad_bands", default_bands="700")
    with pytest.raises(RuntimeError):
        _ = read_data(filename=filename)


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
