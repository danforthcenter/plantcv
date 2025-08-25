## Analyze radial percentile

This function calculates the average value of pixels within a cutoff threshold from the center of an object and writes 
the values out to the [Outputs class](outputs.md).  


**plantcv.analyze.radial_percentile**(*img, mask, roi=None, percentile=50, label="default"*)
**returns** List of average values for either grayscale or RGB

- **Parameters:**
    - img - RGB or grayscale image.
    - mask - Binary mask.
    - roi - Optional ROIs for calculating on multiple objects in an image.
    - percentile - cutoff for considering pixels in the average. Expressed as a percent of maximum distance from the object's center
    - label - Optional label parameter, modifies the variable name of observations recorded. Can be a prefix or list (default = pcv.params.sample_label).
- **Outputs:**
    - A list of average values for RGB or gray channels for each object (if ROIs are provided), or for the single object in the image. 
- **Example use:**
    - Useful for calculating the intensity of the middle of seeds from an X-ray image.
    - Also could be useful in determining if there are color differences in the middle of a plant rosette. 

- **Output data stored:** Data ('gray_frequencies', 'gray_mean', 'gray_median', 'gray_stdev') automatically gets stored to
the [`Outputs` class](outputs.md) when this function is ran. These data can always get accessed during a workflow (example
below). For more detail about data output see [Summary of Output Observations](output_measurements.md#summary-of-output-observations)

**Original grayscale image**

![Screenshot](img/documentation_images/analyze_grayscale/original_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "plot"
# Optionally, set a sample label name
pcv.params.sample_label = "plant"

# Caclulates the proportion of pixels that fall into a signal bin and writes the values to a file.
# Also provides a histogram of this data
analysis_image  = pcv.analyze.grayscale(gray_img=gray_img, labeled_mask=mask, n_labels=1, bins=100)

# Access data stored out from analyze.grayscale
nir_frequencies = pcv.outputs.observations['plant_1']['gray_frequencies']['value']

```


**Near-infrared signal histogram**

![Screenshot](img/documentation_images/analyze_grayscale/nir_histogram.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/analyze/grayscale.py)
