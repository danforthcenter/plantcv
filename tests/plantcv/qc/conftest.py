import pytest
import os
import numpy as np
import matplotlib

# Disable plotting
matplotlib.use("Template")


class QCTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "testdata")
        # Target matrix file
        self.target_matrix_file = os.path.join(self.datadir, "target_matrix.npz")
        # Source 1 matrix file
        self.source1_matrix_file = os.path.join(self.datadir, "source1_matrix.npz")

    @staticmethod
    def load_npz(npz_file):
        """Load data saved in a NumPy .npz file."""
        data = np.load(npz_file, encoding="latin1")
        return data['arr_0']


@pytest.fixture(scope="session")
def qc_test_data():
    """Test data object for the PlantCV transform submodule."""
    return QCTestData()
