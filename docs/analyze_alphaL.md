## Analyze leaf light absorption

Calculate AlphaL leaf absorption: 1 - (red / farred)

**plantcv.analyze.alphaL**(*ps, labeled_mask, n_labels=1, measurement_labels=None, label=None, min_bin=-1, max_bin=1*)

**returns** AlphaL matrix, a `numpy.ndarray`

- **Parameters:**
    - ps - `PSII_data` instance (from [read_cropreporter](photosynthesis_read_cropreporter.md)) containing `aph` data.
    - labeled_mask - Labeled mask of objects (32-bit).
    - n_labels - Total number expected individual objects (default = 1).
    - measurement_labels - list of label(s) for each measurement, modifies the default variable names of observations. must have same length as number of measurements in the frame of ps being used.
    - label - Optional label parameter, modifies the variable name of observations recorded. Can be a prefix or list (default = pcv.params.sample_label).
	- min_bin - Optional, minimum bin label. Defaults to -1.
	- max_bin - Optional, maximum bin label. Defaults to 1.

- **Context:**
    - Calculates mean, median, min, max, mode, and histogram of alphaL for each object in the labeled mask.

- **Example use:**
   - Below
- **Output data stored:** Mean, median, min, max, mode, and histogram of alphaL for each object in the labeled mask are stored to the [`Outputs` class](outputs.md) when this function is ran.

```python

from plantcv import plantcv as pcv

pcv.params.debug = "plot"
# Optionally, set a sample label name
pcv.params.sample_label = "plant"

pcv.analyze.alphaL(ps, labeled_mask=mask)

```


**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/analyze/alphaL.py)
