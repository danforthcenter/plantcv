## Parallel workflow configuration class

`WorkflowConfig` is a class that stores parallel workflow configuration parameters. Configurations can be saved/imported
to run workflows in parallel.

*class* **plantcv.parallel.WorkflowConfig**

**Class methods**

Save a configuration file that can be modified and imported to run workflows in parallel.

**WorkflowConfig.save_config**(*config_file*)

- **Parameters:**
    - config_file (str, required): path/name of output configuration file
- **Context:**
    - Used to create a configuration file that can be edited and imported

Import a configuration file. 

**WorkflowConfig.import_config**(*config_file*)

- **Parameters:**
    - config_file (str, required): path/name of input configuration file
- **Context:**
    - Used to import configuration settings from a file

Validate parameters/structure of configuration data.

**WorkflowConfig.validate_config**()

- **Parameters:**
    - None
- **Context:**
    - Used to run validation checks on configuration settings

- **Parameters:**
    - input_dir (str, required): path/name of input images directory (validates that it exists)
    - json (str, required): path/name of output JSON data file (appends new data if it already exists)
    - filename_metadata (list, required): list of metadata terms used to construct filenames
    - workflow (str, required): path/name of user-defined PlantCV workflow Python script (validates that it exists)
    - output_dir (str, default = "."): path/name of output directory where images will be saved
    - tmp_dir (str, default = `None`): path/name of parent folder for the temporary directory, current working directory when `None`
    - processes (int, default = 1): number of parallel processes
    - start_date (int, default = 1): start date in Unix time used to filter images. Images will be analyzed that are newer than the start date
    - end_date (int, default = `None`): end date in Unix time used to filter images. Images will be analyzed that are older than the end date, unless `None`
    - imgformat (str, default = "png"): image file format/extension
    - delimiter (str, default = "_"): image filename metadata term delimiter character. Alternatively, a regular expression for parsing filename metadata
    - metadata_filters (dict, default = `None`): a dictionary of metadata terms (keys) and values, images will be analyzed that have the associated term and value
    - group_by (list, default = `None`): a list of metadata terms to treat as a group
    - timestampformat (str, default = '%Y-%m-%d %H:%M:%S.%f'): a date format code compatible with strptime C library
    - writeimg (bool, default = `False`): save analysis images to `output_dir` if `True`
    - other_args (list, default = `None`): other arguments required by the workflow
    - coprocess (str, default = `None`): coprocess the specified imgtype with the imgtype specified in metadata_filters (e.g. coprocess NIR images with VIS)
- **Context:**
    - Used to configure parallelization of PlantCV workflows.

### Example

```python
import plantcv.parallel

# Create a WorkflowConfig instance
wf = plantcv.parallel.WorkflowConfig()
# Create a template configuration file
wf.create_template(config_file="my_config.json")
# Edit configuration file as needed
# Import the configuration file
wf.import_config_file(config_file="my_config.json")
# Check for errors
errors = wf.validate_config()
# Run a workflow in parallel
plantcv.parallel.run_workflow(config=wf.config, workflow=workflow)

```
