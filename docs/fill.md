## Fill

Identifies objects and fills objects that are less than specified size

**plantcv.fill**(*bin_img, size*)

**returns** fill_image

- **Parameters:**
    - bin_img - Binary image data
    - size - minimum object area size in pixels (integer), smaller objects will be filled
  - **Context:**
    - Used to reduce image noise
- **Example use:**
    - [Use In VIS Tutorial](tutorials/vis_tutorial.md)
    - [Use In PSII Tutorial](tutorials/psII_tutorial.md) 

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Apply fill to a binary image that has had a median blur applied.
# Image mask is the same binary image with median blur.

binary_img = pcv.median_blur(gray_img=img, ksize=5)

fill_image = pcv.fill(bin_img=binary_img, size=200)

```

**Binary image with [median blur](median_blur.md)**

![Screenshot](img/documentation_images/fill/binary_image.jpg)

**Filled in binary mask (200 pixels)**

![Screenshot](img/documentation_images/fill/fill_200.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/fill.py)
