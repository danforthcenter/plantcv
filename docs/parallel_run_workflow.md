## Run a PlantCV workflow in parallel

Identifies images in a dataset to analyze and runs them in parallel using the specified workflow.

**plantcv.parallel.run_workflow**(*config, workflow*)

- **Parameters:**
    - config - Input parameters defined in an instance of *class plantcv.parallel.Config*
    - workflow - A PlantCV workflow script
    
- **Context:**
    - Runs the entire PlantCV workflow parallelization framework [PlantCV Workflow Parallelization](pipeline_parallel.md). It is a wrapper/helper function around the entire `plantcv.parallel` subpackage. 
