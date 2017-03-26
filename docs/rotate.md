## Rotate

Rotates image without changing the dimensions of the image.

**rotate_img**(*img, rotation_deg, device,debug=None*)

**returns** device, image after rotation

- **Parameters:**
    - img - Input image
    - rotation_deg - rotation angle in degrees, should be an integer, can be a negative number, positive values move counter clockwise.
    - device - Counter for image processing steps
    - debug- None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Rotates image, sometimes it is necessary to rotate an image, especially when clustering objects.
- **Example use:**
    - [Use In Multi-Plant Tutorial](multi-plant_tutorial.md)
    
**Input image**

![Screenshot](img/documentation_images/rotate/34_whitebalance.jpg)

```python
import plantcv as pcv

# Rotate image
device, rotate_img = pcv.rotate_img(img, 10, device, debug='print')
```

**Image after rotating 10 degrees**

![Screenshot](img/documentation_images/rotate/10_rotated_img.jpg)

```python
import plantcv as pcv

# Rotate image
device, rotate_img = pcv.rotate_img(img, -10, device, debug='print')
```

**Image after rotating -10 degrees**

![Screenshot](img/documentation_images/rotate/32_rotated_img.jpg)