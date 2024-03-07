## Analyze the Spatial Distribution of Object(s)

Spatial distribution analysis outputs numeric properties describing the pixel distribution in the X and Y dimension for plants, roots, flowers, etc. In particular, this application can be useful for analyzing the distribution of roots in soil. 
 
**plantcv.analyze.distribution**(*labeled_mask, bin_size_x=100, bin_size_y=100, label=None*)

**returns** Ridgeline plot of histograms of pixel distribution in the X and Y dimensions

- **Parameters:**
    - labeled_mask - Labeled mask of objects (32-bit, output from [`pcv.create_labels`](create_labels.md) or [`pcv.roi.filter`](roi_filter.md)).
    - bin_size_x - Optional parameter, defines the size of the bin in pixels in the X direction. 
    - bin_size_y - Optional parameter, defines the size of the bin in pixels in the Y direction. 
    - label - Optional label parameter, modifies the variable name of observations recorded. Can be a prefix or list (default = pcv.params.sample_label).
- **Context:**
    - Used to output distribution of object(s) (labeled regions) in the X and Y dimensions of an image. 
- **Example use:**

- **Output data stored:** Data ('X_frequencies', 'Y_frequencies', 'X_distribution_mean', 'X_distribution_std', 'X_distribution_median', 'Y_distribution_mean', 'Y_distribution_std', 'Y_distribution_median') 
    automatically gets stored to the [`Outputs` class](outputs.md) when this function is ran. 
    These data can always get accessed during a workflow (example below). For more detail about data output see [Summary of Output Observations](output_measurements.md#summary-of-output-observations)
    
**Original image**



```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "plot"
# Optionally, set a sample label name
pcv.params.sample_label = "plant"

# Characterize object shapes
distribution_image = pcv.analyze.distribution(labeled_mask=mask, bin_size = 100, n_labels=1)

# Access data stored out from analyze.distribution
X_distribution_mean = pcv.outputs.observations['plant_1']['X_distribution_mean']['value']

```

**Histograms of X distribution values**




**Source Code:** 
