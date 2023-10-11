## Import Coordinates to ClickCount Object 

Import coordinates from file to ClickCount Object

**plantcv.annotate.clickcount_file_import**(*img*, *file*)

**returns** ClickCount Object

- **Parameters:**
    - img - img for ClickCount object class initialization
    - file - path to a coordinates file  
- **Context:**
    - Loads coordinates from file to ClickCount object class
- **Example use: *  *
    - Use in pollen germination detection

**Original RGB image**

![Screenshot](img/documentation_images/annotate_clickcount_correct/crop_pollen.png)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "plot"

#step to save out ClickCount coordinates
counter.save_coords(os.path.join(args.outdir,str(args.result) + '.coords'))

#step to import coordinates to ClickCount object
file = os.path.join(args.outdir,str(args.result)+".coords") 
counter=pcv.annotate.clickcount_file_import(img, file)

# view "total" class
counter.view(label="total", color="r", view_all=False)

print(f"There are {counter.count['total']} selected objects")

#view "germinated" class
counter.view(label="germinated", color="b", view_all=False)

print(f"There are {counter.count['germinated']} selected objects")
```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/annotate/clickcount_file_import.py)
