import os
import pytest
import numpy as np

from plantcv.plantcv import Spectral_data
from plantcv.plantcv.hyperspectral import read_data
from plantcv.plantcv.hyperspectral import write_data

def test_write_data_default(tmpdir):
    """Test for PlantCV."""
    rng = np.random.default_rng()

    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")

    lines = 32
    samples = 32
    bands = 5

    # Create random array data in the interval [0-65535] and wavelengths in the
    # interval [400-1000)
    rand_array = rng.integers(0, 65535, size=(lines, samples, bands), dtype=np.uint16, endpoint=True)
    rand_wavelengths = np.sort(600.0*rng.random(size=bands) + 400.0)
    # Create dictionary of wavelengths
    wavelength_dict = {}
    for j, wavelength in enumerate(rand_wavelengths):
        wavelength_dict.update({wavelength: float(j)})

    # Create spectral data object
    rand_spectral_array = Spectral_data(array_data=rand_array,
                                max_wavelength=rand_wavelengths[-1],
                                min_wavelength=rand_wavelengths[0],
                                max_value=float(np.amax(rand_array)),
                                min_value=float(np.amin(rand_array)),
                                d_type=rand_array.dtype,
                                wavelength_dict=wavelength_dict,
                                samples=samples,
                                lines=lines,
                                interleave='bil',
                                wavelength_units='nm',
                                array_type="datacube",
                                pseudo_rgb=None,
                                filename='random_hyperspectral_test',
                                default_bands=[0,1,2])


    filename = os.path.join(cache_dir, 'plantcv_hyperspectral_write_data.raw')
    write_data(filename=filename, spectral_data=rand_spectral_array)

    # Read written hyperspectral image
    array_data = read_data(filename=filename)
    assert np.shape(array_data.array_data) == (lines, samples, bands)
