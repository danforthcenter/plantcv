## Fill

Identifies objects and fills objects that are less than specified size

**plantcv.fill**(*bin_img, size, roi=None*)

**returns** fill_image

- **Parameters:**
    - bin_img - Binary image data
    - size - minimum object area size in pixels (integer), smaller objects will be filled
	- roi - Optional rectangular ROI as returned by [`pcv.roi.rectangle`](roi_rectangle.md) within which to apply this function. (default = None, which uses the entire image)
  - **Context:**
    - Used to reduce image noise
- **Example use:**
    - [Use In Seed Analysis Tutorial](https://plantcv.org/tutorials/seed-analysis-workflow)
    - [Use In PSII Tutorial](https://plantcv.org/tutorials/photosynthesis-multiobject)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

# Apply fill to a binary image that has had a median blur applied.
# Image mask is the same binary image with median blur.

binary_img = pcv.median_blur(gray_img=img, ksize=5)

fill_image = pcv.fill(bin_img=binary_img, size=200)

```

**Binary image with [median blur](median_blur.md)**

![Screenshot](img/documentation_images/fill/binary_image.jpg)

**Filled in binary mask (200 pixels)**

![Screenshot](img/documentation_images/fill/fill_200.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/fill.py)
