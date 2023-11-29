## Click and count objects 

`ClickCount` is a class that allows users to interactively count objects and other annotation tasks.

*class* **plantcv.annotate.ClickCount**(*img*, *figsize*=(12, 6))

- img - Image data
- figsize - Interactive plot figure size (default = (12,6))

### Attributes
**img**: input image.

**points**: a dictionary of coordinates for every class.

**colors**: a dictionary of colors for every class.

**counts**: a dictionary of count for every class.

**figsize**: figure size.

**events**: a list of events.

**label**: current label.

**color**: current color.

**view_all**: a flag indicating whether or not view all labels.

**fig**: matplotlib figure.

**ax**: matplotlib axis.

**p_not_current**: a list of matplotlib patches that are not current label.

### Methods
**import_coords(*coords*, *label*="total")**

Import coordinates from a list of coordinates.

- Parameters:
    - coords - a list of available coordintes.
    - label - class label for imported coordinates. By default `label="total`.

**view(*label*="total", *color*="c", *view_all*=False)**

View marked image, and update markers if needed.

- Parameters:
    - label - class label to show on the marked image. By default `label="total`.
    - color - desired color to show the class. By default `color="c"`.
    - view_all - a flag indicating whether to show markers for all classes or not. 
  
**save_coords(*filename*)**

Save the collected coordinates to a JSON file.

- Parameters:
    - filename - (json) file name to save the coordinates of collected points. 

**onclick(*event*)**

Handles mouse click events.

**correct**(*bin_img*, *bin_img_recover*, *coords*)

Make corrections to annotations 

**returns** recovered image

- **Parameters:**
    - bin_img - binary image, image with selected objects (e.g. mask output of [`pcv.annotate.detect_discs`](annotate_detect_discs.md))
    - bin_img_recover - binary image, image with all potential objects (binary image to recover objects from)  
    - coords - list of coordinates of 'auto' detected points (e.g. coordinate output of `pcv.annotate.detect_discs`)
- **Context:**
    - Make corrections to the number of objects in a binary image with information from the ClickCount class object instance (both remove and recover objects). Also corrects the ClickCount object instance with coordinates at the center of each object (rather than click location).

**file_import**(*filename*)

Import coordinates from file to a ClickCount object instance

- **Parameters:**
    - filename - path to a coordinates file  
- **Context:**
    - Loads coordinates from a file (probably created with the `.save_coords` method) to ClickCount object instance


**create_labels**(*gray_img*, *label='default'*)

Label ClickCount Objects after they have been segmented 

**returns** labeled object image, labeled class image, ordered list of names, number of objects

- **Parameters:**
    - gray_img - gray image with objects uniquely labeled (e.g. output of [pcv.watershed_segmentation](watershed.md))
    - label - option to put in list of labels, defaults to 'default' if not included
- **Context:**
    - Labels each object with a class id (e.g. germinated, and/or total) that matches classes from ClickCount, returns a list of names for input into analyze steps, and also renumbers objects to equal the total number of objects
- **Output data stored:** Data ('count') for each ClickCount category automatically gets stored to the [`Outputs` class](outputs.md) when this function is
run. These data can be accessed during a workflow (example below). For more detail about data output see
[Summary of Output Observations](output_measurements.md#summary-of-output-observations)

- **Example use:**
    - Below

- **Note**: used in Jupyter notebook.

**Input image**

![ori_img](img/documentation_images/annotate_click_count/count_img.jpg)

**Mask of automated detected objects**

![count_img](img/documentation_images/annotate_click_count/count_mask.png)


```python
# include the line of code below to allow interactive activities
%matplotlib widget

# Import packages
from plantcv import plantcv as pcv
import os

# Define workflow inputs
args = WorkflowInputs(images=["rgb_pollen_image.jpg",
                      names="image1",
                      result="imgID_results.json",
                      outdir=".",
                      writeimg=True,
                      debug="plot")
# Set global debug behavior to "plot" (Jupyter Notebooks or X11)
pcv.params.debug = args.debug

# Read image
img, path, fname = pcv.readimage(filename=args.image1)

# Discard objects that are not circular
discs, coor = pcv.annotate.detect_discs(img_l_post, ecc_thresh=0.5)

# ClickCount Initialization
counter = pcv.annotate.ClickCount(img)

# Click on the plotted image to annotate ***** 
counter.view(label="total", color="r", view_all=False)

# Save out ClickCount coordinates file
counter.save_coords(os.path.join(args.outdir, str(args.result) + '.coords'))

# # Optionally, import coordinates to ClickCount object 
# # (pick up where you left off)
# file = os.path.join(args.outdir, str(args.result) + ".coords") 
# counter.file_import(img=img, filename=file)
# # View "total" class
# counter.view(label="total", color="r", view_all=False)

print(f"There are {counter.count['total']} selected objects")

# Launch interactive tool to select objects with a different class
counter.view(label="germinated", color="b", view_all=False)

print(f"There are {counter.count['germinated']} selected objects")

# Associate a unique label to each grain for segmentation, 
# recover the missing grains, and create a complete mask

completed_mask, counter = counter.correct(bin_img=discs, bin_img_recover=img_l_post, coords=coor)


```


**View markers for `total` class**

![total_mask](img/documentation_images/annotate_click_count/with_totalmask.png)

(When interactivity is enabled, you can left click to add markers for the class, or right click to remove markers)

**View markers for `c1` class**

![c1_mask](img/documentation_images/annotate_click_count/with_clickc1.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/annotate/classes.py)
