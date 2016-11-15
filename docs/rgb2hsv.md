## RGB to HSV

Convert image from RGB colorspace to HSV colorspace and split the channels.

<<<<<<< HEAD
**rgb2gray_hsv**(*img, channel, device, debug=None*)
=======
**rgb2gray_hsv**(*img, channel, device, debug=False*)
>>>>>>> master

**returns** device, split image (h, s, or v channel)  

- **Parameters:**
    - img- Image to be converted
    - channel- Split 'h' (hue), 's' (saturation), or 'v' (value) channel
    - device- Counter for image processing steps
<<<<<<< HEAD
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
=======
    - debug- Default value is False, if True, RGB to HSV intermediate image will be printed 
>>>>>>> master
- **Context:**
    - Used to help differentiate plant and background
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)
    - [Use In PSII Tutorial](psII_tutorial.md)

**Original RGB image**

![Screenshot](img/documentation_images/rgb2hsv/original_image.jpg)

```python
import plantcv as pcv

# image converted from RGB to HSV, channels are then split. Hue ('h') channel is outputed.

<<<<<<< HEAD
device, h_channel=pcv.rgb2gray_hsv(img, 'h', device, debug="print")
=======
device, h_channel=pcv.rgb2gray_hsv(img, 'h', device, debug=True)
>>>>>>> master
```

**Hue channel image**

![Screenshot](img/documentation_images/rgb2hsv/hsv_hue.jpg)

```python
import plantcv as pcv
    
# image converted from RGB to HSV, channels are then split. Saturation ('s') channel is outputed.
    
<<<<<<< HEAD
device, s_channel= pcv.rgb2gray_hsv(img, 's', device, debug="print")
=======
device, s_channel= pcv.rgb2gray_hsv(img, 's', device, debug=True)
>>>>>>> master
```  

**Saturation channel image**

![Screenshot](img/documentation_images/rgb2hsv/hsv_saturation.jpg)

```python
import plantcv as pcv

# image converted from RGB to HSV, channels are then split. Value ('v') channel is outputed.

<<<<<<< HEAD
device, v_channel=pcv.rgb2gray_hsv(img, 'v', device, debug="print")
=======
device, v_channel=pcv.rgb2gray_hsv(img, 'v', device, debug=True)
>>>>>>> master
```  

**Value channel image**

![Screenshot](img/documentation_images/rgb2hsv/hsv_value.jpg)
