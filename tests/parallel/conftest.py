import pytest
import os
import json
import pandas as pd


class ParallelTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "testdata")
        # plantcv.parallel.WorkflowConfig template file
        self.workflowconfig_template_file = os.path.join(self.datadir, "workflowconfig_template.json")
        # Flat image directory
        self.flat_imgdir = os.path.join(self.datadir, "flat_imgdir")
        # Flat image directory with dates in filenames
        self.flat_imgdir_dates = os.path.join(self.datadir, "images_w_date")
        # Snapshot image directory
        self.snapshot_imgdir = os.path.join(self.datadir, "snapshot_imgdir")
        # Phenodata directory
        self.phenodata_dir = os.path.join(self.datadir, "phenodata_dir")
        # PlantCV workflow script
        self.workflow_script = os.path.join(self.datadir, "plantcv-script.py")
        # Output directory from parallel processing, contains results files
        self.parallel_results_dir = os.path.join(self.datadir, "parallel_results")
        # JSON results file with appended results
        self.appended_results_file = os.path.join(self.datadir, "appended_results.json")
        # JSON results file with a single set of results
        self.new_results_file = os.path.join(self.datadir, "new_results.json")
        # Valid JSON file but invalid results
        self.valid_json_file = os.path.join(self.datadir, "valid.json")
        self.image_path = os.path.join(self.snapshot_imgdir, 'snapshot57383', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg')
        self.nir_path = os.path.join(self.snapshot_imgdir, 'snapshot57383', 'NIR_SV_0_z1_h1_g0_e65_117779.jpg')

    @staticmethod
    def load_json(json_file):
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

    def appended_results(self):
        """Load appended results from file."""
        return self.load_json(json_file=self.appended_results_file)

    def new_results(self):
        """Load appended results from file."""
        return self.load_json(json_file=self.new_results_file)

    def metadata_snapshot_vis(self):
        """Create image metadata DataFrame."""
        meta = {
            "filepath": [os.path.join(self.snapshot_imgdir, "snapshot57383", "VIS_SV_0_z1_h1_g0_e82_117770.jpg")],
            "camera": ["SV"],
            "imgtype": ["VIS"],
            "zoom": ["z1"],
            "exposure": ["e82"],
            "gain": ["g0"],
            "frame": [None],
            "rotation": ["0"],
            "lifter": ["h1"],
            "timestamp": ["2014-10-22 17:49:35.187"],
            "id": ["117770"],
            "barcode": ["Ca031AA010564"],
            "treatment": [None],
            "cartag": ["2143"],
            "measurementlabel": ["C002ch_092214_biomass"],
            "other": [None]
            }
        df = pd.DataFrame(meta)
        df["timestamp"] = pd.to_datetime(df.timestamp)
        df = df.groupby(["filepath"])
        return df

    def metadata_snapshot_coprocess(self):
        """Create image metadata DataFrame."""
        meta = {
            "filepath": [os.path.join(self.snapshot_imgdir, "snapshot57383", "VIS_SV_0_z1_h1_g0_e82_117770.jpg"),
                         os.path.join(self.snapshot_imgdir, "snapshot57383", "NIR_SV_0_z1_h1_g0_e65_117779.jpg")],
            "camera": ["SV", "SV"],
            "imgtype": ["VIS", "NIR"],
            "zoom": ["z1", "z1"],
            "exposure": ["e82", "e65"],
            "gain": ["g0", "g0"],
            "frame": [None, None],
            "rotation": ["0", "0"],
            "lifter": ["h1", "h1"],
            "timestamp": ["2014-10-22 17:49:35.187", "2014-10-22 17:49:35.187"],
            "id": ["117770", "117779"],
            "barcode": ["Ca031AA010564", "Ca031AA010564"],
            "treatment": [None, None],
            "cartag": ["2143", "2143"],
            "measurementlabel": ["C002ch_092214_biomass", "C002ch_092214_biomass"],
            "other": [None, None]
            }
        df = pd.DataFrame(meta)
        df["timestamp"] = pd.to_datetime(df.timestamp)
        df = df.groupby(["camera", "rotation"])
        return df


@pytest.fixture(scope="session")
def parallel_test_data():
    """Test data object for the PlantCV parallel submodule."""
    return ParallelTestData()
