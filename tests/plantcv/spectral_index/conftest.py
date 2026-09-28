import os
import pytest
import matplotlib
import numpy as np
import pickle as pkl
from plantcv.plantcv.classes import MS_data

# Disable plotting
matplotlib.use("Template")


class ms_data_object:
    def __init__(self):
        array_data=None
    def make_array(self, wavelengths):
        """Make an MS data object on the fly"""
        array_data = np.stack([np.ones((10, 10)) for i in wavelengths], axis=-1)
        wavelength_dict = {k: i for i, k in enumerate(wavelengths)}
        self.array_data = MS_data(array_data=array_data, wavelength_dict=wavelength_dict,
                                  max_wavelength=max(wavelengths),
                                  min_wavelength=min(wavelengths),
                                  pseudo_rgb=None, filename="test")
        return self.array_data


class SpectralIndexTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "testdata")
        self.hsi_file = os.path.join(self.datadir, "hsi.pkl")
        self.small_rgb_img = os.path.join(self.datadir, "setaria_small_plant_rgb.png")
        self.ms_data = ms_data_object()

    def load_hsi(self):
        """Load PlantCV Spectral_data pickled object."""
        with open(self.hsi_file, "rb") as fp:
            return pkl.load(fp)




        
@pytest.fixture(scope="session")
def spectral_index_test_data():
    """Test data object for the PlantCV spectral_index submodule."""
    return SpectralIndexTestData()
