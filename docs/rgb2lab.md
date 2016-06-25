## RGB to LAB

Convert image from RGB colorspace to LAB colorspace and split the channels.

**rgb2gray_hsv(img, channel, device, debug=False)**

**returns** device, split image (l, a, or b channel)

- **Parameters:**
    - img- Image to be converted
    - channel- Split 'l' (lightness), 'a' (green-magenta), or 'b' (blue-yellow) channel
    - device- Counter for image processing steps
    - debug- Default value is False, if True, RGB to LAB intermediate image will be printed 
- **Context:**
    - Used to help differentiate plant and background
- **Example use:**
    - [Use In Tutorial](../vis_tutorial.md)

**Original RGB image**

![Screenshot](img/documentation_images/rgb2lab/original_image.jpg)

```python
import plantcv as pcv

# image converted from RGB to LAB, channels are then split. Lightness ('l') channel is outputed.

device, l_channel=pcv.rgb2gray_lab(img, 'l', device, debug=True)
```

**Lightness channel image**

![Screenshot](img/documentation_images/rgb2lab/lab_lightness.jpg)

```python
import plantcv as pcv

# image converted from RGB to LAB, channels are then split. Green-Magenta ('a') channel is outputed.

device, a_channel= pcv.rgb2gray_lab(img, 'a', device, debug=True)
```

**Green-Magenta channel image**

![Screenshot](img/documentation_images/rgb2lab/lab_green-magenta.jpg)
   
```python
import plantcv as pcv

# image converted from RGB to Lab, channels are then split. Blue-Yellow ('b') channel is outputed.

device, b_channel=pcv.rgb2gray_lab(img, 'b', device, debug=True)
```

**Blue-Yellow channel image**

![Screenshot](img/documentation_images/rgb2lab/lab_blue-yellow.jpg)

