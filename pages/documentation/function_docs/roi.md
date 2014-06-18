---
layout: docs
title: Documentation
subtitle: Region of Interest- Define
---

## Define Region of Interest (ROI)

Define a region of interest of the image.

<font color='blue'><b>define\_roi(img, shape, device, roi=None, roi\_input='default', debug=False, adjust=False, x\_adj=0, y\_adj=0, w\_adj=0, h\_adj=0)</b></font><br>
<font color='orange'><b>returns</b></font> device, ROI contour, ROI hierarchy<br>

<font color='red'><b> Important Note:</b></font> In order for downstream detection of objects within a region of interest to perform properly ROI must be completely contained within the image<br>

- **Parameters:**   
  - img- img to overlay roi 
  - roi- default (None) or user input ROI image (not require to generate an ROI), object area should be white and background should be black, has not been optimized for more than one ROI yet
  - roi_input- type of file roi_base is, either 'binary', 'rgb', or 'default' (no ROI inputted)
  - shape- desired shape of final roi, either 'rectangle', 'circle' or 'ellipse', if  user inputs rectangular roi but chooses 'circle' for shape then a circle is fitted around rectangular roi (and vice versa)
  - device- Counter for image processing steps
  - debug- Default value is False, if True, intermediate image with ROI will be printed 
  - adjust- either 'True' or 'False', if 'True' allows user to adjust ROI on the fly
  - x_adj- adjust center along x axis
  - y_adj- adjust center along y axis
  - w_adj- adjust width
  - h_adj- adjust height

- **Context:**  
  - Used to define a region of interest in the image.

- **Example use:**  

 - [Use In Tutorial]()
 
  ```python
    import plantcv as pcv
    
    # Define region of interest in an image, there is a futher function 'ROI Objects' that allows the user to define if you want to include objects partially inside ROI or if you want to do cut objects to ROI.
    
    define_roi(img, rectangle, device, roi=None, roi_input='default', debug=True, adjust=True, x_adj=0, y_adj=0, w_adj=0, h_adj=-925 )

  ```
  <a href="{{site.baseurl}}/img/documentation_images/roi/21_roi.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/roi/21_roi.png" width="200"></a><br>
  Figure 1. Image with ROI made 'on the fly'. 
 
  ```python
    import plantcv as pcv
    
    # Define region of interest in an image, there is a futher function 'ROI Objects' that allows the user to define if you want to include objects partially inside ROI or if you want to do cut objects to ROI.
    
    define_roi(img, circle, device, roi=None, roi_input='default', debug=True, adjust=True, x_adj=0, y_adj=0, w_adj=0, h_adj=-925 )

  ```
  <a href="{{site.baseurl}}/img/documentation_images/roi/21_roi1.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/roi/21_roi1.png" width="200"></a><br>
  Figure 2. Image with ROI made 'on the fly'. 

 
