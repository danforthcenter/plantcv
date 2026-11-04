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
        # Target RGB image
        self.target_img = os.path.join(self.datadir, "target_img.png")
        # Target matrix file
        self.target_matrix_file = os.path.join(self.datadir, "target_matrix.npz")
        # Color card mask
        self.colorcard_mask = os.path.join(self.datadir, "colorcard_mask.png")
        # Source 1 RGB image
        self.source1_img = os.path.join(self.datadir, "source1_img.png")
        # Source 1 matrix file
        self.source1_matrix_file = os.path.join(self.datadir, "source1_matrix.npz")
        # Source 1 matrix file
        self.source2_matrix_file = os.path.join(self.datadir, "source2_matrix.npz")
        # Matrix M (source 1)
        self.matrix_m1_file = os.path.join(self.datadir, "matrix_m1.npz")
        # Matrix B (source 1)
        self.matrix_b1_file = os.path.join(self.datadir, "matrix_b1.npz")
        # Matrix M (source 2)
        self.matrix_m2_file = os.path.join(self.datadir, "matrix_m2.npz")
        # Matrix B (source 2)
        self.matrix_b2_file = os.path.join(self.datadir, "matrix_b2.npz")
        # Transformation matrix
        self.transformation_matrix_file = os.path.join(self.datadir, "transformation_matrix.npz")
        # Corrected source image
        self.source_corrected = os.path.join(self.datadir, "source_corrected.png")
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
