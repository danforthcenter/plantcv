## Analyze PSII Signal

Extract Fv/Fm data of objects.

**plantcv.photosynthesis.analyze_fvfm**(*fdark, fmin, fmax, mask, bins=256, label="default"*)

**returns** PSII analysis images (Fv/Fm image, Fv/Fm histogram)

- **Parameters:**
    - fdark - image object, grayscale
    - fmin - image object  grayscale
    - fmax - image object, grayscale
    - mask - binary mask of selected contours
    - bins - number of grayscale bins (0-256 for 8-bit images and 0 to 65,536), if you would like to bin data, you would alter this number (default bins=256)
    - label - Optional label parameter, modifies the variable name of observations recorded. (default `label="default"`)
- **Context:**
    - Used to extract Fv/Fm or Fv'/Fm' per identified plant pixel.
    - Generates histogram of Fv/Fm data.
    - Generates Fv/Fm image.
- **Example use:**
    - [Use In PSII Tutorial](tutorials/psII_tutorial.md)
- **Output data stored:** Data ('fvfm_hist', 'fvfm_hist_peak', 'fvfm_median', 'fdark_passed_qc') automatically gets stored to the [`Outputs` class](outputs.md) when this function is ran. 
    These data can always get accessed during a workflow (example below). [Summary of Output Observations](output_measurements.md#summary-of-output-observations)

**Fdark image**

![Screenshot](img/documentation_images/fluor_fvfm/fdark.jpg)

**Fmin image**

![Screenshot](img/documentation_images/fluor_fvfm/fmin.jpg)

**Fmax image**

![Screenshot](img/documentation_images/fluor_fvfm/fmax.jpg)

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Analyze Fv/Fm    
fvfm_images = pcv.photosynthesis.analyze_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=kept_mask, bins=256, label="fluor")

# Access data stored out from fluor_fvfm
fvfm_median = pcv.outputs.observations['fluor']['fvfm_median']['value']

# Store the two images
fvfm_img = fvfm_images[0]
fvfm_his = fvfm_images[1]

# Pseudocolor the Fv/Fm image
pseudo_img = pcv.pseudocolor(gray_img=fvfm_img, mask=kept_mask)

```

**Histogram of Fv/Fm values**

![Screenshot](img/documentation_images/fluor_fvfm/fvfm_histogram.jpg)

**Pseudocolored output image based on Fv/Fm**

![Screenshot](img/documentation_images/pseudocolor/pseudo_img.jpg)

The grayscale Fv/Fm image (returned to analysis_image) can be used with the [pcv.visualize.pseudocolor](visualize_pseudocolor.md) function
which allows the user to pick a colormap for plotting.

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/photosynthesis/analyze_fvfm.py)
