import pytest
import os
import matplotlib

# Disable plotting
matplotlib.use("Template")


class HyperspectralTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "testdata")


@pytest.fixture(scope="session")
def hyperspectral_test_data():
    return HyperspectralTestData()
