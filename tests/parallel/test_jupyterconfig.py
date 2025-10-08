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
    object.__setattr__(jupcon, "in_notebook", lambda: True)
    jupcon.save_config()
    assert jupcon.in_notebook() and os.path.exists(jupcon.config)


def test_import_jupcon_file(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create config instance
    os.chdir(tmpdir.mkdir("cache"))
    os.environ["JPY_SESSION_NAME"] = "example.ipynb"
    jupcon = jupyterconfig()
    # import config file
    jupcon.import_config(config_file=parallel_test_data.workflowconfig_template_file)
    content = vars(jupcon)
    content = {k.strip("_"): v for k, v in content.items()}
    assert content["notebook"] == jupcon.notebook


def test_jupcon_inspect_dataset(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # initialize jupyterconfig
    os.chdir(tmpdir.mkdir("cache"))
    os.environ["JPY_SESSION_NAME"] = "example.ipynb"
    jupcon = jupyterconfig()
    # force this to act like there is a notebook
    object.__setattr__(jupcon, "in_notebook", lambda: True)
    jupcon.input_dir = parallel_test_data.flat_imgdir
    summary, meta = jupcon.inspect_dataset()
    assert len(summary) == 1 and len(meta) == 3


def test_jupcon_notebook2script(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # initialize jupyterconfig
    starting_dir = os.getcwd()
    os.chdir(tmpdir.mkdir("cache"))
    os.environ["JPY_SESSION_NAME"] = "dummy.ipynb"
    jupcon = jupyterconfig()
    object.__setattr__(jupcon, "in_notebook", lambda: True)
    jupcon.notebook = os.path.join(starting_dir, parallel_test_data.jupyternotebook)
    jupcon.workflow = os.path.join(os.getcwd(), "dummy.py")

    jupcon.notebook2script()
    assert os.path.exists(jupcon.workflow) and jupcon.analysis_script


def test_jupcon_run(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # initialize jupyterconfig
    os.chdir(tmpdir.mkdir("cache"))
    os.environ["JPY_SESSION_NAME"] = "example.ipynb"
    jupcon = jupyterconfig()
    with open("example.py", "w") as f:
        f.write("from plantcv import plantcv as pcv")
    # force this to act like there is a notebook
    object.__setattr__(jupcon, "in_notebook", lambda: True)
    jupcon.notebook = jupcon.find_notebook()
    jupcon.input_dir = parallel_test_data.flat_imgdir
    jupcon.workflow = "example.py"
    jupcon.results = "example"
    jupcon.run()
    assert os.path.exists(jupcon.results)


def test_jupcon_run_bad_input(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # initialize jupyterconfig
    os.chdir(tmpdir.mkdir("cache"))
    os.environ["JPY_SESSION_NAME"] = "example.ipynb"
    jupcon = jupyterconfig()
    # force this to act like there is a notebook
    object.__setattr__(jupcon, "in_notebook", lambda: True)
    jupcon.input_dir = parallel_test_data.flat_imgdir
    jupcon.run()
    assert not os.path.exists(jupcon.results)
