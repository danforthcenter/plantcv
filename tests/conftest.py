import pytest
import os
import matplotlib
import json

# Disable plotting
matplotlib.use("Template")


class TestData:
    def __init__(self):
        """Initialize simple variables."""
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testdata")
        self.workflowconfig_template_file = os.path.join(self.datadir, "workflowconfig_template.json")
        self.flat_imgdir = os.path.join(self.datadir, "flat_imgdir")
        self.flat_imgdir_dates = os.path.join(self.datadir, "images_w_date")
        self.snapshot_imgdir = os.path.join(self.datadir, "snapshot_imgdir")
        self.workflow_script = os.path.join(self.datadir, "plantcv-script.py")
        self.metadata_snapshot_vis = {
            'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
                'path': os.path.join(self.snapshot_imgdir, 'snapshot57383', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
                'camera': 'SV',
                'imgtype': 'VIS',
                'zoom': 'z1',
                'exposure': 'e82',
                'gain': 'g0',
                'frame': '0',
                'lifter': 'h1',
                'timestamp': '2014-10-22 17:49:35.187',
                'id': '117770',
                'plantbarcode': 'Ca031AA010564',
                'treatment': 'none',
                'cartag': '2143',
                'measurementlabel': 'C002ch_092214_biomass',
                'other': 'none'
                }
            }
        self.metadata_flat_vis = {
            'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
                'path': os.path.join(self.flat_imgdir, 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
                'camera': 'SV',
                'imgtype': 'VIS',
                'zoom': 'z1',
                'exposure': 'e82',
                'gain': 'g0',
                'frame': '0',
                'lifter': 'h1',
                'timestamp': None,
                'id': '117770',
                'plantbarcode': 'none',
                'treatment': 'none',
                'cartag': 'none',
                'measurementlabel': 'none',
                'other': 'none'
                }
            } 

    # JSON loading helper function
    def load_json(self, json_file):
        """JSON loader helper function.
        Inputs:
        json_file = JSON filepath

        Returns:
        data      = Dictionary of JSON data

        :param json_file: str
        :return data: dict
        """
        with open(json_file, "r") as fp:
            data = json.load(fp)
            return data

    def workflowconfig_template(self):
        """Load WorkflowConfig template from file."""
        return self.load_json(json_file=self.workflowconfig_template_file)


@pytest.fixture(scope="session")
def test_data():
    return TestData()
