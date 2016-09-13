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
 - [Use in VIS/NIR Tutorial]()

**Original image**

![Screenshot](img/documentation_images/analyze_color/original_image.jpg)

```python
import plantcv as pcv

# Flip Image

device, flipped= pcv.flip(img, 'horizontal', device, debug="print")

```

**Flipped Image**

![Screenshot](img/documentation_images/analyze_color/color_histogram.jpg)
