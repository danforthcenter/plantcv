## Running in Parallel from a Jupyter notebook

The `JupyterConfig` class is very similar to the [`WorkflowConfig` class](parallel_config.md) and is used to configure a parallel workflow directly from a Jupyter notebook.

### Quick Start

Initializing a `JupyterConfig` object in a Jupyter notebook will immediately use `nbconvert` to create a python script version of the workflow. When the python script is generated notebook cells marked with `@ignore` as the start of a comment (`# @ignore`) are excluded, which may be useful to avoid making diagnostic plots in parallel or otherwise in keeping your notebook reproducible. Any calls to `plot_image` will also be removed. Similar to `WorkflowConfig` objects you can overwrite default attributes to meet your particular needs. Once your edits are done the `run` method will run the workflow in parallel. Note that you will need to specify arguments with [`workflow_inputs`](parallel_workflow_inputs.md) how you would when using `WorkflowConfig` to run a script in parallel.

```python
from plantcv import parallel as pcvpar

jupcon = pcvpar.JupyterConfig()
jupcon.input_dir = "path/to/images"
# ... other edits
jupcon.run()

args = pcvpar.workflow_inputs()
```

*class* **plantcv.parallel.jupyterconfig**

### Class methods

Inspect the input dataset.

**JupyterConfig.inspect_dataset**()

- **Parameters:**
    - None
- **Context:**
    - Used to check which images will be found by the current configuration using [`inspect_dataset`](parallel_inspect_config.md).


Save a configuration file that can be modified and imported to run workflows in parallel.

**JupyterConfig.save_config**()

- **Parameters:**
    - None
- **Context:**
    - Used to create a configuration file that can be edited and imported. The configuration file is named by `JupyterConfig.config`, which defaults to the name of the notebook with the `.json` extension.


Run a parallel workflow from Jupyter.

**JupyterConfig.run**()

- **Parameters:**
    - None
- **Context:**
    - Used to run a parallel workflow, similar to the [`plantcv-run-workflow`](pipeline_parallel.md) utility.


There are additional methods (`find_notebook`, `nameScript`, `nameResults`, `notebook2script`, `nameConfig`, and `in_notebook`) which are used internally on initializing the `JupyterConfig` object to make and name the different files needed to run in parallel. These generally do not need to be interacted with directly and their generated values can be overwritten if desired.



### Attributes

* **notebook**: (str, default = `os.environ["JPY_SESSION_NAME"]`): Name of the Jupyter notebook file. This is used to name results, python script, and saved configuration json.

* **workflow**: (str, default = `self.nameScript()`): Name of the python workflow to run in parallel. Default is to name the python script with the same basename as the Jupyter notebook where this is initialized.

* **config**: (str, default = `self.nameConfig()`): Name of the configuration json file to save to run in parallel. Default is to name the json with the same basename as the Jupyter notebook where this is initialized.

* **analysis_script**: (bool, default = `self.notebook2script()`): True if the workflow file exists, false otherwise. Normally this should be True since `JupyterConfig.notebook2script()` writes the python script specified by `JupyterConfig.workflow`. 

Additional attributes are the same as those in the [`WorkflowConfig` documentation](parallel_config.md).


### Example

```python
from plantcv import plantcv as pcv 
from plantcv import parallel as pcvpar

jupcon = pcvpar.JupyterConfig()
jupcon.input_dir = "path/to/images"
jupcon.cluster_config["n_workers"] = 10
# ... other edits to defaults
jupcon.run()

# get arguments from plantcv.parallel.workflowinputs
args = pcvpar.workflow_inputs() # This is necessary for running the notebook in parallel
# read image
img, path, filename = pcv.readimage(filename=args.image1)
# other components of your workflow
# ...
# save results
pcv.outputs.save_results(filename= args.result, outformat="json")
```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/parallel/jupyterconfig.py)

