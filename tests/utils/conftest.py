import pytest
import os


class UtilsTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "testdata")
        # PlantCV results file
        self.plantcv_results_file = os.path.join(self.datadir, "plantcv_results.json")
        # Invalid results file
        self.invalid_results_file = os.path.join(self.datadir, "invalid_results.json")
        # Snapshot image directory
        self.snapshot_imgdir = os.path.join(self.datadir, "snapshot_imgdir")
        # Flat image directory
        self.flat_imgdir = os.path.join(self.datadir, "flat_imgdir")
        # Phenodata directory
        self.phenodata_dir = os.path.join(self.datadir, "phenodata_dir")
        # ImageJ Pixel Inspector sampled RGB values
        self.rgb_values_file = os.path.join(self.datadir, "pixel_inspector_rgb_values.txt")


@pytest.fixture(scope="session")
def utils_test_data():
    """Test data object for the PlantCV utils submodule."""
    return UtilsTestData()
