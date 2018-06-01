## Median Blur

Applies a median blur filter. Applies median value to central pixel within a kernel size (ksize x ksize). 
The function is a wrapper for the OpenCV function [median blur](http://docs.opencv.org/doc/tutorials/imgproc/gausian_median_blur_bilateral_filter/gausian_median_blur_bilateral_filter.html_).  

**median_blur**(*img, ksize, device, debug=None*)**

**returns** device, blurred image

- **Parameters:**
    - img - img object
    - ksize - kernel size => ksize x ksize box, must be an odd value
    - device - Counter for image processing steps
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Used to reduce image noise
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)
    - [Use In NIR Tutorial](nir_tutorial.md)
    - [Use In PSII Tutorial](psII_tutorial.md) 

**Thresholded image**

![Screenshot](img/documentation_images/median_blur/thresholded_image.jpg)

```python
from plantcv import plantcv as pcv

# Apply median blur to a binary image that has been previously thresholded.
device, blur_5 = pcv.median_blur(img, 5, device, debug="print")
```

**Median blur (k = 5)**

![Screenshot](img/documentation_images/median_blur/median_blur5.jpg)

```python
from plantcv import plantcv as pcv

# Apply median blur to a binary image that has been previously thresholded.
device, blur_11 = pcv.median_blur(img, 11, device, debug="print")
```

**Median blur (k = 11)**

![Screenshot](img/documentation_images/median_blur/median_blur11.jpg)
