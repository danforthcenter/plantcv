## Fill

Identifies objects and fills objects that are less than specified size

**fill**(*img, mask, size, device, debug=None*)

**returns** device, filled image

- **Parameters:**
    - img - binary image object. This image will be returned after filling.
    - mask - binary image object. This image will be used to identify image objects (contours).
    - size - minimum object area size in pixels (integer), smaller objects will be filled
    - device - Counter for image processing steps
    - debug- None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Used to reduce image noise
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)
    - [Use In PSII Tutorial](psII_tutorial.md) 

```python
from plantcv import plantcv as pcv

# Apply fill to a binary image that has had a median blur applied.
# Image mask is the same binary image with median blur.

device, binary_img = pcv.median_blur(img, 5, device, debug="print")
device, mask = pcv.median_blur(img, 5, device, debug="print")

device, fill_image = pcv.fill(binary_img, mask, 200, device, debug="print")
```

**Binary image with median blur**

![Screenshot](img/documentation_images/fill/binary_image.jpg)

**Binary image with median blur and fill (200 pixels)**

![Screenshot](img/documentation_images/fill/fill_200.jpg)
