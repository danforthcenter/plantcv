import pytest
import os
import json
import matplotlib
import matplotlib.pyplot as plt
from plantcv.plantcv._globals import params, Params, outputs
from tests import synthetic

# Disable plotting
matplotlib.use("Template")


class TestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = synthetic.TESTDATA
        # Outputs results file - JSON
        self.outputs_results_json = os.path.join(self.datadir, "outputs_results.json")
        # Outputs results file - CSV
        self.outputs_results_csv = os.path.join(self.datadir, "outputs_results.csv")
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


@pytest.fixture(autouse=True)
def reset_params():
    """Always clear parameter changes from running functions"""
    params.__dict__.update(vars(Params()))
    outputs.clear()
    yield
    plt.close("all")
