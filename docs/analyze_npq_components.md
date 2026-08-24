## Analyze Components of Nonphotochemical Quenching of Photosystem II

Where the [main nonphotochemical quenching (NPQ) analysis function](analyze_npq.md) returns NPQ of Photosystem II (PSII)
this function calculates various other components of nophotochemical quenching. See details for explanations of the
calculated components.

**plantcv.analyze.npq_componeents**(*ps, labeled_mask, n_labels=1, label=None*)

**returns** list of dictionaries containing numpy.ndarrays

- **Parameters:**
    - ps - PSII Data object containing `ojip_dark` and `ojip_light` data from `npq` or `psl` and `psd` images.
    - labeled_mask - Labeled mask of objects (32-bit).
    - n_labels - Total number expected individual objects (default = 1).
    - label - Optional label parameter, modifies the variable name of observations recorded. Can be a prefix or list (default = pcv.params.sample_label).
- **Context:**
    - Used to extract NPQ components per identified plant object.
    - Calculates averages of NPQ component values.
    - Generates an NPQ image.
- **Example use:**
    - below
- **Output data stored:** Data are automatically stored to the 
  [`Outputs` class](outputs.md) labeled as `mean_{METRIC}_{TIME}` when this function is run. These data can be accessed during a workflow (example below). `{measurement_label}` is automatically created when importing the dataset, e.g. with `read_cropreporter()` but can be overwritten with `measurement_labels` argument.
  [Summary of Output Observations](output_measurements.md#summary-of-output-observations)

- **Details**
    - **qP** - Fraction of open reaction centers (based on puddle mode)/ Photochemical quenching. Calculated as `(Fm'-Fp)/(Fm'-F0')`
    - **qN** - Term for quantifying non-photochemical quenching. Calculated as `1 - (Fm'-F0')/(Fm-F0)`. Bounded [0, 1].
    - **qL** - Fraction of open reaction centers (based on lake mode)/ Photochemical quenching. Calculated as `qP * F0'/Fp`
    - **qI** - Slow relaxing component of non-photochemical quenching. Calculated as `(Fm-Fm'')/Fm''`
    - **qE** - Fast relaxing component of non-photochemical quenching. Calculated as `Fm * (Fm''-Fm')/(Fm'' * Fm')`
    - **phiNO** - Quantum yield of non-regulated energy dissipation. Calculated as `1 / (NPQ+1+ql * Fm/F0)` where `NPQ` is calculated as `Fm/Fmp - 1`.
    - **phiNPQ** - Quantum yield of non-photochemical quenching. Calculated as `1-Fq'/Fm'-phiNO`

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"
# Optionally, set a sample label name
pcv.params.sample_label = "plant"

# Analyze NPQ components
l = pcv.analyze.npq_components(ps=ps, labeled_mask=kept_mask)

# Access the qP mean value
qP_median = pcv.outputs.observations['plant_1']['qP_median_t0']['value']

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/analyze/npq_components.py)
