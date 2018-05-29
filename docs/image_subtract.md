## Image Subtract

Obtain a image of the pixelwise input values within two image files. 
This is a wrapper for the OpenCV function [subtract](http://docs.opencv.org/2.4/modules/core/doc/operations_on_arrays.html#subtract).

**image_subtract**(*img, img2, device, debug=None*)

**returns** device, subtracted image

- **Parameters:**
    - img - image to be analyzed
    - img2 - image to subtract
    - device - Counter for image processing steps
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Get features that are different between images
- **Example use:**
    - [Use In NIR Tutorial](nir_tutorial.md)

**Original grayscale image (image 1)**

![Screenshot](img/documentation_images/image_subtract/original_image.jpg)

**Image to be subtracted (image 2)**

![Screenshot](img/documentation_images/image_subtract/image2.jpg)

```python
from plantcv import base as pcv

# Subtract image from another image. 
device, subtracted_img = pcv.image_subtract(img, img2,  device, debug="print")
```

**Subtraction of image 2 from image 1**

![Screenshot](img/documentation_images/image_subtract/subtracted.jpg)
