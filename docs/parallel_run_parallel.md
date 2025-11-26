## Run Parallel Workflow

Runs a workflow in parallel based off of a configuration file.

**plantcv.parallel.run_parallel**(*config*)

**returns** none

- **Parameters:**
	- config   - [plantcv.parallel.WorkflowConfig](parallel_config.md) object
- **Context:**
    - This function is built into the [PlantCV Workflow Parallelization](pipeline_parallel.md) pipeline and is called whenever you use `plantcv-run-workflow` on the command line or `jupyterconfig.run` in jupyter. You should not have to interact with this function directly but it is documented here for clarity. The `run_parallel` function calls several functions that are available in `plantcv.parallel` which users also are not expected to directly interact with.

- **Details:**

	- This function calls several other functions exported from `plantcv.parallel` and `plantcv.plantcv` which users do not have to directly interact with.
	- **1:** The [`plantcv.parallel.metadata_parser`](parallel_metadata_parser.md) function is used to find input images and parse their metadata.
	- **2:** The [`plantcv.parallel.job_builder`](parallel_job_builder.md) function is used to build a list of jobs with their input parameters.
	- **3:** The [`plantcv.parallel.multiprocess`](parallel_multiprocess.md) function makes a dask cluster and run each job specified in the job list.
	- **4:** [`plantcv.plantcv.process_results`](process_results.md) is used to collect each job's results file into a single json file.
	- **5:** [`plantcv.plantcv.json2csv`](json2csv.md) converts the collated json file into two csv files.

- **Example use:**
    - Below 

```python
from plantcv.parallel import run_parallel

run_parallel(config)

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/parallel/run_parallel.py)
