## Flood Fill 

Fills based on a starting point with a user specified value

**plantcv.floodfill**(*bin_img, points, value=0, roi=None*)

**returns** filled_image

- **Parameters:**
    - bin_img - Binary image data or Gray image
    - points - list of seed points to start flood fill (e.g. `points=[(x,y)]`)
    - value - value from 0-255
	- roi - Optional rectangular ROI as returned by [`pcv.roi.rectangle`](roi_rectangle.md) within which to apply this function. If an ROI is passed, then points are relative to this ROI. (default = None, which uses the entire image)
  - **Context:**
    - Used to fill in object 
- **Example use:**
    - Below

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

# Apply flood filll  to a binary image 

fill_image = pcv.floodfill(bin_img=binary_img, points =[(31,137)], value=0)

```

**Binary image**

![Screenshot](img/documentation_images/floodfill/Figure1.png)

**Binary image with holes filled**

![Screenshot](img/documentation_images/floodfill/floodfill-Figure2.png)

**Example with an optional regional filter**

```python

from plantcv import plantcv as pcv

# Set global debug behavior
pcv.params.debug = "plot"

# Define a rectangular Region Of Interest
roi = pcv.roi.rectangle(img=binary_image, x=30, y=100, h=100, w=100)

# Apply flood filll  to a binary image 
fill_image = pcv.floodfill(bin_img=binary_img, points=[(1,37)], value=0, roi=roi)

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/floodfill.py)
