---
layout: docs
title: Documentation
subtitle: Combine Objects
---

## Combine Objects

Combine objects together for downstream analysis,usually done after object filtering.

<font color='blue'><b>object\_composition(img, contours, hierarchy, device, debug=False)</b></font><br>
<font color='orange'><b>returns</b></font> device, grouped object, image mask<br>

- **Parameters:**   
  - contours- object list
  - device- device number. Used to count steps in the pipeline
  - debug- Default value is False, if True, intermediate image with ROI will be printed 

- **Context:**  
  - This function combines objects together. This is important for downstream analysis of shape characteristics, if plant objects are not combined then one plant can appear to be many different objects.

- **Example use:**  

 - [Use In Tutorial]()
 
  ```python
    import plantcv as pcv
    
    # Combine objects so downstream analysis can be run on a single plant object
    
    device, obj, mask = pcv.object_composition(img, roi_objects, hierarchy, device, debug=True)

  ```
  <a href="{{site.baseurl}}/img/documentation_images/combine_objects/gus1008.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/combine_objects/gus1008.png" width="200">
  <a href="{{site.baseurl}}/img/documentation_images/combine_objects/20_id_objects.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/combine_objects/20_id_objects.png" width="200">
  <a href="{{site.baseurl}}/img/documentation_images/combine_objects/23_objcomp.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/combine_objects/23_objcomp.png" width="200"></a><br>
  Figure 1. (Left) Original image. (Middle) Identified objects. (Right) Combined objects.


 
