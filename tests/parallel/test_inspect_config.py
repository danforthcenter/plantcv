from plantcv.parallel import inspect_dataset, WorkflowConfig


def test_inspect_dataset(parallel_test_data):
    """Test for PlantCV
    Testing inspection for config files
    """
    # initialize config
    config = WorkflowConfig()
    config.input_dir = parallel_test_data.flat_imgdir
    config.imgformat = "jpg"
    config.filename_metadata = ["imgtype", "camera", "angle", "zoom", "gain", "exposure", "lifter", "id"]
    config.metadata_filters = {"imgtype" : "VIS"}
    # inspect dataset
    sdf, df = inspect_dataset(config)

    assert sdf.shape == (2, 16) and df.shape == (2, 18)


def test_inspect_dataset_string(parallel_test_data):
    """Test for PlantCV
    Testing inspection for config files
    """
    # initialize config
    sdf, df = inspect_dataset(parallel_test_data.phenodata_dir)
    # nothing found because default is png imgformat
    assert sdf.shape == (1, 2) and df.shape == (12, 3)
