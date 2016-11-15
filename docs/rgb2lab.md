## RGB to LAB

Convert image from RGB colorspace to LAB colorspace and split the channels.

<<<<<<< HEAD
**rgb2gray_hsv**(*img, channel, device, debug=None*)
=======
**rgb2gray_hsv**(*img, channel, device, debug=False*)
>>>>>>> master

**returns** device, split image (l, a, or b channel)

- **Parameters:**
    - img- Image to be converted
<<<<<<< HEAD
    - channel - Split 'l' (lightness), 'a' (green-magenta), or 'b' (blue-yellow) channel
    - device - Counter for image processing steps
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
=======
    - channel- Split 'l' (lightness), 'a' (green-magenta), or 'b' (blue-yellow) channel
    - device- Counter for image processing steps
    - debug- Default value is False, if True, RGB to LAB intermediate image will be printed 
>>>>>>> master
- **Context:**
    - Used to help differentiate plant and background
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)

**Original RGB image**

![Screenshot](img/documentation_images/rgb2lab/original_image.jpg)

```python
import plantcv as pcv

# image converted from RGB to LAB, channels are then split. Lightness ('l') channel is outputed.

<<<<<<< HEAD
device, l_channel=pcv.rgb2gray_lab(img, 'l', device, debug="print")
=======
device, l_channel=pcv.rgb2gray_lab(img, 'l', device, debug=True)
>>>>>>> master
```

**Lightness channel image**

![Screenshot](img/documentation_images/rgb2lab/lab_lightness.jpg)

```python
import plantcv as pcv

# image converted from RGB to LAB, channels are then split. Green-Magenta ('a') channel is outputed.

<<<<<<< HEAD
device, a_channel= pcv.rgb2gray_lab(img, 'a', device, debug="print")
=======
device, a_channel= pcv.rgb2gray_lab(img, 'a', device, debug=True)
>>>>>>> master
```

**Green-Magenta channel image**

![Screenshot](img/documentation_images/rgb2lab/lab_green-magenta.jpg)
   
```python
import plantcv as pcv

# image converted from RGB to Lab, channels are then split. Blue-Yellow ('b') channel is outputed.

<<<<<<< HEAD
device, b_channel=pcv.rgb2gray_lab(img, 'b', device, debug="print")
=======
device, b_channel=pcv.rgb2gray_lab(img, 'b', device, debug=True)
>>>>>>> master
```

**Blue-Yellow channel image**

![Screenshot](img/documentation_images/rgb2lab/lab_blue-yellow.jpg)

