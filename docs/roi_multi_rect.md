## Create Multiple Rectangular Regions of Interest (ROI) 

**plantcv.roi.multi_rect**(*img, coord, h=None, w=None, spacing=None, nrows=None, ncols=None*)

**returns** roi_objects

- **Parameters:**
    - img            = Input image data.
    - coord          = Two-element tuple of the center of the top left object.
    - h              = Int height of each rectangular ROI
	- w              = Int width of each rectangular ROI
    - spacing        = Two-element tuple of the horizontal and vertical spacing between ROIs.
    - nrows          = Number of rows in ROI layout.
    - ncols          = Number of columns in ROI layout.
- **Context:**
    - Used to define multiple regions of interest in the same image. Users can either specify a
      starting coordinate (`coord`), number of row and columns, and spacing to create a grid of ROIs,
      or a custom list of coordinates that specify the centers of the ROIs. Providing a custom list 
      of coordinates (list of tuples) is useful for missing plants or any arrangement that isn't 
      a perfect grid. Returns an Objects instance that can be used in downstream steps. The analysis
      image includes a number representing ROI order. 

**Reference Image**

![Screenshot](img/documentation_images/multi/original_multi_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

# Make a grid of ROIs
rois1 = pcv.roi.multi_rect(img, coord = (40, 90), h=50, w=50,
                           spacing=(70, 70), nrows=3, ncols=5)

# Specify a list of coordinates of desired ROIs 
rois2 = pcv.roi.multi_rect(img, coord=[(40, 90), (105, 90), (170, 90)], h=50, w=50)

```

**Grid of ROIs**

![Screenshot](img/documentation_images/multi/grid_rect_roi.png)

**Custom list of ROIs** 

![Screenshot](img/documentation_images/multi/custom_list_rect_roi.png)

### Next steps:

This function returns an Objects dataclass, which can be used with [create_labels](create_labels.md) to create a labeled
mask for use with analysis functions.

```python
lbl_mask, n_lbls = pcv.create_labels(mask=mask, rois=rois)

# Analyze the shape of each plant 
shape_img = pcv.analyze.size(img=img1, labeled_mask=lbl_mask, n_labels=n_lbls, label="plant")

# Print out a text file with shape data for each plant in the image 
pcv.outputs.save_results(filename=filename)

```

**Image with shape analysis characteristics on each plant** 

![Screenshot](img/documentation_images/multi/multi_plants_shape.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/roi/roi_methods.py)
