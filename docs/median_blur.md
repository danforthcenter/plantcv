## Median Blur

Applies a median blur filter. Applies median value to central pixel within a kernel size (ksize x ksize). 
The function is a wrapper for the OpenCV function [median blur](http://docs.opencv.org/doc/tutorials/imgproc/gausian_median_blur_bilateral_filter/gausian_median_blur_bilateral_filter.html_).  

**median_blur**(*img, ksize, device, debug=False*)**

**returns** device, blurred image

- **Parameters:**
    - img - img object
    - ksize - kernel size => ksize x ksize box, must be an odd value
    - device - Counter for image processing steps
    - debug- Default value is False, if True, median blurred intermediate image will be printed
- **Context:**
    - Used to reduce image noise
- **Example use:**
    - [Use In Tutorial](vis_tutorial.md)

**Thresholded image**

![Screenshot](img/documentation_images/median_blur/thresholded_image.jpg)

```python
import plantcv as pcv

# Apply median blur to a binary image that has been previously thresholded.
device, blur_5 = pcv.median_blur(img, 5, device, debug=True)
```

**Median blur (k = 5)**

![Screenshot](img/documentation_images/median_blur/median_blur5.jpg)

```python
import plantcv as pcv

# Apply median blur to a binary image that has been previously thresholded.
device, blur_11 = pcv.median_blur(img, 11, device, debug=True)
```

**Median blur (k = 11)**

![Screenshot](img/documentation_images/median_blur/median_blur11.jpg)
