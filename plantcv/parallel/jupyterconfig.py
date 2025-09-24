import os
import nbformat
from nbconvert import PythonExporter
from plantcv.parallel import WorkflowConfig, run_parallel, inspect_dataset


class jupyterconfig:
    # initialization based mainly on plantcv/parallel/WorkflowConfig class
    def __init__(self):

        # reactive properties set within notebook when initialized
        self.notebook = self.find_notebook()  # path to active notebook
        self.workflow = self.nameScript()  # path to python script, created here
        self.config = self.nameConfig()  # path to config, will be written based on this object
        self.analysis_script = self.notebook2script()  # convert notebook to py
        # things that should be user set after object is initialized, argument like.
        self.input_dir = "."
        self.results = "results"
        self.filename_metadata = []
        self.img_outdir = "./output_images"
        self.include_all_subdirs = True
        self.tmp_dir = "."
        self.start_date = None
        self.end_date = None
        self.imgformat = "png"
        self.delimiter = "_"
        self.metadata_filters = {}
        self.metadata_regex = {}
        self.timestampformat = "%Y-%m-%dT%H:%M:%S.%fZ"
        self.writeimg = False  # might be removed generally
        self.other_args = {}
        self.groupby = ["filepath"]
        self.group_name = "auto"
        self.cleanup = True
        self.append = False
        self.cluster = "LocalCluster"
        self.cluster_config = {
            "n_workers": 1,
            "cores": 1,
            "memory": "1GB",
            "disk": "1GB",
            "log_directory": None,
            "local_directory": None,
            "job_extra_directives": None
        }

    # make reactive notebook property and hidden helper
    @property
    def notebook(self):
        """Get active notebook file name"""
        self._notebook = self.find_notebook()
        return self._notebook

    @notebook.setter
    def notebook(self, new):
        """Set active notebook file name"""
        self._notebook = new

    # function for finding the active notebook, slightly fraught?
    def find_notebook(self):
        """Make active notebook file name"""
        ipynb_path = "not found."
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
        self._analysis_script = self.notebook2script()
        return self._analysis_script

    @analysis_script.setter
    def analysis_script(self, new):
        """Set new analysis script value, you should not do this"""
        self._analysis_script = new
    
    # function to convert a notebook to a script and write it out
    def notebook2script(self):
        """Turn notebook into a script"""
        # Make that self.script file
        # Read the notebook file
        if self.in_notebook():
            with open(self.notebook) as fh:
                nb = nbformat.reads(fh.read(), nbformat.NO_CONVERT)
            # Create a Python exporter instance
            exporter = PythonExporter()
            # Convert the notebook to Python code
            source, _ = exporter.from_notebook_node(nb)
            # Write the output to a Python file
            # NOTE could say that if you don't see 'workflow_inputs(' in the code someplace then add it?
            # I don't think we'll have smart enough parsing logic for that though. Might be a rtfm situation.
            with open(self.workflow, 'w') as fh:
                fh.writelines(source)
            # return boolean for if self.script exists
        return os.path.exists(self.workflow)

    # make reactive property for config so that it rewrites when changed?
    @property
    def config(self):
        """Get config values"""
        self._config = self.nameConfig()
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
                setattr(config, attr, getattr(self, attr))
            summary, meta = inspect_dataset(config)
        return summary, meta
    # proper functions called for stuff other than reactive properties
    def run(self):
        """Run current Config"""
        # if in notebook, save config, start parallel.
        if self.in_notebook():
            print("Initializing from" + self.notebook + "Notebook")
            # before running, rerun reactives then kick off the parallel process?
            self.save_config()
            # other "reactives" should be set since they are based only on the file
            # this is being run in.
            # if needed could change them again but I think this is reasonable for now.
            print("Starting parallel workflow from notebook kernel")
            config = WorkflowConfig()
            config.import_config(self.config)
            if config.validate_config():
                run_parallel(config)
                print("Done!")
            else:
                print("Config validation failed, run aborted")
        # NOTE could do an else to set args in the global but so far that hasn't worked

    def save_config(self):
        """Save current Config"""
        # this should make a python script and a config file per the standard way of parallelizing
        # i think this makes a WorkflowConfig from this thing and parallelizes per the standard method after that,
        #      just turning the jupyter kernel into the head node?
        # make a config object
        if self.in_notebook():
            config = WorkflowConfig()
            # find shared keys between config and self, loop over assigning from self to config
            for attr in [attr for attr in vars(config).keys() if attr in vars(self).keys()]:
                setattr(config, attr, getattr(self, attr))
            # set a few manually due to property differences
            config.workflow = self.workflow
            config.json = self.results
            # save
            config.save_config(config_file=self.config)
            print("Saved" + self.config)

    @staticmethod
    def in_notebook():
        """Check if executed from a notebook."""
        import __main__ as main
        return not hasattr(main, '__file__')
    
    def validate(self):
        """Validation checks on current configuration."""
        # this should check the notebook and warn you about any suspicious lines (hey are you wanting to plot this..?)
        return self
    def lint(self):
        """linter"""
        # optionally could perform extra quality control on the generated script?
        return self
