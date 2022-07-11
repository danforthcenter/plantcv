import pytest
import os
import numpy as np
import matplotlib

# Disable plotting
matplotlib.use("Template")


class RoiTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "testdata")
        # RGB image
        self.small_rgb_img = os.path.join(self.datadir, "setaria_small_plant_rgb.png")
        # Gray image
        self.small_gray_img = os.path.join(self.datadir, "setaria_small_plant_gray.png")
        # Contours file
        self.small_contours_file = os.path.join(self.datadir, "setaria_small_plant_contours.npz")
        # Grid image
        self.bin_grid_img = os.path.join(self.datadir, "brassica_2plants_bin_img.png")

    @staticmethod
    def load_contours(npz_file):
        """Load data saved in a NumPy .npz file."""
        data = np.load(npz_file, encoding="latin1")
        return data['contours'], data['hierarchy']


@pytest.fixture(scope="session")
def roi_test_data():
    """Test data object for the PlantCV roi submodule."""
    return RoiTestData()
