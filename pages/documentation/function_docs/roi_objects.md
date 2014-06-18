---
layout: docs
title: Documentation
subtitle: Region of Interest- Objects
---

## Find Objects within a Region of Interest

Find objects within a region of interest, either cut those objects to the region of interest or include objects that overlap with the region of interest.

<font color='blue'><b>roi\_objects(img,roi\_type,roi\_contour, roi\_hierarchy,object\_contour, obj\_hierarchy, device, debug=False)</b></font><br>
<font color='orange'><b>returns</b></font> device, ROI contour, ROI hierarchy<br>

<font color='red'><b> Important Note:</b></font> If your ROI object detection does not perform first check that the ROI is completely within the image<br>

- **Parameters:**
  - img = img to display kept objects
  - roi_type = 'cutto' or 'partial' (for partially inside)
  - roi_contour = contour of roi, output from "View and Ajust ROI" function
  - roi_hierarchy = contour of roi, output from "View and Ajust ROI" function
  - object_contour = contours of objects, output from "Identifying Objects" fuction
  - obj_hierarchy = hierarchy of objects, output from "Identifying Objects" fuction
  - device = device number.  Used to count steps in the pipeline
  - device- Counter for image processing steps
  - debug- Default value is False, if True, intermediate image with ROI will be printed 

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

  ```python
    import plantcv as pcv
    
    # Define region of interest in an image, there is a futher function 'ROI Objects' that allows the user to define if you want to include objects partially inside ROI or if you want to do cut objects to ROI.
    
    define_roi(img, ellipse, device, roi=None, roi_input='default', debug=True, adjust=True, x_adj=0, y_adj=0, w_adj=0, h_adj=-925 )

  ```
  <a href="{{site.baseurl}}/img/documentation_images/roi/21_roi2.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/roi/21_roi2.png" width="200"></a><br>
  Figure 3. Image with ROI made 'on the fly'. 
