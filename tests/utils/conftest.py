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


@pytest.fixture(scope="session")
def utils_test_data():
    return UtilsTestData()
