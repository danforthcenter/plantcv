## Analyze PSII Signal

Extract Fv/Fm data of objects.

**plantcv.fluor_fvfm**(*fdark, fmin, fmax, mask, bins=256*)

**returns** PSII analysis images (Fv image, Fv/Fm histogram)

- **Parameters:**
    - fdark - image object, grayscale
    - fmin - image object  grayscale
    - fmax - image object, grayscale
    - mask - binary mask of selected contours
    - bins - number of grayscale bins (0-256 for 8-bit images and 0 to 65,536), if you would like to bin data, you would alter this number (default bins=256)
- **Context:**
    - Used to extract fv/fm per identified plant pixel.
    - Generates histogram of fv/fm data.
    - Generates fv/fm image.
    - Data automatically gets stored into the [Outputs class](outputs.md). Users can look at the data collected at any point during 
    the workflow by using [pcv.print_results](print_results.md) which prints all stored data to a .json file.
- **Example use:**
    - [Use In PSII Tutorial](psII_tutorial.md)
- **Output data stored:** [Summary of Output Observations](output_measurements.md#summary-of-output-observations)

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
fvfm_images = pcv.fluor_fvfm(fdark, fmin, fmax, kept_mask, 256)

# Store the two images
fv_im g= fvfm_images[0]
fvfm_his = fvfm_images[1]

# Pseudocolor the Fv/Fm image
pseudo_img = pcv.pseudocolor(gray_img=fv_img, mask=kept_mask)

```

**Histogram of Fv/Fm values**

![Screenshot](img/documentation_images/fluor_fvfm/fvfm_histogram.jpg)

**Pseudocolored output image based on Fv/Fm**

![Screenshot](img/documentation_images/pseudocolor/pseudo_img.jpg)

The grayscale Fv/Fm image (returned to analysis_image) can be used with the [pcv.visualize.pseudocolor](visualize_pseudocolor.md) function
which allows the user to pick a colormap for plotting.
