## Process Results

Process a directory of results files from running PlantCV over as many images as needed and create a formatted,
concatenated data output file. 

**plantcv.parallel.process_results**(*config*)

**returns** none

- **Parameters:**
    - config   - plantcv.parallel.WorkflowConfig object
- **Context:**
    - This step is built into the [PlantCV Workflow Parallelization](pipeline_parallel.md) feature. Each workflow will save
    hierarchical data files using [`pcv.outputs.save_results`](outputs.md). `process_results` step takes place after all
    images have been analyzed and combines these single workflow data files into one text file that can be used as input for
    the [`json2csv`](json2csv.md) function. 
- **Example use:**
    - Below 

```python
from plantcv import parallel 

config = parallel.WorkflowConfig()
# edits to config

# Read in image
parallel.process_results(config)

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/parallel/process_results.py)
