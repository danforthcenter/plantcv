---
layout: docs
title: Documentation
subtitle: Find Objects
---

## Find Objects

Find objects within the image.

<font color='blue'>**find\_objects(img, mask, device, debug=False)**</font><br>
<font color='orange'>**returns**</font> device, objects, object hierarchy

    
- **Parameters:**   
  - img - image that the objects will be overlayed
  - mask - what is used for object detection
  - device - Counter for image processing steps
  - debug- Default value is False, if True, intermediate image with identified objects will be printed 

- **Context:**  
  - Used to identify objects (plant material) in an image.

- **Example use:**  

 - [Use In Tutorial](http://plantcv.danforthcenter.org/pages/documentation/function_docs/vis_tutorial.html)
 
  ```python
    import plantcv as pcv
    
    # Identify objects (plant material) in an image, all objects regardless of hierarchy are filled (e.g. holes between leaves).
    
    device, id_objects,obj_hierarchy = pcv.find_objects(img, mask, device, debug=True)

  ```
  <a href="{{site.baseurl}}/img/documentation_images/find_objects/VIS_SV_180_z2500_349810.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/find_objects/VIS_SV_180_z2500_349810.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/find_objects/18_fill200.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/find_objects/18_fill200.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/find_objects/20_id_objects.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/find_objects/20_id_objects.png" width="200"></a><br>
  Figure 1. (Left) Original image. (Middle) Binary image mask. (Right) Image with objects identified.  
 

