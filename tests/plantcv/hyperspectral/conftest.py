import pytest
import os
import matplotlib

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


@pytest.fixture(scope="session")
def hyperspectral_test_data():
    return HyperspectralTestData()
