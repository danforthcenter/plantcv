from plantcv.parallel import WorkflowConfig
import pytest


def test_save_config_file(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a tmp JSON file
    template_file = tmpdir.mkdir("cache").join("config.json")
    # Create config instance
    config = WorkflowConfig()
    # Save template file
    config.save_config(config_file=template_file)
    content = parallel_test_data.load_json(json_file=template_file)

    assert content == parallel_test_data.workflowconfig_template()


def test_import_config_file(parallel_test_data):
    """Test for PlantCV."""
    # Create config instance
    config = WorkflowConfig()
    # import config file
    config.import_config(config_file=parallel_test_data.workflowconfig_template_file)
    content = vars(config)
    content = {k.strip("_"): v for k, v in content.items()}
    assert content == parallel_test_data.workflowconfig_template()


def test_reactive_metadata_terms_config(parallel_test_data):
    """Test for PlantCV."""
    # Create config instance
    config = WorkflowConfig()
    # add a non-standard piece of filename metadata
    config.filename_metadata = ["a weird key"]
    assert bool(config.metadata_terms["a weird key"])

    
def test_validate_config(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    img_outdir = tmpdir.mkdir("cache")
    # Create config instance
    config = WorkflowConfig()
    # Set valid values in config
    config.input_dir = parallel_test_data.flat_imgdir
    config.results = "valid_config.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = parallel_test_data.workflow_script
    config.img_outdir = str(img_outdir)
    # Validate config
    assert config.validate_config()


def test_invalid_startdate(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    img_outdir = tmpdir.mkdir("cache")
    # Create config instance
    config = WorkflowConfig()
    # Set valid values in config
    config.input_dir = parallel_test_data.flat_imgdir
    config.results = "valid_config.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = parallel_test_data.workflow_script
    config.img_outdir = str(img_outdir)
    config.start_date = "2020-05-10"
    # Validate config
    assert not config.validate_config()


def test_invalid_enddate(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    img_outdir = tmpdir.mkdir("cache")
    # Create config instance
    config = WorkflowConfig()
    # Set valid values in config
    config.input_dir = config.input_dir = parallel_test_data.flat_imgdir
    config.results = "valid_config.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = config.workflow = parallel_test_data.workflow_script
    config.img_outdir = str(img_outdir)
    config.end_date = "2020-05-10"
    config.timestampformat = "%Y%m%d"
    # Validate config
    assert not config.validate_config()


def test_invalid_cluster():
    """Test for PlantCV."""
    # Create config instance
    config = WorkflowConfig()
    # Set invalid values in config
    # input_dir and json are not defined by default, but are required
    # Set invalid cluster type
    config.cluster = "MyCluster"
    # Validate config
    assert not config.validate_config()


def test_bad_config_setting():
    """Test for PlantCV."""
    # create config instance
    config = WorkflowConfig()
    # try to set groupby (list) to a string
    with pytest.raises(ValueError):
        config.groupby = "bad"


def test_too_many_cluster_config_cores(parallel_test_data):
    """Test for PlantCV."""
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = config.input_dir = parallel_test_data.flat_imgdir
    config.json = "valid_config.json"
    config.workflow = config.workflow = parallel_test_data.workflow_script
    # Set invalid values in config
    # input_dir and json are not defined by default, but are required
    # Set invalid cluster type
    config.cluster = "LocalCluster"
    config.cluster_config["n_workers"] = 1000
    config.cluster_config["cores"] = 1000
    # Validate config
    assert not config.validate_config()
