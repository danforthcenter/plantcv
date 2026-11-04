import pytest
import os
import numpy as np
import matplotlib

# Disable plotting
matplotlib.use("Template")


class TransformTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "testdata")
        # Checkerboard image directory
        self.checkerboard_imgdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                "..", "..", "testdata", "checkerboard_imgdir")
        # Fish eye image
        self.fisheye_test_img = os.path.join(self.datadir, "fisheye_test_img.jpg")
        # mtx matrix
        self.mtx = os.path.join(self.datadir, "mtx.npz")
        # dist matrix
        self.dist = os.path.join(self.datadir, "dist.npz")

    @staticmethod
    def load_npz(npz_file):
        """Load data saved in a NumPy .npz file."""
        data = np.load(npz_file, encoding="latin1")
        return data['arr_0']


@pytest.fixture(scope="session")
def transform_test_data():
    """Test data object for the PlantCV transform submodule."""
    return TransformTestData()
