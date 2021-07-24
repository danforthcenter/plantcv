## RGB to HSV

Convert image from RGB color space to HSV color space and split the channels.

**plantcv.rgb2gray_hsv**(*rgb_img, channel*)

**returns** split image (h, s, or v channel)  

- **Parameters:**
    - rgb_img - RGB image data
    - channel - Split 'h' (hue), 's' (saturation), or 'v' (value) channel
   
- **Context:**
    - Used to help differentiate plant and background
- **Example use:**
    - [Use In VIS Tutorial](tutorials/vis_tutorial.md)
    - [Use In PSII Tutorial](tutorials/psII_tutorial.md)

**Original RGB image**

![Screenshot](img/documentation_images/rgb2hsv/original_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# image converted from RGB to HSV, channels are then split. 
# Hue ('h') channel is output
h_channel = pcv.rgb2gray_hsv(rgb_img=rgb_img, channel='h')

```

**Hue channel image**

![Screenshot](img/documentation_images/rgb2hsv/hsv_hue.jpg)

```python

# Saturation ('s') channel is output    
s_channel = pcv.rgb2gray_hsv(rgb_img=rgb_img, channel='s')

```  

**Saturation channel image**

![Screenshot](img/documentation_images/rgb2hsv/hsv_saturation.jpg)

```python

# Value ('v') channel is output
v_channel = pcv.rgb2gray_hsv(rgb_img=rgb_img, channel='v')

```  

**Value channel image**

![Screenshot](img/documentation_images/rgb2hsv/hsv_value.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/rgb2gray_hsv.py)
