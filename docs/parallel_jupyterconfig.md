## Running in Parallel from a Jupyter notebook

The `jupyterconfig` class is very similar to the [`WorkflowConfig` class](parallel_config.md) and is used to configure a parallel workflow directly from a Jupyter notebook.

### Quick Start

Initializing a `jupyterconfig` object in a Jupyter notebook will immediately use `nbconvert` to create a python script version of the workflow. Similar to `WorkflowConfig` objects you can overwrite default attributes to meet your particular needs. Once your edits are done the `run` method will run the workflow in parallel.

```python
from plantcv import parallel as pcvpar

jupcon = pcvpar.jupyterconfig()
jupcon.input_dir = "path/to/images"
# ... other edits
jupcon.run()
```

*class* **plantcv.parallel.jupyterconfig**

### Class methods

Inspect the input dataset.

**jupyterconfig.inspect_dataset**()

- **Parameters:**
    - None
- **Context:**
    - Used to check which images will be found by the current configuration using [`inspect_dataset`](parallel_inspect_config.md).


Save a configuration file that can be modified and imported to run workflows in parallel.

**jupyterconfig.save_config**()

- **Parameters:**
    - None
- **Context:**
    - Used to create a configuration file that can be edited and imported. The configuration file is named by `jupyterconfig.config`, which defaults to the name of the notebook with the `.json` extension.


Run a parallel workflow from Jupyter.

**jupyterconfig.run**()

- **Parameters:**
    - None
- **Context:**
    - Used to run a parallel workflow, similar to the [`plantcv-run-workflow`](pipeline_parallel.md) utility.


There are additional methods (`find_notebook`, `nameScript`, `nameResults`, `notebook2script`, `nameConfig`, and `in_notebook`) which are used internally on initializing the `jupyterconfig` object to make and name the different files needed to run in parallel.



### Attributes

* **notebook**: (str, default = os.environ["JPY_SESSION_NAME"]): Name of the Jupyter notebook file. This is used to name results, python script, and saved configuration json.

* **workflow**: (str, default = self.nameScript()): Name of the python workflow to run in parallel. Default is to name the python script with the same basename as the Jupyter notebook where this is initialized.

* **config**: (str, default = self.nameConfig()): Name of the configuration json file to save to run in parallel. Default is to name the json with the same basename as the Jupyter notebook where this is initialized.

* **analysis_script**: (bool, default = self.notebook2script()): True if the workflow file exists, false otherwise. Normally this should be True since `jupyterconfig.notebook2script()` writes the python script specified by `jupyterconfig.workflow`. 

Additional attributes are the same as those in the [`WorkflowConfig` documentation](parallel_config.md).
