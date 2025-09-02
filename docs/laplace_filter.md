## Laplace Filter

This is a filtering method used to identify and highlight fine edges based on the 2nd derivative.

**plantcv.laplace_filter**(*gray_img, ksize, scale, roi=None*)

**returns** filtered image

- **Parameters:**
    - gray_img - Grayscale image data
    - ksize - apertures size used to calculate 2nd derivative filter, specifies the size of the kernel (must be an odd integer: 1,3,5...)
    - scale - scaling factor applied (multiplied) to computed Laplacian values (scale = 1 is unscaled)
	- roi - Optional rectangular ROI as returned by [`pcv.roi.rectangle`](roi_rectangle.md) within which to apply this function. (default = None, which uses the entire image)

- **Context:**
    - Used to define edges around objects
- **Example use:**
    - Below

**Input grayscale image**

![Screenshot](img/documentation_images/laplace_filter/grayscale_image.jpg)

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

# Apply to a grayscale image
# Filtered image will highlight areas of rapid pixel intensity change
lp_img = pcv.laplace_filter(gray_img=gray_img, ksize=1, scale=1)

```

**Image after Laplace filter**

![Screenshot](img/documentation_images/laplace_filter/lp_filtered.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/laplace_filter.py)
