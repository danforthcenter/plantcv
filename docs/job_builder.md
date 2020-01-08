## Job Builder

The job builder step in [PlantCV Workflow Parallelization](pipeline_parallel.md) builds a list of image processing jobs.

**plantcv.parallel.job_builder**(*meta, valid_meta, workflow, job_dir, out_dir, coprocess=None, other_args="", writeimg=False*)

**returns** none

- **Parameters:**
    - meta   - Dictionary of processed image metadata
    - valid_meta - Dictionary of valid metadata keys
    - workflow - PlantCV image processing workflow script file
    - job_dir - Intermediate file output directory
    - out_dir - Output images directory
    - coprocess - Coprocess the specified imgtype with the imgtype specified in meta_filters (default: None) 
    - other_args - String of additional arguments to be passed to the workflow script (default: "")
    - writeimg - Boolean that specifies whether output images should be created or not (default: False) 
- **Context:**
    - This step is built into the [PlantCV Workflow Parallelization](pipeline_parallel.md) feature. It builds a list of image processing 
    jobs which is the input for the [multiprocess](multiprocess.md) step in workflow parallelization. 

