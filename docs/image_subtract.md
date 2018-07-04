## Image Subtract

This is a function is used to subtract values of one gray-scale image array from another gray-scale image array. The
    resulting gray-scale image array has a minimum element value of zero. That is all negative values resulting from the
    subtraction are forced to zero.

**plantcv.image_subtract**(*gray_img1, gray_img2*)

**returns** new_img

- **Parameters:**
    - gray_img1 - a gray-scale or binary image from which gray_img2 will be subtracted
    - gray_img2 - a gray-scale or binary image to be subtracted from gray_img1
- **Context:**
    - returns difference in pixel values of two images 
- **Example use:**
    - [Use In NIR Tutorial](nir_tutorial.md)

**Gray_Img1**

![Screenshot](img/documentation_images/image_subtract/plant_img.jpg)

**Gray_Img2**

![Screenshot](img/documentation_images/image_subtract/background_img.jpg)

```python
from plantcv import plantcv as pcv

# Subtract image from another image. 
device, subtracted_img = pcv.image_subtract(gray_img1, gray_img2)
```

**Result**

![Screenshot](img/documentation_images/image_subtract/result.jpg)
