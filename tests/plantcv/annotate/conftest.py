import pytest
import os
import matplotlib

# Disable plotting
matplotlib.use("Template")


class AnnotateTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "testdata")
        # RGB image
        self.small_rgb_img = os.path.join(self.datadir, "setaria_small_plant_rgb.png")
        # Disc image mask
        self.discs_mask = os.path.join(self.datadir, "discs_binary.png")
        # Clickcount_correct image masks
        self.pollen = os.path.join(self.datadir, "crop_pollen.png")
        self.pollen_all = os.path.join(self.datadir, "pollen_all_mask.png")
        self.pollen_discs = os.path.join(self.datadir, "pollen_detectdisc_mask.png")
        self.pollen_watershed = os.path.join(self.datadir, "pollen_watershed.png")
        self.pollen_recovered = os.path.join(self.datadir, "pollen_recovered.png")


@pytest.fixture(scope="session")
def annotate_test_data():
    """Test data object for the PlantCV annotate submodule."""
    return AnnotateTestData()
