## Resize

Resizes images, used to resize masks over other images.

**resize**(*img, resize_x, resize_y, device, debug=None*)

**returns** device, image after resizing

- **Parameters:**
    - img1 - Input image
    - resize_x - resize number in the x dimension (does not need to be an integer)
    - resize_y - resize number in the y dimension (does not need to be an integer)
    - device - Counter for image processing steps
    - debug- None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Resizes images.
- **Example use:**
    - [Use In NIR-Vis Tutorial](nir_vis_tutorial.md)
    
**Input image**

![Screenshot](img/documentation_images/dilate/grayscale_image.jpg)

```python
import plantcv as pcv

# Perform dilation
# Results in addition of pixels to the boundary of object
device, dilate_img = pcv.dilate(img, kernel, 1 device, debug='print')
```

**Image after dilation**

![Screenshot](img/documentation_images/dilate/dilate.jpg)
