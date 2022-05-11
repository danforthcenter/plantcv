import pytest
import os
import matplotlib

# Disable plotting
matplotlib.use("Template")


class ThresholdTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "testdata")
        # RGB image
        self.small_rgb_img = os.path.join(self.datadir, "setaria_small_plant_rgb.png")
        # Gray image
        self.small_gray_img = os.path.join(self.datadir, "setaria_small_plant_gray.png")


@pytest.fixture(scope="session")
def threshold_test_data():
    """Test data object for the PlantCV threshold submodule."""
    return ThresholdTestData()
