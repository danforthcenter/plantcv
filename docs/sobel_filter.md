## Sobel Filter

This is a filtering method used to identify and highlight coarse changes in pixel intensity based on the 1st derivative.

**sobel_filter**(*img, k, scale, device, debug=False*)

**returns** device, filtered image

- **Parameters:**
    - img - binary image object. This image will be returned after filling.
    - dx - derivative of x to analyze (1-3)
    - dy = derivative of y to analyze (1-3)
    - k - apertures size used to calculate 2nd derivative filter, specifies the size of the kernel (must be an odd integer: 1,3,5...)
    - scale - scaling factor applied (multiplied) to computed Laplacian values (scale = 1 is unscaled)
    - device - Counter for image processing steps
    - debug- Default value is False, if True, filled intermediate image will be printed 
- **Context:**
    - Used to define edges within and around objects

**Original grayscale image**

![Screenshot](img/documentation_images/sobel_filter/original_image.jpg)

```python
import plantcv as pcv

# Apply to a grayscale image
# Filtered image will highlight areas of coarse pixel intensity change based on 1st derivative
device, lp_img = pcv.sobel_filter(img, 1, 0, 1, device, debug=True)
device, lp_img = pcv.sobel_filter(img, 0, 1, 1, device, debug=True)
```

**Sobel filtered (x-axis)**

![Screenshot](img/documentation_images/sobel_filter/sobel-x.jpg)

**Sobel filtered (y-axis)**

![Screenshot](img/documentation_images/sobel_filter/sobel-y.jpg)
