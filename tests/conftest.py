import pytest
import os
import pickle as pkl
import matplotlib

# Disable plotting
matplotlib.use("Template")


class TestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testdata")
        # RGB image
        self.camelina_rgb_img = os.path.join(self.datadir, "camelina_rgb_img.jpg")
        # Binary mask for RGB image
        self.camelina_bin_img = os.path.join(self.datadir, "camelina_bin_img.png")
        # Gray image
        self.camelina_gray_img = os.path.join(self.datadir, "camelina_gray_img.jpg")
        # PlantCV Spectral_data object
        self.hsi_file = os.path.join(self.datadir, "hsi.pkl")
        # Binary mask for HSI
        self.hsi_mask_file = os.path.join(self.datadir, "hsi_mask.png")
        # Outputs results file - JSON
        self.outputs_results_json = os.path.join(self.datadir, "outputs_results.json")
        # Outputs results file - CSV
        self.outputs_results_csv = os.path.join(self.datadir, "outputs_results.csv")

    def load_hsi(self, pkl_file):
        """Load PlantCV Spectral_data pickled object."""
        with open(pkl_file, "rb") as fp:
            return pkl.load(fp)


@pytest.fixture(scope="session")
def test_data():
    return TestData()
