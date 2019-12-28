## Multiprocess

Runs as many jobs as possible with the specified number of CPUs.

**plantcv.parallel.multiprocess**(*jobs, cpus*)

**returns** None

- **Parameters:**
    - jobs   - List of jobs
    - cpus - Number of CPUs 
- **Context:**
    - This is one of the last steps built into the [PlantCV Workflow Parallelization](pipeline_parallel.md) feature. 
    It executes jobs from a list created by the [job builder](parallel_job_builder.md) step. 
