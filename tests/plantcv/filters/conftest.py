import pytest
import os
import matplotlib

# Disable plotting
matplotlib.use("Template")


class FiltersTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "testdata")
        # Binary mask for eccentricity filter
        self.small_bin_fill = os.path.join(self.datadir, "floodfill.png")
        # Binary mask for object filter
        self.barley_example = os.path.join(self.datadir, "example_barley_mask.png")


@pytest.fixture(scope="session")
def filters_test_data():
    """Test data object for the PlantCV filter submodule."""
    return FiltersTestData()
