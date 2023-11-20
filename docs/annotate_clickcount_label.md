## Label ClickCount Objects

Label ClickCount Objects after they have been segmented 

**plantcv.annotate.clickcount_label**(*gray_img*, *counter*, *imgname='default'*)

**returns** labeled object image, labeled class image, ordered list of names, number of objects

- **Parameters:**
    - gray_img - gray image with objects uniquely labeled (output of watershed for example)
    - counter - ClickCount class object with points interactively corrected by the user
    - imgname - option to put in imgname, defaults to 'default' if not included
- **Context:**
    - Labels each object with a class id (e.g. germinated, and/or total) that matches classes from ClickCount, returns a list of names for input into analyze steps, and also renumbers objects to equal the total number of objects
- **Example use:**
    - Use in pollen germination detection example below
- **Output data stored:** Data ('count') for each ClickCount category automatically gets stored to the [`Outputs` class](outputs.md) when this function is
run. These data can be accessed during a workflow (example below). For more detail about data output see
[Summary of Output Observations](output_measurements.md#summary-of-output-observations)

**Original RGB image**

![Screenshot](img/documentation_images/annotate_clickcount_label/crop_pollen.png)
  
**Output of Watershed Segementation**

![Screenshot](img/documentation_images/annotate_clickcount_label/Figure6.png)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "plot"

# Apply binary 'white' mask over an image. 
obj_label, class_label, class_list, num = pcv.annotate.clickcount_label(gray_img=pollen_watershed, counter=counter, imgname="pollen_heat")

count = pcv.outputs.observations['pollen_heat']['total']

```

**Recovered Objects Image**

![Screenshot](img/documentation_images/annotate_clickcount_label/Figure7.png)
![Screenshot](img/documentation_images/annotate_clickcount_label/Figure8.png)


**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/annotate/clickcount_label.py)
