# Integration tests for plantcv-run-workflow
import os
import sys
import dask
import pytest
import shutil
import tempfile
from plantcv.parallel import WorkflowConfig
from plantcv.parallel.cli import main


def test_parallel_cli_template(tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory and results file
    conf_file = tmpdir.mkdir("sub").join("config.json")
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-run-workflow", "--template", conf_file.strpath]
    with pytest.raises(SystemExit):
        main()


def test_parallel_cli_dryrun(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory and results file
    conf_file = tmpdir.mkdir("sub").join("config.json")
    config = WorkflowConfig()
    config.input_dir = parallel_test_data.flat_imgdir
    config.results = "valid_config.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = parallel_test_data.workflow_script
    config.img_outdir = str(conf_file.dirpath())
    config.save_config(config_file=conf_file.strpath)
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-run-workflow", "--dryrun", conf_file.strpath]
    assert main() is None


def test_parallel_cli_invalid_config(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    conf_file = tmpdir.mkdir("cache").join("config.json")
    config = WorkflowConfig()
    # Set valid values in config
    config.results = "valid_config.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = parallel_test_data.workflow_script
    config.img_outdir = str(conf_file.dirpath())
    config.save_config(config_file=conf_file.strpath)
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-run-workflow", "--config", conf_file.strpath]
    with pytest.raises(SystemExit) as exitcode:
        main()
    assert exitcode.value.code == 1


def test_parallel_cli_overwriting_config(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    conf_file = tmpdir.mkdir("cache").join("config.json")
    config = WorkflowConfig()
    # Set valid values in config
    config.results = conf_file.strpath
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = parallel_test_data.workflow_script
    config.img_outdir = str(conf_file.dirpath())
    config.save_config(config_file=conf_file.strpath)
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-run-workflow", "--config", conf_file.strpath]
    with pytest.raises(SystemExit) as exitcode:
        main()
    assert exitcode.value.code == 1


def test_parallel_cli_valid_config_checkpointed(parallel_test_data, tmpdir, capsys):
    """Test for PlantCV."""
    # Create a test tmp directory
    conf_file = tmpdir.mkdir("cache").join("config.json")
    os.chdir(conf_file.dirpath().strpath)
    # Set the temp directory for dask
    dask.config.set(temporary_directory=str(conf_file.dirpath()))
    config = WorkflowConfig()
    # Set valid values in config
    config.input_dir = parallel_test_data.flat_imgdir
    config.results = conf_file.dirpath().join(os.path.basename(parallel_test_data.new_results_file)).strpath
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.metadata_regex = {"filepath": ".*"}
    config.workflow = parallel_test_data.workflow_script
    config.img_outdir = str(conf_file.dirpath())
    config.tmp_dir = str(conf_file.dirpath() / "tmp")
    # CHANGE: make a "previous run" directory under _PCV_PARALLEL_CHECKPOINT_ (note the
    # trailing underscore, matching run_parallel) holding a hash that cannot match
    prev_run_dir = os.path.join(config.tmp_dir, "_PCV_PARALLEL_CHECKPOINT_")
    os.makedirs(prev_run_dir)
    with open(os.path.join(prev_run_dir, "_PCV_WORKFLOW_HASH"), "w") as f:
        f.write("qwerty")
    config.cluster_config["log_directory"] = "."
    config.append = False
    config.checkpoint = True
    config.save_config(config_file=conf_file.strpath)
    shutil.copy(parallel_test_data.new_results_file, conf_file.dirpath())
    # Mock ARGV
    sys.argv = ["plantcv-run-workflow", "--config", conf_file.strpath]
    assert main() is None
    assert "has changed, checkpoint data will be ignored" in capsys.readouterr().out
