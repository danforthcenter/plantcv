---
layout: docs
title: Documentation
subtitle: Analyze Shapes
---

## Analyze Shape Characteristics of Object

Shape analysis outputs numeric properties for an input object (contour or grouped contours), works best on grouped contours.
 
<font color='blue'><b>analyze\_object(img, imgname, obj, mask, device, debug=False, filename=False)</b></font><br>
<font color='orange'><b>returns</b></font> device, shape data headers, shape data, image with shape data<br>

- **Parameters:**   
  - img - image object (most likely the original), color(RGB)
  - imgname - name of image
  - obj - single or grouped contour object
  - device - Counter for image processing steps
  - debug - Default value is False, if True, intermediate image with ROI will be printed 
  - filename - False or image name. If defined print image

- **Context:**  
  - Used to output shape characteristics of an image, including height, object area, convex hull, convex hull area, perimeter, extent x, extent y, longest axis, centroid x coordinate, centroid y coordinate, in bounds QC (if object touches edge of image, image is flagged). 

- **Example use:**  

 - [Use In Tutorial](http://plantcv.danforthcenter.org/pages/documentation/function_docs/vis_tutorial.html)
 
  ```python
    import plantcv as pcv
    
    # Characterize object shapes
        
    device, shape_header,shape_data,shape_img = pcv.analyze_object(img, imgname, objects, mask, device, debug=True, /home/malia/setaria_shape_img.png)

  ```
  <a href="{{site.baseurl}}/img/documentation_images/analyze_shapes/VIS_SV_180_z2500_349810.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/analyze_shapes/VIS_SV_180_z2500_349810.png" width="200">
  <a href="{{site.baseurl}}/img/documentation_images/analyze_shapes/22_obj_on_img.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/analyze_shapes/22_obj_on_img.png" width="200">
  <a href="{{site.baseurl}}/img/documentation_images/analyze_shapes/24_shapes.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/analyze_shapes/24_shapes.png" width="200"></a><br>
  Figure 1. (Left) Original image. (Middle) Identified objects. (Right) Image with shape characteristics
 

