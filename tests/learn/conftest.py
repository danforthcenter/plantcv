import pytest
import os
import matplotlib

# Disable plotting
matplotlib.use("Template")


class LearnTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "testdata")
        # RGB image
        self.small_rgb_img = os.path.join(self.datadir, "setaria_small_rgb_img.png")
        # Binary mask
        self.small_bin_img = os.path.join(self.datadir, "setaria_small_bin_img.png")
        # RGB values table
        self.rgb_values_table = os.path.join(self.datadir, "rgb_values_table.txt")


@pytest.fixture(scope="session")
def learn_test_data():
    return LearnTestData()
