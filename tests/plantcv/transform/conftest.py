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
        # Checkerboard image directory
        self.checkerboard_imgdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                "..", "..", "testdata", "checkerboard_imgdir")
        # Fish eye image
        self.fisheye_test_img = os.path.join(self.datadir, "fisheye_test_img.jpg")
        # mtx matrix
        self.mtx = os.path.join(self.datadir, "mtx.npz")
        # dist matrix
        self.dist = os.path.join(self.datadir, "dist.npz")
        # Merged image HS
        self.merged_HS = os.path.join(self.datadir, "merged_HS.jpg")
        # Merged image HA
        self.merged_HA = os.path.join(self.datadir, "merged_HA.jpg")
        # Merged image HG
        self.merged_HG = os.path.join(self.datadir, "merged_HG.jpg")
        # Merged image VS
        self.merged_VS = os.path.join(self.datadir, "merged_VS.jpg")
        # Merged image VA
        self.merged_VA = os.path.join(self.datadir, "merged_VA.jpg")
        # Merged image VG
        self.merged_VG = os.path.join(self.datadir, "merged_VG.jpg")
        # Horizontal images to merge
        self.mergehoriz = self.get_file_paths(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                           "..", "..", "testdata", "mergehoriz/"))
        # Horizontal images to merge
        self.mergevert = self.get_file_paths(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                          "..", "..", "testdata", "mergevert/"))

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

    @staticmethod
    def get_file_paths(directory):
        """Get file paths from a directory."""
        return [os.path.join(directory, f) for f in os.listdir(directory)]


@pytest.fixture(scope="session")
def transform_test_data():
    """Test data object for the PlantCV transform submodule."""
    return TransformTestData()
