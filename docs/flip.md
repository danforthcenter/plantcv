## Flip Image

Flips and image in either the horizontal or vertical direction

**flip**(*img, direction, device, debug=None*)

**returns** device, flipped_image

- **Parameters:**
    - img - image object (numpy array)
    - direction - the direction you want the image flipped either 'horizontal' or 'vertical'
    - device - Counter for image processing steps
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Used to flip images when necessary
- **Example use:**
 - flip image horizontally or vertically, rotate function is also available to adjust image positioning.

**Original image**

![Screenshot](img/documentation_images/flip/original_image.jpg)

```python
from plantcv import plantcv as pcv

# Flip Image Horizontal

device, flipped= pcv.flip(img, 'horizontal', device, debug="print")

```

**Flipped Image**

![Screenshot](img/documentation_images/flip/flipped.jpg)

```python
from plantcv import plantcv as pcv

# Flip Image Vertical

device, flipped= pcv.flip(img, 'vertical', device, debug="print")

```

**Flipped Image**

![Screenshot](img/documentation_images/flip/flipped1.jpg)