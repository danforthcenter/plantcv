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
    - tmp_dir (str, default = `None`): path/name of parent folder for the temporary directory, uses system default temporary directory when `None`
    - start_date (int, default = 1): start date used to filter images. Images will be analyzed that are newer than the start date. string format matching timestampformat
    - end_date (int, default = `None`): end date used to filter images. Images will be analyzed that are older than the end date, unless `None`. string format matching timestampformat
    - imgformat (str, default = "png"): image file format/extension
    - delimiter (str, default = "_"): image filename metadata term delimiter character. Alternatively, a regular expression for parsing filename metadata
    - metadata_filters (dict, default = `None`): a dictionary of metadata terms (keys) and values, images will be analyzed that have the associated term and value
    - group_by (list, default = `None`): a list of metadata terms to treat as a group
    - timestampformat (str, default = '%Y-%m-%d %H:%M:%S.%f'): a date format code compatible with strptime C library. see [strptime docs](https://docs.python.org/3.7/library/datetime.html#strftime-and-strptime-behavior) for supported codes.
    - writeimg (bool, default = `False`): save analysis images to `output_dir` if `True`
    - other_args (list, default = `[]`): list of other arguments required by the workflow (e.g. ["--input1", "value1", "--input2", "value2"])
    - coprocess (str, default = `None`): coprocess the specified imgtype with the imgtype specified in metadata_filters (e.g. coprocess NIR images with VIS)
    - cluster (str, default = "LocalCluster"): LocalCluster will run PlantCV workflows on a single machine. All valid options currently are: "LocalCluster",
    "HTCondorCluster", "LSFCluster", "MoabCluster", "OARCluster", "PBSCluster", "SGECluster", and "SLURMCluster". See [Dask-Jobqueue](https://jobqueue.dask.org/) for more details.
    - cluster_config (dict, default: see below ): a dictionary of parameters and values used to configure the cluster for parallel processing locally or remotely.
    - metadata_terms (dict, default: as-is): a dictionary of metadata terms used to assign values in image filenames (or metadata files) to metadata terms (should not be modified).
- **Context:**
    - Used to configure parallelization of PlantCV workflows.

### Cluster configuration

[Dask](https://dask.org/) is used to parallelize PlantCV image analysis workflows using both `dask.distributed` and `dask_jobqueue`.
In Dask a cluster is a type of computing environment, which could either be local or a remote resource (in this case a computing cluster managed by a scheduler).

First, we need to define the type of cluster to use. `LocalCluster` is the simplest setup and creates a pool of computing resources on the machine where we will
run the `plantcv.parallel` functions.

!!! note
    The concept of "local" and "remote" is relative to the PlantCV program, not the user. In other words, LocalCluster
    could be used to run PlantCV on a single remote machine if this task were submitted to a remote computing environment
    (e.g. cloud, campus cluster, etc.). This is the standard approach PlantCV has used in older versions.

All other currently supported cluster types listed above allow the user to configure PlantCV to interface with a job
scheduling platform and distribute image analysis workflows across a computing resource (e.g. campus cluster).

!!! warning
    The cluster name supplied to the `cluster` setting must match one of the keywords above exactly (case-sensitive).

After defining the cluster, parameters are used to define the size of and request resources from the given computing environment.
These settings are defined in the `cluster_config` parameter. We define by default the following parameters:

- n_workers (int, required, default = 1): the number of workers/slots to request from the cluster. Because we generally use
1 CPU per image analysis workflow, this is effectively the maximum number of concurrently running workflows.
- cores (int, required, default = 1): the number of compute cores per workflow. This should be left as 1 unless a workflow is designed to use multiple CPUs/cores/threads.
- memory (str, required, default = "1GB"): the amount of memory/RAM used per workflow. Can be set as a number plus units (KB, MB, GB, etc.).
- disk (str, required, default = "1GB"): the amount of disk space used per workflow. Can be set as a number plus units (KB, MB, GB, etc.).
- log_directory (str, optional, default = `None`): directory where worker logs are stored. Can be set to a path or environmental variable.
- local_directory (str, optional, default = `None`): dask working directory location. Can be set to a path of environmental variable.
- job_extra (dict, optional, default = `None`): extra parameters sent to the scheduler. Specified as a dictionary of key-value pairs (e.g. `{"getenv": "true"}`).

!!! note
    `n_workers` is the only parameter used by `LocalCluster`, all others are currently ignored. `n_workers`, `cores`,
    `memory`, and `disk` are required by the other clusters. All other parameters are optional. Additional parameters
    defined in the [dask-jobqueu API](https://jobqueue.dask.org/en/latest/api.html) can be supplied.

### Example

```python
import plantcv.parallel

# Create a WorkflowConfig instance
config = plantcv.parallel.WorkflowConfig()
# Create a template configuration file
config.save_config(config_file="my_config.json")
# Edit configuration file as needed
# Import the configuration file
config.import_config(config_file="my_config.json")
# Check for errors
passed = config.validate_config()

# Change configuration values directly in Python
config.input_dir = "./my_images"
```
