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
        self.small_rgb_img = os.path.join(self.datadir, "setaria_small_rgb_img.png")
        # Binary mask for RGB image
        self.small_bin_img = os.path.join(self.datadir, "setaria_small_bin_img.png")
        # Gray image
        self.small_gray_img = os.path.join(self.datadir, "setaria_small_gray_img.png")
        # PlantCV Spectral_data object
        self.hsi_file = os.path.join(self.datadir, "hsi.pkl")
        # Binary mask for HSI
        self.hsi_mask_file = os.path.join(self.datadir, "hsi_mask.png")
        # Outputs results file - JSON
        self.outputs_results_json = os.path.join(self.datadir, "outputs_results.json")
        # Outputs results file - CSV
        self.outputs_results_csv = os.path.join(self.datadir, "outputs_results.csv")
        # RGBA image
        # Image from http://www.libpng.org/pub/png/png-OwlAlpha.html
        # This image may be used, edited and reproduced freely.
        self.rgba_img = os.path.join(self.datadir, "owl_rgba_img.png")
        # ENVI hyperspectral data
        self.envi_bil_file = os.path.join(self.datadir, "darkReference")
        # Thermal image
        self.thermal_img = os.path.join(self.datadir, "FLIR2600.csv")
        # Bayer image
        self.bayer_img = os.path.join(self.datadir, "bayer_img.png")

    def load_hsi(self, pkl_file):
        """Load PlantCV Spectral_data pickled object."""
        with open(pkl_file, "rb") as fp:
            return pkl.load(fp)


@pytest.fixture(scope="session")
def test_data():
    return TestData()
