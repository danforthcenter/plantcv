from plantcv.parallel import inspect_dataset, WorkflowConfig


def test_inspect_dataset(parallel_test_data):
    """Test for PlantCV
    Testing inspection for interactively made config files
    """
    # initialize config
    config = WorkflowConfig()
    config.input_dir = parallel_test_data.flat_imgdir
    config.imgformat = "jpg"
    config.filename_metadata = ["imgtype", "camera", "angle", "zoom", "gain", "exposure", "lifter", "id"]
    config.metadata_filters = {"imgtype" : "VIS"}
    # inspect dataset
    sdf, df = inspect_dataset(config)

    assert sdf.shape == (2, 10) and df.shape == (2, 12)


def test_inspect_dataset_string(parallel_test_data):
    """Test for PlantCV
    Testing inspection for file path input
    """
    sdf, df = inspect_dataset(parallel_test_data.phenodata_dir)
    # nothing found because default is png imgformat
    assert sdf.shape == (1, 6) and df.shape == (12, 7)


def test_inspect_dataset_config_file(parallel_test_data):
    """Test for PlantCV
    Testing inspection for existing config files
    """
    # workflowconfig_template_file here has an empty string input_dir so nothing is found
    sdf, df = inspect_dataset(parallel_test_data.workflowconfig_template_file)
    assert sdf.shape == (0, 5) and df.shape == (0, 6)
