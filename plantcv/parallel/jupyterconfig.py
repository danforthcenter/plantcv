import os
import json
import re
import nbformat
from nbconvert import PythonExporter
from plantcv.parallel.workflowconfig import WorkflowConfig, _config_attr_lookup
from plantcv.parallel.run_parallel import run_parallel
from plantcv.parallel.inspect_dataset import inspect_dataset
from plantcv.parallel.message import parallel_print


class jupyterconfig:
    # initialization based mainly on plantcv/parallel/WorkflowConfig class
    def __init__(self):
        object.__setattr__(self, "verbose", True)
        # reactive properties set within notebook when initialized
        object.__setattr__(self, "notebook", self.find_notebook())  # path to active notebook
        object.__setattr__(self, "workflow", self.nameScript())  # path to python script, created here
        object.__setattr__(self, "config", self.nameConfig())  # path to config, will be written based on this object
        object.__setattr__(self, "analysis_script", self.notebook2script())  # convert notebook to py
        # things that should be user set after object is initialized, argument like.
        object.__setattr__(self, "input_dir", ".")
        object.__setattr__(self, "results", "results")
        object.__setattr__(self, "filename_metadata", [])
        object.__setattr__(self, "img_outdir", "./output_images")
        object.__setattr__(self, "include_all_subdirs", True)
        object.__setattr__(self, "tmp_dir", ".")
        object.__setattr__(self, "start_date", None)
        object.__setattr__(self, "end_date", None)
        object.__setattr__(self, "imgformat", "all")
        object.__setattr__(self, "delimiter", "_")
        object.__setattr__(self, "metadata_filters", {})
        object.__setattr__(self, "metadata_regex", {})
        object.__setattr__(self, "timestampformat", "%Y-%m-%dT%H:%M:%S.%fZ")
        object.__setattr__(self, "writeimg", False)  # might be removed generally
        object.__setattr__(self, "other_args", {})
        object.__setattr__(self, "groupby", ["filepath"])
        object.__setattr__(self, "group_name", "auto")
        object.__setattr__(self, "checkpoint", True)
        object.__setattr__(self, "cleanup", True)
        object.__setattr__(self, "append", False)
        object.__setattr__(self, "cluster", "LocalCluster")
        object.__setattr__(self, "cluster_config", {
            "n_workers": 1,
            "cores": 1,
            "memory": "1GB",
            "disk": "1GB",
            "log_directory": None,
            "local_directory": None,
            "job_extra_directives": None
        })
        # does not need to have reactive metadata_terms, those are made when run() is called

    def __setattr__(self, name, value):
        _config_attr_lookup(self, name, value)
        object.__setattr__(self, name, value)

    # make reactive notebook property and hidden helper
    @property
    def notebook(self):
        """Get active notebook file name"""
        return self._notebook

    @notebook.setter
    def notebook(self, new):
        """Set active notebook file name"""
        self._notebook = new

    # function for finding the active notebook, slightly fraught?
    def find_notebook(self):
        """Make active notebook file name"""
        ipynb_path = "not_found"
        if self.in_notebook():
            ipynb_path = os.environ['JPY_SESSION_NAME']
        return ipynb_path

    # make reactive workflow (python script path) property and hidden helper
    @property
    def workflow(self):
        """Get workflow file name"""
        self._workflow = self.nameScript()
        return self._workflow

    @workflow.setter
    def workflow(self, new):
        """Set workflow file name, you probably should not do this"""
        self._workflow = new

    # function for naming script
    def nameScript(self):
        """Make workflow file name"""
        # make a name for the script
        py_path = os.path.splitext(self.notebook)[0] + ".py"
        return py_path

    # function for naming results if empty
    @property
    def results(self):
        """Get results file name"""
        self._results = self.nameResults()
        return self._results

    @results.setter
    def results(self, new):
        """Set results file name"""
        self._results = new

    def nameResults(self):
        """Name results file"""
        res_path = os.path.splitext(self.notebook)[0] + "_parallel_results"
        return res_path

    # make reactive analysis script as self.script, value here stored as boolean
    @property
    def analysis_script(self):
        """Get analysis_script attribute and make script"""
        self._analysis_script = os.path.exists(self.workflow)
        return self._analysis_script

    @analysis_script.setter
    def analysis_script(self, new):
        """Set new 'analysis script is ready' bool value, you should not do this"""
        self._analysis_script = new

    # function to convert a notebook to a script and write it out
    def notebook2script(self):
        """Turn notebook into a script"""
        # Make that self.script file
        # Read the notebook file
        if self.in_notebook():
            with open(self.notebook) as fh:
                nb = nbformat.reads(fh.read(), nbformat.NO_CONVERT)
            # ignore @ignore tagged cells
            del_cells = []
            for i, cell in enumerate(nb.cells):
                if re.search(r"^\s*#\s*@ignore", cell.source, re.MULTILINE) and cell.cell_type == "code":
                    del_cells.append(i)
            for i in sorted(del_cells, reverse=True):
                del nb.cells[i]
            # Create a Python exporter instance
            exporter = PythonExporter()
            # Convert the notebook to Python code
            source, _ = exporter.from_notebook_node(nb)
            # Write the output to a Python file
            with open(self.workflow, 'w') as fh:
                fh.writelines(source)
            # return boolean for if self.script exists
        return os.path.exists(self.workflow)

    # make reactive property for config so that it rewrites when changed?
    @property
    def config(self):
        """Get config values"""
        return self._config

    @config.setter
    def config(self, new):
        """Set config values"""
        self._config = new

    # make a configuration file for running in parallel within current corpus
    def nameConfig(self):
        """Make name for config file"""
        # save out with self config
        config_file_name = os.path.splitext(self.workflow)[0] + ".json"
        return config_file_name

    def inspect_dataset(self):
        """Inspect input directory of images"""
        summary = None
        meta = None
        if self.in_notebook():
            config = WorkflowConfig()
            for attr in [attr for attr in vars(config).keys() if attr in vars(self).keys()]:
                object.__setattr__(config, attr, getattr(self, attr))
            summary, meta = inspect_dataset(config)
        return summary, meta

    # proper functions called for stuff other than reactive properties
    def run(self):
        """Run current Config"""
        # if in notebook, save config, start parallel.
        if self.in_notebook():
            parallel_print("Initializing from " + self.notebook + " Notebook", verbose=self.verbose)
            # before running, rerun reactives then kick off the parallel process?
            self.save_config()
            # other "reactives" should be set since they are based only on the file
            # this is being run in.
            # if needed could change them again but I think this is reasonable for now.
            parallel_print("Starting parallel workflow from notebook kernel", verbose=self.verbose)
            config = WorkflowConfig()
            config.import_config(self.config)
            if config.validate_config():
                run_parallel(config)
                parallel_print("Done!", verbose=config.verbose)
            else:
                print("Config validation failed, run aborted")

    def save_config(self):
        """Save current Config"""
        # make a config object
        if self.in_notebook():
            config = WorkflowConfig()
            # find shared keys between config and self, loop over assigning from self to config
            for attr in [attr for attr in vars(config).keys() if attr in vars(self).keys()]:
                object.__setattr__(config, attr, getattr(self, attr))
            # set a few manually due to property differences
            config.workflow = self.workflow
            config.json = self.results
            # save
            config.save_config(config_file=self.config)
            parallel_print("Saved " + self.config, verbose=self.verbose)

    # Import a configuration from a file
    def import_config(self, config_file):
        """Import a configuration file.

        Input variables:
        config_file = Configuration file to import

        :param config_file: str
        """
        # Open the file for reading
        with open(config_file, "r") as fp:
            # Import the JSON configuration data
            config = json.load(fp)
            for key, value in config.items():
                if key == "json":
                    object.__setattr__(self, "results", value)
                elif key != "_metadata_terms":
                    object.__setattr__(self, key, value)

    @staticmethod
    def in_notebook():
        """Check if executed from a notebook."""
        # when jobs are run they are submitted to command line, so have no __file__ attribute
        import __main__ as main
        return not hasattr(main, '__file__')
