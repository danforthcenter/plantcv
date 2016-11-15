## Define Region of Interest (ROI)

Define a region of interest of the image.

<<<<<<< HEAD
**define_roi**(*img, shape, device, roi=None, roi_input='default', debug=None, adjust=False, x_adj=0, y_adj=0, w_adj=0, h_adj=0*)
=======
**define_roi**(*img, shape, device, roi=None, roi_input='default', debug=False, adjust=False, x_adj=0, y_adj=0, w_adj=0, h_adj=0*)
>>>>>>> master

**returns** device, ROI contour, ROI hierarchy

**Important Note:** In order for downstream detection of objects within a region of interest to 
perform properly ROI must be completely contained within the image.

- **Parameters:**
    - img- img to overlay roi
    - roi- default (None) or user input ROI image (not require to generate an ROI), object area should be white and background should be black, has not been optimized for more than one ROI yet
    - roi_input- type of file roi_base is, either 'binary', 'rgb', or 'default' (no ROI inputted)
    - shape- desired shape of final roi, either 'rectangle', 'circle' or 'ellipse', if  user inputs rectangular roi but chooses 'circle' for shape then a circle is fitted around rectangular roi (and vice versa)
    - device- Counter for image processing steps
<<<<<<< HEAD
    - debug- None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None 
=======
    - debug- Default value is False, if True, intermediate image with ROI will be printed 
>>>>>>> master
    - adjust- either 'True' or 'False', if 'True' allows user to adjust ROI on the fly
    - x_adj- adjust center along x axis
    - y_adj- adjust center along y axis
    - w_adj- adjust width
    - h_adj- adjust height
- **Context:**
    - Used to define a region of interest in the image.
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)
    - [Use In PSII Tutorial](psII_tutorial.md) 

```python
import plantcv as pcv

# Define region of interest in an image, there is a futher function 'ROI Objects' that allows 
# the user to define if you want to include objects partially inside ROI or if you want to do cut objects to ROI.
<<<<<<< HEAD
device, roi, roi_hierarchy = define_roi(img, 'rectangle', device, roi=None, roi_input='default', debug="print", adjust=True, x_adj=0, y_adj=0, w_adj=0, h_adj=-925)
=======
device, roi, roi_hierarchy = define_roi(img, 'rectangle', device, roi=None, roi_input='default', debug=True, adjust=True, x_adj=0, y_adj=0, w_adj=0, h_adj=-925)
>>>>>>> master
```

**Image with rectangular ROI**

![Screenshot](img/documentation_images/define_roi/rectangle_roi.jpg)

```python
import plantcv as pcv

# Define region of interest in an image, there is a futher function 'ROI Objects' that allows 
# the user to define if you want to include objects partially inside ROI or if you want to do cut objects to ROI.
<<<<<<< HEAD
device, roi, roi_hierarchy = define_roi(img, 'circle', device, roi=None, roi_input='default', debug="print", adjust=True, x_adj=0, y_adj=0, w_adj=0, h_adj=-925)
=======
device, roi, roi_hierarchy = define_roi(img, 'circle', device, roi=None, roi_input='default', debug=True, adjust=True, x_adj=0, y_adj=0, w_adj=0, h_adj=-925)
>>>>>>> master
```

**Image with circular ROI**

![Screenshot](img/documentation_images/define_roi/circle_roi.jpg)

```python
import plantcv as pcv

# Define region of interest in an image, there is a futher function 'ROI Objects' that allows
# the user to define if you want to include objects partially inside ROI or if you want to do cut objects to ROI.
<<<<<<< HEAD
device, roi, roi_hierarchy = define_roi(img, 'ellipse', device, roi=None, roi_input='default', debug="print", adjust=True, x_adj=0, y_adj=0, w_adj=0, h_adj=-925)
=======
device, roi, roi_hierarchy = define_roi(img, 'ellipse', device, roi=None, roi_input='default', debug=True, adjust=True, x_adj=0, y_adj=0, w_adj=0, h_adj=-925)
>>>>>>> master
```

**Image with elliptical ROI**

![Screenshot](img/documentation_images/define_roi/ellipse_roi.jpg)
