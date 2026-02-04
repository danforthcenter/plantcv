import sys
from plantcv.parallel import WorkflowConfig
from plantcv.parallel.run_parallel import _check_for_conda


def test_checking_conda_env(parallel_test_data, monkeypatch, tmpdir):
    """Test for plantCV."""
    monkeypatch.setattr(sys, "executable", "/my/XcondaX/env/example/python")
    # set up a configuration
    config = WorkflowConfig()
    # check for conda
    config = _check_for_conda(config)
    assert config.cluster_config["job_script_prologue"][0] == "source /my/XcondaX/bin/activate"
