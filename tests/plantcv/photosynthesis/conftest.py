import pytest
import os
import matplotlib

# Disable plotting
matplotlib.use("Template")


class PhotosynthesisTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "testdata")
        # CropReporter data file
        self.cropreporter = os.path.join(self.datadir, "PSII_PSD_supopt_temp_btx623_22_rep1.DAT")
        # Fdark image
        self.fdark = os.path.join(self.datadir, "FLUO_TV_dark.png")
        # Fmin image
        self.fmin = os.path.join(self.datadir, "FLUO_TV_min.png")
        # Fmax image
        self.fmax = os.path.join(self.datadir, "FLUO_TV_max.png")
        # Mask image
        self.ps_mask = os.path.join(self.datadir, "FLUO_TV_MASK.png")


@pytest.fixture(scope="session")
def photosynthesis_test_data():
    """Test data object for the PlantCV photosynthesis submodule."""
    return PhotosynthesisTestData()
