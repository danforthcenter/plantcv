import pytest
import os
import numpy as np
import matplotlib
import pickle as pkl

# Disable plotting
matplotlib.use("Template")


class VisualizeTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "testdata")
        # RGB image
        self.small_rgb_img = os.path.join(self.datadir, "setaria_small_plant_rgb.png")
        # Gray image
        self.small_gray_img = os.path.join(self.datadir, "setaria_small_plant_gray.png")
        # Binary mask for RGB image
        self.small_bin_img = os.path.join(self.datadir, "setaria_small_plant_mask.png")
        # Composed contours file
        self.small_composed_contours_file = os.path.join(self.datadir, "setaria_small_plant_composed_contours.npz")
        # PlantCV hyperspectral image object
        self.hsi_file = os.path.join(self.datadir, "hsi.pkl")

    @staticmethod
    def load_composed_contours(npz_file):
        """Load data saved in a NumPy .npz file."""
        data = np.load(npz_file, encoding="latin1")
        return data['contour']

    @staticmethod
    def load_hsi(pkl_file):
        """Load PlantCV Spectral_data pickled object."""
        with open(pkl_file, "rb") as fp:
            return pkl.load(fp)


@pytest.fixture(scope="session")
def visualize_test_data():
    """Test data object for the PlantCV visualize submodule."""
    return VisualizeTestData()
