from plantcv.parallel import jupyterconfig
import os


def test_jupcon_in_notebook():
    """Test for PlantCV."""
    # initialize jupyterconfig
    jupcon = jupyterconfig()
    # main.__file__ is the py.test runner, so this check will be false.
    # this makes other testing potentially difficult.
    assert not jupyterconfig.in_notebook()


def test_jupcon_overwriting_in_notebook(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # initialize jupyterconfig
    temp_path = tmpdir.mkdir("cache")
    os.environ["JPY_SESSION_NAME"] = "example.ipynb"
    os.chdir(temp_path)
    jupcon = jupyterconfig()
    # force this to act like there is a notebook
    jupcon.in_notebook = lambda: True
    jupcon.save_config()
    print(os.getcwd())
    assert jupcon.in_notebook() and os.path.exists(jupcon.config)
