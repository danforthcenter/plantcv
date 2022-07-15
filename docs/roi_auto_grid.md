## Create a Grid of Circular Regions of Interest (ROI) Automatically

**plantcv.roi.auto_grid**(*bin_mask, nrows, ncols, radius=None, img=None*)

**returns** roi_objects

- **Parameters:**
    - bin_mask       = A binary mask.
    - nrows          = Number of rows in ROI layout.
    - ncols          = Number of columns in ROI layout.
    - radius         = Optional parameter to specify the radius of the ROIs.
    - img            = Optional Image from which the binary mask was created.
- **Context:**
    - Used to define a grid of multiple circular regions of interest in the same binary mask. Users
      specify a number of rows and columns, and the function detects a grid of circular ROIs based
      on the inputs. A custom radius can optionally be set for the individual circles. If the image from
      which the binary mask was created is passed as an argumnet, ROIs will be drawn on that image if
      debug is set to plot. Otherwise, they will be drawn on the binary mask. Returns an Objects
      dataclass that can be used in downstream steps. It is not necessary for there to be a plant
      in every grid cell, just that the objects follow a general grid structure and that there is at
      least one object in each row and column. Similar to the [pcv.roi.multi](roi_multi.md) function.

**Reference Image**

![Screenshot](img/documentation_images/multi/original_multi_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Make a grid of ROIs 
rois = pcv.roi.auto_grid(bin_mask=mask, nrows=3, ncols=6, radius=20, img=img)

```

**Grid of ROIs**

![Screenshot](img/documentation_images/multi/grid_roi.jpg)

### Next steps:

This function returns an Objects dataclass, which contains contours and hierarchy attributes. Since
  these attributes are lists, the downstream steps require users to loop over each. The 
  [pcv.roi_objects](roi_objects.md) and [pcv.object_composition](object_composition.md) functions 
  usually follow an ROI step.

```python
import numpy as np 

img_copy = np.copy(img)

# The result file should exist if plantcv-workflow.py was run
if os.path.exists(args.result):
    # Open the result file
    results = open(args.result, "r")
    # The result file would have image metadata in it from plantcv-workflow.py, read it into memory
    metadata = results.read()
    # Close the file
    results.close()
    # Delete the file, we will create new ones
    os.remove(args.result)

for roi, hierarchy in rois:
    # Find objects
    filtered_contours, filtered_hierarchy, filtered_mask, filtered_area = pcv.roi_objects(
        img=img, roi_type="partial", roi_contour=roi, roi_hierarchy=hierarchy, object_contour=obj, 
        obj_hierarchy=obj_hierarchy)
    
    # Combine objects together in each plant     
    plant_contour, plant_mask = pcv.object_composition(img=img, contours=filtered_contours, hierarchy=filtered_hierarchy)        
    
    # Analyze the shape of each plant 
    analysis_images = pcv.analyze_object(img=img_copy, obj=plant_contour, mask=plant_mask)
    
    # Save the image with shape characteristics 
    img_copy = analysis_images
    
    # Print out a text file with shape data for each plant in the image 
    filename = args.result[:-4] + "_" + str(i) + ".txt" 
    with open(filename, "w") as r:
        r.write(metadata)
    pcv.outputs.save_results(filename=filename)
    # Clear the measurements stored globally into the Outputs class
    pcv.outputs.clear()
    
# Plot out the image with shape analysis on each plant in the image 
pcv.plot_image(img_copy)
```
**Custom list of ROIs** 

![Screenshot](img/documentation_images/multi/first_plant_mask.jpg)

**Custom list of ROIs** 

![Screenshot](img/documentation_images/multi/first_plant_object.jpg)

**Custom list of ROIs** 

![Screenshot](img/documentation_images/multi/first_plant_shape.jpg)

Many intermediate outputs later... 

**Image with shape analysis characteristics on each plant** 

![Screenshot](img/documentation_images/multi/multi_plants_shape.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/roi/roi_methods.py)
