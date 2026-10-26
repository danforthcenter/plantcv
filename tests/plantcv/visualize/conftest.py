import pytest
import os
import matplotlib
import pickle as pkl

# Disable plotting
matplotlib.use("Template")


class VisualizeTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "testdata")
        # PlantCV hyperspectral image object
        self.hsi_file = os.path.join(self.datadir, "hsi.pkl")

    @staticmethod
    def load_hsi(pkl_file):
        """Load PlantCV Spectral_data pickled object."""
        with open(pkl_file, "rb") as fp:
            return pkl.load(fp)


@pytest.fixture(scope="session")
def visualize_test_data():
    """Test data object for the PlantCV visualize submodule."""
    return VisualizeTestData()
