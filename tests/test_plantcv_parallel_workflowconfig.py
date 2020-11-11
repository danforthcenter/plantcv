from plantcv.parallel import WorkflowConfig
import json


def test_plantcv_parallel_workflowconfig_save_config_file(test_data, tmpdir):
    # Create a tmp JSON file
    template_file = tmpdir.mkdir("sub").join("config.json")
    # Create config instance
    config = WorkflowConfig()
    # Save template file
    config.save_config(config_file=str(template_file))
    content = json.load(template_file)

    assert test_data["workflowconfig_template"] == content


def test_plantcv_parallel_workflowconfig_import_config_file(test_data):
    # Create config instance
    config = WorkflowConfig()
    # import config file
    config.import_config(config_file=test_data["workflowconfig_template_file"])

    assert vars(config) == test_data["workflowconfig_template"]


def test_plantcv_parallel_workflowconfig_validate_config(test_data, tmpdir):
    # Create a test tmp directory
    img_outdir = tmpdir.mkdir("sub")
    # Create config instance
    config = WorkflowConfig()
    # Set valid values in config
    config.input_dir = test_data["img_flatdir"]
    config.json = "valid_config.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data["workflow_script"]
    config.img_outdir = img_outdir
    # Validate config
    assert config.validate_config()


def test_plantcv_parallel_workflowconfig_invalid_startdate(test_data, tmpdir):
    # Create a test tmp directory
    img_outdir = tmpdir.mkdir("sub")
    # Create config instance
    config = WorkflowConfig()
    # Set valid values in config
    config.input_dir = test_data["img_flatdir"]
    config.json = "valid_config.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data["workflow_script"]
    config.img_outdir = img_outdir
    config.start_date = "2020-05-10"
    # Validate config
    assert not config.validate_config()


def test_plantcv_parallel_workflowconfig_invalid_enddate(test_data, tmpdir):
    # Create a test tmp directory
    img_outdir = tmpdir.mkdir("sub")
    # Create config instance
    config = WorkflowConfig()
    # Set valid values in config
    config.input_dir = config.input_dir = test_data["img_flatdir"]
    config.json = "valid_config.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = config.workflow = test_data["workflow_script"]
    config.img_outdir = img_outdir
    config.end_date = "2020-05-10"
    config.timestampformat = "%Y%m%d"
    # Validate config
    assert not config.validate_config()


def test_plantcv_parallel_workflowconfig_invalid_metadata_terms():
    # Create config instance
    config = WorkflowConfig()
    # Set invalid values in config
    # input_dir and json are not defined by default, but are required
    # Set an incorrect metadata term
    config.filename_metadata.append("invalid")
    # Validate config
    assert not config.validate_config()


def test_plantcv_parallel_workflowconfig_invalid_filename_metadata():
    # Create config instance
    config = WorkflowConfig()
    # Set invalid values in config
    # input_dir and json are not defined by default, but are required
    # Do not set required filename_metadata
    # Validate config
    assert not config.validate_config()


def test_plantcv_parallel_workflowconfig_invalid_cluster():
    # Create config instance
    config = WorkflowConfig()
    # Set invalid values in config
    # input_dir and json are not defined by default, but are required
    # Set invalid cluster type
    config.cluster = "MyCluster"
    # Validate config
    assert not config.validate_config()
