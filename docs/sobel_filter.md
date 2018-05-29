## Sobel Filter

This is a filtering method used to identify and highlight coarse changes in pixel intensity based on the 1st derivative.

**sobel_filter**(*img, dx,dy,k, device, debug=None*)

**returns** device, filtered image

- **Parameters:**
    - img - binary image object. This image will be returned after filling.
    - dx - derivative of x to analyze (0-3)
    - dy - derivative of y to analyze (0-3)
    - k - apertures size used to calculate 2nd derivative filter, specifies the size of the kernel (must be an odd integer: 1,3,5...)
    - device - Counter for image processing steps
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None 
- **Context:**
    - Used to define edges within and around objects
- **Example use:**
    - [Use In NIR Tutorial](nir_tutorial.md)

**Original grayscale image**

![Screenshot](img/documentation_images/sobel_filter/original_image.jpg)

```python
from plantcv import base as pcv

# Apply to a grayscale image
# Filtered image will highlight areas of coarse pixel intensity change based on 1st derivative
device, lp_img = pcv.sobel_filter(img, 1, 0, 1, device, debug="print")
device, lp_img = pcv.sobel_filter(img, 0, 1, 1, device, debug="print")
```

**Sobel filtered (x-axis)**

![Screenshot](img/documentation_images/sobel_filter/sobel-x.jpg)

**Sobel filtered (y-axis)**

![Screenshot](img/documentation_images/sobel_filter/sobel-y.jpg)
