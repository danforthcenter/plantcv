## Logical Operations - And

Join two images using the bitwise AND operator. Images must be the same size. 
This is a wrapper for the Opencv Function [bitwise_and](http://docs.opencv.org/2.4/modules/core/doc/operations_on_arrays.html#bitwise-and).  

**logical_and**(*img1, img2, device, debug=None*)

**returns** device, 'and' image

- **Parameters:**
    - img1 - image object 1.
    - img2 - image object 2.
    - device - Counter for image processing steps
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Used to combine to images. Very useful when combining image channels that have been thresholded seperately.
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)

**Input binary image 1**

![Screenshot](img/documentation_images/logical_and/image1.jpg)

**Input binary image 2**

![Screenshot](img/documentation_images/logical_and/image2.jpg)

```python
from plantcv import plantcv as pcv

# Combine two images that have had different thresholds applied to them.
# For logical 'and' operation object pixel must be in both images to be included in 'and' image.
device, and_image = pcv.logical_and(s_threshold, b_threshold, device, debug="print")
```

**Combined image**

![Screenshot](img/documentation_images/logical_and/joined.jpg)
