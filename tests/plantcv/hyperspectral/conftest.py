import pytest
import os
import matplotlib
import pickle as pkl

# Disable plotting
matplotlib.use("Template")


class HyperspectralTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "testdata")
        self.envi_bil_file = os.path.join(self.datadir, "darkReference")
        self.envi_no_default = os.path.join(self.datadir, "darkReference2")
        self.envi_appox_pseudo = os.path.join(self.datadir, "darkReference3")
        self.envi_bad_interleave = os.path.join(self.datadir, "darkReference4")
        self.arcgis = os.path.join(self.datadir, "darkReference_arcgis")
        self.arcgis_hdr = os.path.join(self.datadir, "darkReference_arcgis.hdr")
        self.bad_filename = os.path.join(self.datadir, "darkReference0")
        self.hsi_file = os.path.join(self.datadir, "hsi.pkl")
        self.hsi_mask_file = os.path.join(self.datadir, "hsi_mask.png")
        self.hsi_whiteref_file = os.path.join(self.datadir, "hsi_whiteref.pkl")
        self.hsi_darkref_file = os.path.join(self.datadir, "hsi_darkref.pkl")
        self.savi_file = os.path.join(self.datadir, "savi.pkl")

    @staticmethod
    def load_hsi(pkl_file):
        """Load PlantCV Spectral_data pickled object."""
        with open(pkl_file, "rb") as fp:
            return pkl.load(fp)


@pytest.fixture(scope="session")
def hyperspectral_test_data():
    """Test data object for the PlantCV hyperspectral submodule."""
    return HyperspectralTestData()
