## Analyze Nonphotochemical Quenching of Photosystem II without dark measurements

Extract estimates of the nonphotochemical quenching (NPQ) of Photosystem II (PSII) without dark-adjusted frames. 
Calculates  `4.88 / (Fmp / F0p - 1) - 1` data from a masked region for each `Fmp+` frame from PAM time data.


**plantcv.analyze.npqfast**(*ps, labeled_mask, n_labels=1, min_bin=0, max_bin="auto", measurement_labels=None, label=None*)

**returns** NPQ DataArray and Histograms of NPQ values

- **Parameters:**
    - ps - PSII Data object containing `PMT` pam time data.
    - labeled_mask - Labeled mask of objects (32-bit).
    - n_labels - Total number expected individual objects (default = 1).
    - min_bin - minimum bin value ("auto" or user input minimum value - must be an integer). (default `min_bin=0`)
    - max_bin - maximum bin value ("auto" or user input maximum value - must be an integer). (default `max_bin="auto"`)
    - measurement_labels - list of label(s) for each measurement in `ojip_light` data, modifies the variable name of observations recorded
    - label - Optional label parameter, modifies the variable name of observations recorded. Can be a prefix or list (default = pcv.params.sample_label).
- **Context:**
    - Used to extract NPQ per identified plant pixel.
    - Generates histogram of NPQ values.
    - Generates an NPQ image.
- **Example use:**
    - [Use In PSII Tutorial](https://plantcv.org/tutorials/photosynthesis)
- **Output data stored:** Data ('npqfast_hist_{measurement_label}', 'npqfast_max_{measurement_label}', 'npqfast_median_{measurement_label}') are automatically stored to the 
  [`Outputs` class](outputs.md) when this function is run. These data can be accessed during a workflow (example below). `{measurement_label}` is automatically created when importing the dataset, e.g. with `read_cropreporter()` but can be overwritten with `measurement_labels` argument.
  [Summary of Output Observations](output_measurements.md#summary-of-output-observations)


```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"
# Optionally, set a sample label name
pcv.params.sample_label = "plant"

# Analyze NPQ   
npq, npq_hist = pcv.analyze.npqfast(ps=ps, labeled_mask=kept_mask)

# Access the NPQ median value
# the default measurement label for cropreporter data is t1
npq_median = pcv.outputs.observations['plant_1']['npqfast_median_t1']['value']

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/analyze/npq_fast.py)
