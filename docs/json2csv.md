## Converting JSON results to CSV

The `plantcv.plantcv.json2csv` function is used to convert `PlantCV` results files from json into csv format. Single value traits and multi-value traits are split into two csv files, named with the appropriate suffix.
Most of the time you will not need to call this function directly as it is called by `plantcv.parallel.run_parallel` and through `plantcv.plantcv.process_results(..., outformat="csv")`.

Parallel results from [`plantcv-run-workflow`](pipeline_parallel.md) automatically are converted from json into 2 CSV files, one for single-value traits (where each object is described by one quantity like area or height) and one for multi-value traits (where each object is described by several quantities like hue).

**plantcv.plantcv.json2csv**(*json_file, csv_prefix*)

**returns** none

- **Parameters:**
	- json_file    - str, path to json file of plantcv results as saved by [pcv.outputs.save_results](outputs.md) or [pcv.process_results](pipeline_parallel.md).
	- csv_prefix   - str, prefix of output csv name. The two created files will be named `{csv_prefix}-single-value-traits.csv` and `{csv_prefix}-multi-value-traits.csv`.

- **Context:**
	- Used to convert json data to csv format for downstream analysis.
	
- **Example use:**
	- Below

```python
from plantcv import plantcv as pcv
pcv.json2csv("your_file.json", "new_file")

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/json2csv.py)
