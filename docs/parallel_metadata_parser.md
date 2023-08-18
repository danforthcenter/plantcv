## Metadata Parser

Reads metadata the from the input data directory.

**plantcv.parallel.metadata_parser**(*config*)

**returns** dataset (grouped Pandas DataFrame of image metadata)

- **Parameters:**
    - config   - plantcv.parallel.WorkflowConfig object
- **Context:**
    - This is one of the first steps built into the [PlantCV Workflow Parallelization](pipeline_parallel.md) feature.
    It reads metadata the from the input data directory and uses the outputs in the [job builder](parallel_job_builder.md) step.

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/parallel/parsers.py)
