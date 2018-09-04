## New Rotate

Rotates image without changing the dimensions of the image.

**rotate**(*img, rotation_deg, crop, device,debug=None*)

**returns** device, image after rotation

- **Parameters:**
    - img - RGB or grayscale image data
    - rotation_deg - rotation angle in degrees, should be an integer, can be a negative number, positive values move counter clockwise.
    - crop - if crop is set to True, image will be cropped to original image dimensions, if set to false, the image size will be adjusted to accomodate new image dimensions.
    - device - Counter for image processing steps
    - debug- None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Rotates image, sometimes it is necessary to rotate an image, especially when clustering objects.
- **Example use:**
    - [Use In Multi-Plant Tutorial](multi-plant_tutorial.md)
    
**Input image**

![Screenshot](img/documentation_images/rotate2/34_whitebalance.jpg)

```python
from plantcv import plantcv as pcv

# Rotate image
device, rotate_img = pcv.rotate(img, 10, True, device, debug='print')
```

**Image after rotating 10 degrees**

![Screenshot](img/documentation_images/rotate2/10_rotated_img.jpg)

```python
from plantcv import plantcv as pcv

# Rotate image
device, rotate_img = pcv.rotate(img, -10, device, False, debug='print')
```

**Image after rotating -10 degrees**

![Screenshot](img/documentation_images/rotate2/8_rotated_img.png)