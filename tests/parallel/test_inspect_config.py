import pytest
from plantcv.parallel import inspect_dataset, WorkflowConfig


def test_inspect_dataset(parallel_test_data):
    """Test for PlantCV
    Testing inspection for config files
    """
    # initialize config
    config = WorkflowConfig()
    config.input_dir = parallel_test_data.flat_imgdir
    config.imgformat = "jpg"
    # inspect dataset
    sdf, df = inspect_dataset(config)

    assert sdf.shape == (1, 18) and df.shape == (2, 19)


def test_inspect_dataset_string(parallel_test_data):
    """Test for PlantCV
    Testing inspection for config files
    """
    # initialize config
    sdf, df = inspect_dataset(parallel_test_data.flat_imgdirconfig)
    # nothing found because default is png imgformat
    assert sdf.shape == (0, 2) and df.shape == (0, 3)
