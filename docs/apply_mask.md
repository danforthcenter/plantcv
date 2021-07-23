## Apply Mask

Apply binary mask to an image.

**plantcv.apply_mask**(*img, mask, mask_color*)

**returns** masked image

- **Parameters:**
    - img - RGB image data or [Spectral_data](Spectral_data.md) class object. 
    - mask - Binary mask image data
    - mask_color - 'white' or 'black'
- **Context:**
    - Apply a binary image mask over a grayscale or RGB image. Useful for separating plant and background materials.
- **Example use:**
    - [Use In VIS Tutorial](tutorials/vis_tutorial.md)
    - [Use In NIR Tutorial](tutorials/nir_tutorial.md)
    - [Use In PSII Tutorial](tutorials/psII_tutorial.md)
    - [Use In Hyperspectral Tutorial](tutorials/hyperspectral_tutorial.md)

**Original RGB image**

![Screenshot](img/documentation_images/apply_mask/original_image.jpg)

**Mask image**

![Screenshot](img/documentation_images/apply_mask/mask.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "print"

# Apply binary 'white' mask over an image. 
masked_image = pcv.apply_mask(img=img, mask=mask, mask_color='white')

```

**White-masked image**

![Screenshot](img/documentation_images/apply_mask/white_masked_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "print"

# Apply binary 'black' mask over an image.
masked_image = pcv.apply_mask(img=img, mask=mask, mask_color='black')

```
  
**Black-masked image**

![Screenshot](img/documentation_images/apply_mask/black_masked_image.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/apply_mask.py)
