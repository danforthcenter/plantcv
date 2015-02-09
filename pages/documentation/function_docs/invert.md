---
layout: docs
title: Documentation
subtitle: Invert    
---

## Invert

Invert a binary image. This is a wrapper for the OpenCV function [bitwise_not](http://docs.opencv.org/modules/core/doc/operations_on_arrays.html)

<font color='blue'><b>invert(img, device, debug=False)</font></b><br>
<font color='orange'>**returns**</font> device, inverted image

- **Parameters:**   
  - img = image to be inverted (works best with binary image)
  - device- Counter for image processing steps
  - debug- Default value is False, if True, masked intermediate image will be printed 

- **Context:**  
  - Invert image values. Useful for inverting an image mask.

- **Example use:**  

 - [Use In Tutorial](http://plantcv.danforthcenter.org/pages/documentation/function_docs/flu_tutorial.html)
 
  ```python
    import plantcv as pcv
    
    # Invert a binary mask. 
    
      device, inverted_img = pcv.invert(img, device, debug=True)
  ```
  
  <a href="{{site.baseurl}}/img/documentation_images/invert/12_roi_mask.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/invert/12_roi_mask.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/invert/12_roi_objects.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/invert/12_roi_objects.png" width="200"></a>  

  Figure 1. (Left) Original image. (Right) Inverted image. 
 
