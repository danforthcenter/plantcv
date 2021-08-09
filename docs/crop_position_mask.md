## Crop and Position Mask

Takes a binary mask and positions it on another image. 

**plantcv.crop_position_mask**(*img, mask, x, y, v_pos="top", h_pos="right"*)

**returns** newmask

- **Parameters:**
    - img - RGB or grayscale image data for plotting
    - mask - binary image to be used as a mask
    - x - amount to push in the vertical direction
    - y - amount to push in the horizontal direction
    - v_pos -push from the "top" (default) or "bottom" in the vertical direction
    - h_pos - push from the "right" (default) or "left" in the horizontal direction
   
- **Context:**
    - This function is used to position a binary mask over another image.
      The function will also resize the mask so it is the same size as the target image.
   
- **Example use:**
 - [Use in VIS/NIR Tutorial](tutorials/vis_nir_tutorial.md)

**Original image**

![Screenshot](img/documentation_images/crop_position_mask/original_image.jpg)

**Original resized mask (using the resize function)**

![Screenshot](img/documentation_images/crop_position_mask/23_resize1.jpg)


```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Image not positioned (no adustment)
cropped1 = pcv.crop_position_mask(img=img, mask=mask, x=0, y=0, v_pos="top", h_pos="right")

```

****

![Screenshot](img/documentation_images/crop_position_mask/18_mask_overlay.jpg)


```python

# Image positioned
cropped2 = pcv.crop_position_mask(img=img, mask=mask, x=40, y=3, v_pos="top", h_pos="right")

```

****

![Screenshot](img/documentation_images/crop_position_mask/19_mask_overlay.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/crop_position_mask.py)
