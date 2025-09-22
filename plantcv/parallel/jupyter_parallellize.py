import os
from nbconvert import PythonExporter # new dependency
# from plantcv.parallel.workflowconfig import WorkflowConfig # this is pending #1792 merging to separate workflowconfig from init.py

class jupyterconfig:
    # initialization based mainly on plantcv/parallel/WorkflowConfig class
    def __init__(self):
        self.workflow = self.notebook2script(),  # path to python script, created here
        self.config = self.setupConfiguration() # path to config, will be written based on this object
        self.input_dir = "." # needs to be set? Defaults to here?
        self.filename_metadata = [] # won't neeeed to be set post #1798 but should be still
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
        self.writeimg = False # might be removed generally
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
    def notebook2script(self):
        # save the script this is being called in as `script`, add `script` to background config?
        ipynb_path = os.environ['JPY_SESSION_NAME']
        if self.script is None:
            # get it from os?
            py_path = os.path.splitext(ipynb_path)[0] + ".py"
            self.script = py_path
        # Make that self.script file
        # Read the notebook file
        with open(ipynb_path) as fh:
            nb = nbformat.reads(fh.read(), nbformat.NO_CONVERT)
        # Create a Python exporter instance
        exporter = PythonExporter()
        # Convert the notebook to Python code
        source, _ = exporter.from_notebook_node(nb)
        # Write the output to a Python file
        with open(self.script, 'w') as fh:
            fh.writelines(source)

    def setupConfiguration(self):
        # this should make a python script and a config file per the standard way of parallelizing
        # i think this makes a WorkflowConfig from this thing and parallelizes per the standard method after that, just turning the jupyter kernel into the head node?
        # make a config object
        config = WorkflowConfig()
        # find shared keys between config and self
        # loop over shared keys, assign from self to config
        # run config.save_config(self.config)
        # ...
        # profit?

        
        return self


    
    def validate_notebook(self):
        # this should check the notebook and warn you about any suspicious lines (hey are you wanting to plot this..?)
        #
        return self
    def lint_notebook(self):
        # optionally could perform extra quality control on the generated script?
        return self
