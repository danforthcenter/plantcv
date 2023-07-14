## Job Builder

The job builder step in [PlantCV Workflow Parallelization](pipeline_parallel.md) builds a list of image processing jobs.

**plantcv.parallel.job_builder**(*meta, config*)

**returns** none

- **Parameters:**
    - meta   - Grouped Pandas DataFrame of processed image metadata
    - config - plantcv.parallel.WorkflowConfig object
- **Context:**
    - This step is built into the [PlantCV Workflow Parallelization](pipeline_parallel.md) feature. It builds a list of image processing 
    jobs which is the input for the [multiprocess](parallel_multiprocess.md) step in workflow parallelization. 

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/parallel/job_builder.py)
