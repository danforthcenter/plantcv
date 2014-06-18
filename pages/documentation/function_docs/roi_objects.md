---
layout: docs
title: Documentation
subtitle: Region of Interest- Objects
---

## Find Objects within a Region of Interest

Find objects within a region of interest, either cut those objects to the region of interest or include objects that overlap with the region of interest.

<font color='blue'><b>roi\_objects(img,roi\_type,roi\_contour, roi\_hierarchy,object\_contour, obj\_hierarchy, device, debug=False)</b></font><br>
<font color='orange'><b>returns</b></font> device, kept objects, object hierarchy, object mask, object area <br>

<font color='red'><b> Important Note:</b></font> If your ROI object detection does not perform first check that the ROI is completely within the image<br>

- **Parameters:**
  - img = img to display kept objects
  - roi\_type = 'cutto' or 'partial' (include objects that are partially inside or overlapping with ROI)
  - roi\_contour = contour of roi, output from "define_roi" function
  - roi\_hierarchy = contour of roi, output from "define_roi" function 
  - object\_contour = contours of objects, output from "find_objects" fuction 
  - obj\_hierarchy = hierarchy of objects, output from "find_objects" fuction
  - device = device number.  Used to count steps in the pipeline
  - device- Counter for image processing steps
  - debug- Default value is False, if True, intermediate image with ROI objects identified will be printed 

- **Context:**  
  - Used to find objects within a region of interest and decide which ones to keep.

- **Example use:**  

 - [Use In Tutorial]()
 
  ```python
    import plantcv as pcv
    
    # ROI objects allows the user to define if objects partially inside ROI are included or if objects are cut to ROI.
    
    device,roi_objects, hierarchy, kept_mask, obj_area = pcv.roi_objects(img,'partial', roi, roi_hierarchy, objects, obj_hierarchy, device, debug=True)

  ```
  <a href="{{site.baseurl}}/img/documentation_images/roi_objects/22_obj_on_img.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/roi_objects/22_obj_on_img.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/roi_objects/22_roi_mask.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/roi_objects/22_roi_mask.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/roi_objects/22_roi_objects.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/roi_objects/22_roi_objects.png" width="200"></a><br>
  Figure 1. (Left) Object (green) that is identified as partially inside ROI. (Middle) Mask of identified object. (Right) Kept objects. 
 
  ```python
    import plantcv as pcv
    
    # Define region of interest in an image, there is a futher function 'ROI Objects' that allows the user to define if you want to include objects partially inside ROI or if you want to do cut objects to ROI.
    
    device,roi_objects, hierarchy, kept_mask, obj_area = pcv.roi_objects(img,'cutto', roi, roi_hierarchy, objects, obj_hierarchy, device, debug=True)

  ```
  <a href="{{site.baseurl}}/img/documentation_images/roi_objects/22_obj_on_img1.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/roi_objects/22_obj_on_img1.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/roi_objects/22_roi_mask1.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/roi_objects/22_roi_mask1.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/roi_objects/22_roi_objects1.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/roi_objects/22_roi_objects1.png" width="200"></a><br>
  Figure 2. (Left) Object (green) that is cut to the ROI. (Middle) Mask of identified object. (Right) Kept objects. 
 
 
