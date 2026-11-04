import pytest
import os
import json
import numpy as np
import matplotlib
from tests import synthetic

# Disable plotting
matplotlib.use("Template")


class TestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testdata")
        # heic image
        self.heic_img = os.path.join(self.datadir, "example.HEIC")
        # Outputs results file - JSON
        self.outputs_results_json = os.path.join(self.datadir, "outputs_results.json")
        # Outputs results file - CSV
        self.outputs_results_csv = os.path.join(self.datadir, "outputs_results.csv")
        # Thermal image
        self.thermal_img = os.path.join(self.datadir, "FLIR2600.csv")
        # Thermal image data
        self.thermal_obj_file = os.path.join(self.datadir, "thermal_img.npz")
        # Thermal image mask
        self.thermal_mask = os.path.join(self.datadir, "thermal_img_mask.png")
        # Bayer image
        self.bayer_img = os.path.join(self.datadir, "bayer_img.png")
        # Naive Bayes trained model file
        self.nb_trained_model = os.path.join(self.datadir, "naive_bayes_pdfs.txt")
        # Naive Bayes bad model file
        self.nb_bad_model = os.path.join(self.datadir, "naive_bayes_pdfs_bad.txt")
        # Kmeans classifier directory
        self.kmeans_classifier_dir = os.path.join(self.datadir, "kmeans_classifier_dir")
        # Circle Wells for Hough Circle
        self.hough_circle = os.path.join(self.datadir, "circle-wells.png")
        # Kmeans classifier grayscale directory
        self.kmeans_classifier_gray_dir = os.path.join(self.datadir, "kmeans_classifier_gray_dir")
        # nd2 file
        self.nd2_img = os.path.join(self.datadir, "test_nd2_img.nd2")
        # flir thermal img
        self.flir_img = os.path.join(self.datadir, "FLIR_test.jpg")
        # parallel results to process
        self.parallel_results_dir = os.path.join(self.datadir, "parallel_results")
        # appended results file
        self.appended_results_file = os.path.join(self.datadir, "appended_results.json")
        # new results file
        self.new_results_file = os.path.join(self.datadir, "new_results.json")
        # valid results file
        self.valid_json_file = os.path.join(self.datadir, "valid.json")
        # invalid results file
        self.invalid_results_file = os.path.join(self.datadir, "invalid_results.json")
        # plantcv general results file
        self.plantcv_results_file = os.path.join(self.datadir, "plantcv_results.json")
        # List of masks
        self.masks_list = os.path.join(self.datadir, "masks_list.pkl")

    @staticmethod
    def load_npz(npz_file):
        """Load data saved in a NumPy .npz file."""
        data = np.load(npz_file, encoding="latin1")
        return data['arr_0']

    @staticmethod
    def load_json(json_file):
        """JSON loader helper function."""
        with open(json_file, "r") as fp:
            data = json.load(fp)
            return data

    def new_results(self):
        """Load appended results from file."""
        return self.load_json(json_file=self.new_results_file)

    def appended_results(self):
        """Load appended results from file."""
        return self.load_json(json_file=self.appended_results_file)


@pytest.fixture(scope="session")
def test_data():
    """Test data object for the main PlantCV package."""
    return TestData()


@pytest.fixture
def synthetic_mask():
    """Binary mask of the synthetic plant (see tests/synthetic.py)."""
    return synthetic.plant_mask()


@pytest.fixture
def synthetic_rgb():
    """BGR image of the synthetic plant (see tests/synthetic.py)."""
    return synthetic.plant_rgb()


@pytest.fixture
def synthetic_gray():
    """Grayscale image of the synthetic plant (see tests/synthetic.py)."""
    return synthetic.plant_gray()
