## Import Coordinates to ClickCount Object 

Import coordinates from file to a new object instance of a [ClickCount class](annotate_click_count.md). 

**plantcv.annotate.clickcount_file_import**(*img*, *filename*)

**returns** ClickCount Object instance

- **Parameters:**
    - img - img for ClickCount object class initialization
    - filename - path to a coordinates file  
- **Context:**
    - Loads coordinates from file, probably created with the [`.save_coords`](annotate_click_count.md#methods) method to ClickCount object class
- **Example use:**
    - [Interactive tutorial](tutorials/interactive_ClickCount_tutorial.md)
    - Abbreviated example below

```python

# Import packages
from plantcv import plantcv as pcv
import os

# Define workflow inputs
args = WorkflowInputs(images=["rgb_image.jpg",
                      names="image1",
                      result="results.json",
                      outdir=".",
                      writeimg=True,
                      debug="plot")
# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = args.debug
img, path, fname = pcv.readimage(filename=args.image1)

# Initialization
counter = pcv.annotate.ClickCount(img)

# Click on the plotted image to collect coordinates

# Save out ClickCount coordinates
counter.save_coords(os.path.join(args.outdir,str(args.result) + '.coords'))

# Import coordinates to ClickCount object
file = os.path.join(args.outdir,str(args.result)+".coords") 
counter = pcv.annotate.clickcount_file_import(img=img, filename=file)

# View "total" class
counter.view(label="total", color="r", view_all=False)

print(f"There are {counter.count['total']} selected objects")

# View "germinated" class
counter.view(label="germinated", color="b", view_all=False)

print(f"There are {counter.count['germinated']} selected objects")
```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/annotate/clickcount_file_import.py)
