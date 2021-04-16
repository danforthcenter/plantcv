## Analyze NPQ Signal

Extract NPQ data of objects.

**plantcv.photosynthesis.analyze_npq**(*data, mask, bins=256, label="default"*)

**returns** NPQ analysis images (NPQ image, NPQ histogram)

- **Parameters:**
    - data - [X-array](http://xarray.pydata.org/en/stable/#) of binary image data
    - mask - binary mask of selected contours
    - bins - number of grayscale bins (0-256 for 8-bit images and 0 to 65,536), if you would like to bin data, you would alter this number (default bins=256)
    - label - Optional label parameter, modifies the variable name of observations recorded. (default `label="default"`)
- **Context:**
    - Used to extract NPQ per identified plant pixel.
    - Generates histogram of NPQ data.
    - Generates NPQ image.
- **Example use:**
    - Below
- **Output data stored:** Data ('npq_hist', 'npq_hist_peak', 'npq_median', 'fdark_passed_qc') automatically gets stored to the [`Outputs` class](outputs.md) when this function is ran. 
    These data can always get accessed during a workflow (example below). [Summary of Output Observations](output_measurements.md#summary-of-output-observations)


```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Analyze NPQ   
npq_images = pcv.photosynthesis.analyze_npq(data=data_array, mask=kept_mask, bins=256, label="fluor")

# Access data stored out from fluor_NPQ
npq_median = pcv.outputs.observations['fluor']['npq_median']['value']

# Store the two images
npq_img = npq_images[0]
npq_his = npq_images[1]

# Pseudocolor the Fv/Fm image
pseudo_img = pcv.pseudocolor(gray_img=npq_img, mask=kept_mask)

```

**Histogram of NPQ values**

![Screenshot](img/documentation_images/)

**Pseudocolored output image based on Fv/Fm**

![Screenshot](img/documentation_images/)

The grayscale NPQ image (returned to analysis_image) can be used with the [pcv.visualize.pseudocolor](visualize_pseudocolor.md) function
which allows the user to pick a colormap for plotting.

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/photosynthesis/analyze_npq.py)
