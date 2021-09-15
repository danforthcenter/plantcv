## RGB to LAB

Convert image from RGB color space to LAB color space and split the channels.

**plantcv.rgb2gray_lab**(*rgb_img, channel*)

**returns** split image (l, a, or b channel)

- **Parameters:**
    - rgb_img - RGB image data
    - channel - Split 'l' (lightness), 'a' (green-magenta), or 'b' (blue-yellow) channel
   
- **Context:**
    - Used to help differentiate plant and background
- **Example use:**
    - [Use In VIS Tutorial](tutorials/vis_tutorial.md)

**Original RGB image**

![Screenshot](img/documentation_images/rgb2lab/original_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# image converted from RGB to LAB, channels are then split. 
# Lightness ('l') channel is output
l_channel = pcv.rgb2gray_lab(rgb_img=rgb_img, channel='l')

```

**Lightness channel image**

![Screenshot](img/documentation_images/rgb2lab/lab_lightness.jpg)

```python

# Green-Magenta ('a') channel is output
a_channel = pcv.rgb2gray_lab(rgb_img=rgb_img, channel='a')

```

**Green-Magenta channel image**

![Screenshot](img/documentation_images/rgb2lab/lab_green-magenta.jpg)
   
```python

# Blue-Yellow ('b') channel is output
b_channel = pcv.rgb2gray_lab(rgb_img=rgb_img, channel='b')

```

**Blue-Yellow channel image**

![Screenshot](img/documentation_images/rgb2lab/lab_blue-yellow.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/rgb2gray_lab.py)
