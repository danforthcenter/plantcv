import pytest
import os
import matplotlib
import pickle as pkl

# Disable plotting
matplotlib.use("Template")


class SpectralIndexTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "testdata")
        self.hsi_file = os.path.join(self.datadir, "hsi.pkl")
        self.small_rgb_img = os.path.join(self.datadir, "setaria_small_plant_rgb.png")

    def load_hsi(self):
        """Load PlantCV Spectral_data pickled object."""
        with open(self.hsi_file, "rb") as fp:
            return pkl.load(fp)


@pytest.fixture(scope="session")
def spectral_index_test_data():
    """Test data object for the PlantCV spectral_index submodule."""
    return SpectralIndexTestData()
