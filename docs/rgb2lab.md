## RGB to LAB

Convert image from RGB colorspace to LAB colorspace and split the channels.

**rgb2gray_hsv**(*img, channel, device, debug=None*)

**returns** device, split image (l, a, or b channel)

- **Parameters:**
    - img- Image to be converted
    - channel - Split 'l' (lightness), 'a' (green-magenta), or 'b' (blue-yellow) channel
    - device - Counter for image processing steps
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Used to help differentiate plant and background
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)

**Original RGB image**

![Screenshot](img/documentation_images/rgb2lab/original_image.jpg)

```python
from plantcv import plantcv as pcv

# image converted from RGB to LAB, channels are then split. Lightness ('l') channel is outputed.

device, l_channel=pcv.rgb2gray_lab(img, 'l', device, debug="print")
```

**Lightness channel image**

![Screenshot](img/documentation_images/rgb2lab/lab_lightness.jpg)

```python
from plantcv import plantcv as pcv

# image converted from RGB to LAB, channels are then split. Green-Magenta ('a') channel is outputed.

device, a_channel= pcv.rgb2gray_lab(img, 'a', device, debug="print")
```

**Green-Magenta channel image**

![Screenshot](img/documentation_images/rgb2lab/lab_green-magenta.jpg)
   
```python
from plantcv import plantcv as pcv

# image converted from RGB to Lab, channels are then split. Blue-Yellow ('b') channel is outputed.

device, b_channel=pcv.rgb2gray_lab(img, 'b', device, debug="print")
```

**Blue-Yellow channel image**

![Screenshot](img/documentation_images/rgb2lab/lab_blue-yellow.jpg)

