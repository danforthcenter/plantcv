## Standard Deviation Filter 

Creates a grayscale image of pixelwise standard deviation from a grayscale image.


**plantcv.stdev_filter**(*img, ksize, borders='nearest'*)

**returns** stdev image

- **Parameters:**
    - img - Grayscale or RGB image data
    - ksize - Kernel size for texture measure calculation
    - borders - How the array borders are handled, either ‘reflect’, ‘constant’, ‘nearest’ (default), ‘mirror’, or ‘wrap’
- **Note:**
    - This function is computationally expensive than other filters and will likely take several moments to run (even longer if images are large).
- **Example use:**
    - Below

**Original image**

![Screenshot](img/documentation_images/stdev_filter/cropped_plantago.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "plot"

# Create binary image from a gray image based on texture values.
texture_img_11 = pcv.stdev_filter(img=gray_img, ksize=11, borders='nearest')
texture_img_51 = pcv.stdev_filter(img=gray_img, ksize=45, borders='nearest')
texture_img_111 = pcv.stdev_filter(img=gray_img, ksize=111, borders='nearest')

                                    
```

**Standard deviation image (ksize=11)**

![Screenshot](img/documentation_images/stdev_filter/stdev_img11.jpg)

**Standard deviation image (ksize=45)**

![Screenshot](img/documentation_images/stdev_filter/stdev_img45.jpg)

**Standard deviation image (ksize=111)**

![Screenshot](img/documentation_images/stdev_filter/stdev_img111.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/stdev_filter.py)
