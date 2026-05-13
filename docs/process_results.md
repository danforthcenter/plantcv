## Process Results

Process a directory of results files from running PlantCV over as many images as needed and create a formatted,
concatenated data output file. 

**plantcv.plantcv.process_results**(*input_dir=".", filename="results", outformat="csv"*)

**returns** none

- **Parameters:**
	- input_dir   - str or [plantcv.parallel.WorkflowConfig](parallel_config.md) object
	- filename    - str, filename to write out, ignored if `input_dir` is a `WorkflowConfig` object
	- outformat   - str, "csv" or "json". If "csv" (the default) then intermediate json used to make the csv files is not kept.
- **Context:**
    - This step is built into the [PlantCV Workflow Parallelization](pipeline_parallel.md) feature. Each workflow will save
    hierarchical data files using [`pcv.outputs.save_results`](outputs.md). `process_results` step takes place after all
    images have been analyzed and combines these single workflow data files into one text file that can be used as input for
    the [`json2csv`](json2csv.md) function. This can also be used outside of parallel workflows, for instance if you have
	run a jupyter based workflow several times.
- **Example use:**
    - Below 

```python
from plantcv import plantcv as pcv

pcv.process_results()

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/process_results.py)
