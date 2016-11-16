## Shift Image

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

![Screenshot](img/documentation_images/resize/19_flipped.jpg)

```python
import plantcv as pcv

# Resize image
device, resize_img = pcv.resize(img, 0.1154905775,0.1154905775, device, debug='print')
```

**Image after resizing**

![Screenshot](img/documentation_images/resize/19_resize1.jpg)
