## Converting JSON results to CSV

The `plantcv.parallel.json2csv` function is used to convert `PlantCV` results files from json into csv format.
Most of the time you will not need to call this function directly.

Parallel results from [`plantcv-run-workflow`](pipeline_parallel.md) automatically are converted from json into 2 CSV files, one for single-value traits (where each object is described by one quantity like area or height) and one for multi-value traits (where each object is described by several quantities like hue).

For other json results you can use this function to make tabular data:

```python
from plantcv import parallel as pcvpar
pcvpar.json2csv("your_file.json", "new_file.csv")

```
