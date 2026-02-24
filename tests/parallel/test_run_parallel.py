import sys
from plantcv.parallel import WorkflowConfig
from plantcv.parallel.run_parallel import _check_for_conda


def test_checking_conda_env(parallel_test_data, monkeypatch, tmpdir):
    """Test for plantCV."""
    monkeypatch.setattr(sys, "executable", "/my/Xconda3/env/example/python")
    # set up a configuration
    config = WorkflowConfig()
    # check for conda
    config = _check_for_conda(config)
    assert config.cluster_config["job_script_prologue"][0] == "source /my/Xconda3/bin/activate"


def test_checking_conda_base_env(monkeypatch):
    """Test for PlantCV."""
    # Simulate a base conda environment executable (no envs/ segment)
    monkeypatch.setattr(sys, "executable", "/my/Xconda4/bin/python")
    config = WorkflowConfig()
    # This should not raise and should produce an activation line for the base env
    config = _check_for_conda(config)
    assert config.cluster_config["job_script_prologue"] == ["source /my/Xconda4/bin/activate"]
