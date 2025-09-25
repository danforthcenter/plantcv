from plantcv.parallel import jupyterconfig
import os


def test_jupcon_in_notebook(tmpdir):
    """Test for PlantCV."""
    # initialize jupyterconfig
    os.chdir(tmpdir.mkdir("cache"))
    jupcon = jupyterconfig()
    # main.__file__ is the py.test runner, so this check will be false.
    # this makes other testing potentially difficult.
    assert not jupcon.in_notebook()


def test_jupcon_save_config(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # initialize jupyterconfig
    os.chdir(tmpdir.mkdir("cache"))
    os.environ["JPY_SESSION_NAME"] = "example.ipynb"
    jupcon = jupyterconfig()
    # force this to act like there is a notebook
    jupcon.in_notebook = lambda: True
    jupcon.save_config()
    assert jupcon.in_notebook() and os.path.exists(jupcon.config)


def test_jupcon_inspect_dataset(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # initialize jupyterconfig
    os.chdir(tmpdir.mkdir("cache"))
    os.environ["JPY_SESSION_NAME"] = "example.ipynb"
    jupcon = jupyterconfig()
    # force this to act like there is a notebook
    jupcon.in_notebook = lambda: True
    jupcon.input_dir = parallel_test_data.flat_imgdir
    summary, meta = jupcon.inspect_dataset()
    assert len(summary) == 1 and len(meta) == 3


def test_jupcon_run(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # initialize jupyterconfig
    os.chdir(tmpdir.mkdir("cache"))
    os.environ["JPY_SESSION_NAME"] = "example.ipynb"
    jupcon = jupyterconfig()
    with open("example.py", "w") as f:
        f.write("from plantcv import plantcv as pcv")
    # force this to act like there is a notebook
    jupcon.in_notebook = lambda: True
    jupcon.input_dir = parallel_test_data.flat_imgdir
    jupcon.run()
    assert os.path.exists(jupcon.results)
    

def test_jupcon_run_bad_input(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # initialize jupyterconfig
    os.chdir(tmpdir.mkdir("cache"))
    os.environ["JPY_SESSION_NAME"] = "example.ipynb"
    jupcon = jupyterconfig()
    # force this to act like there is a notebook
    jupcon.in_notebook = lambda: True
    jupcon.input_dir = parallel_test_data.flat_imgdir
    jupcon.run()
    assert not os.path.exists(jupcon.results)
