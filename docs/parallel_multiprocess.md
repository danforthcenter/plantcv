## Multiprocess

Runs PlantCV workflows in parallel locally or in a distributed computing resource.

**plantcv.parallel.create_dask_cluster**(*cluster, cluster_config*)

**returns** Dask cluster client

- **Parameters:**
    - cluster   - Name of the cluster type [see WorkflowConfig](parallel_config.md).
    - cluster_config - Dictionary of cluster configuration parameters [see WorkflowConfig](parallel_config.md).
- **Context:**
    - Used to create a computing cluster resource (including local environment) for [PlantCV Workflow Parallelization](pipeline_parallel.md).

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/parallel/multiprocess.py)


**plantcv.parallel.multiprocess**(*jobs, client*)

**returns** None

- **Parameters:**
    - jobs   - List of jobs
    - client - A Dask cluster client object that connects to the requested computing cluster environment.
- **Context:**
    - This is one of the last steps built into the [PlantCV Workflow Parallelization](pipeline_parallel.md) feature. 
    It executes jobs from a list created by the [job builder](parallel_job_builder.md) step. 

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/parallel/multiprocess.py)
