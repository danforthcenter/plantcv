import pytest
from plantcv.parallel import metadata_parser, WorkflowConfig


def test_metadata_parser_snapshots(parallel_test_data):
    """Test for PlantCV.

    Test parsing a "phenofront" dataset.
    """
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = parallel_test_data.snapshot_imgdir
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = parallel_test_data.workflow_script
    config.metadata_filters = {"imgtype": "VIS", "camera": "SV"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"

    meta = metadata_parser(config=config)
    assert len(meta) == 1


@pytest.mark.parametrize("subdirs", [True, False])
def test_metadata_parser_images(parallel_test_data, subdirs):
    """Test for PlantCV.

    Test parsing a filename-based dataset.
    """
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = parallel_test_data.flat_imgdir
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = parallel_test_data.workflow_script
    config.metadata_filters = {"imgtype": "VIS"}
    config.imgformat = "jpg"
    config.include_all_subdirs = subdirs
    config.delimiter = r'(VIS)_(SV)_(\d+)_(z1)_(h1)_(g0)_(e82)_(\d+)'

    meta = metadata_parser(config=config)
    assert len(meta) == 1


def test_metadata_parser_phenodata(parallel_test_data):
    """Test for PlantCV.

    Test parsing a "phenodata" dataset.
    """
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = parallel_test_data.phenodata_dir
    config.json = "output.json"
    config.workflow = parallel_test_data.workflow_script
    config.imgformat = "jpg"

    meta = metadata_parser(config=config)
    assert len(meta) == 12
