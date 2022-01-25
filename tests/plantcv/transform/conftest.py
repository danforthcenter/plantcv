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
        # RGB image
        self.small_rgb_img = os.path.join(self.datadir, "setaria_small_plant_rgb.png")
        # Gray image
        self.small_gray_img = os.path.join(self.datadir, "setaria_small_plant_gray.png")
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
        # Source 2 RGB image
        self.source2_img = os.path.join(self.datadir, "source2_img.png")
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
        # Color card image
        self.colorcard_img = os.path.join(self.datadir, "colorcard_img.png")

    @staticmethod
    def create_test_img(sz_img):
        """Create a test image."""
        img = np.random.randint(np.prod(sz_img), size=sz_img) * 255
        img = img.astype(np.uint8)
        return img

    @staticmethod
    def create_test_img_bin(sz_img):
        """Create a test binary image."""
        img = np.zeros(sz_img)
        img[3:7, 2:8] = 1
        return img

    @staticmethod
    def load_npz(npz_file):
        """Load data saved in a NumPy .npz file."""
        data = np.load(npz_file, encoding="latin1")
        return data['arr_0']


@pytest.fixture(scope="session")
def transform_test_data():
    """Test data object for the PlantCV transform submodule."""
    return TransformTestData()
