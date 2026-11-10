import pytest
import os
import json
import pandas as pd
from tests import synthetic


class ParallelTestData:
    def __init__(self, imgroot):
        """Initialize simple variables and write the synthetic image datasets to imgroot."""
        # Test data directory
        self.datadir = synthetic.TESTDATA
        # plantcv.parallel.WorkflowConfig template file
        self.workflowconfig_template_file = os.path.join(self.datadir, "workflowconfig_template.json")
        # Flat image directory
        self.flat_imgdir = synthetic.write_image_dir(os.path.join(imgroot, "flat_imgdir"), "flat")
        # Snapshot image directory
        self.snapshot_imgdir = synthetic.write_image_dir(os.path.join(imgroot, "snapshot_imgdir"), "snapshot")
        # Phenodata directory
        self.phenodata_dir = synthetic.write_image_dir(os.path.join(imgroot, "phenodata_dir"), "phenodata")
        # PlantCV workflow script
        self.workflow_script = os.path.join(self.datadir, "plantcv-script.py")
        # Dummy jupyter notebook file
        self.jupyternotebook = os.path.join(self.datadir, "dummy.ipynb")
        self.image_path = os.path.join(self.snapshot_imgdir, 'snapshot57383', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg')
        self.nir_path = os.path.join(self.snapshot_imgdir, 'snapshot57383', 'NIR_SV_0_z1_h1_g0_e65_117779.jpg')

    def workflowconfig_template(self):
        """Load WorkflowConfig template from file."""
        with open(self.workflowconfig_template_file, "r") as fp:
            return json.load(fp)

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
        return df


@pytest.fixture(scope="session")
def parallel_test_data(tmp_path_factory):
    """Test data object for the PlantCV parallel submodule."""
    return ParallelTestData(str(tmp_path_factory.mktemp("parallel_data")))
