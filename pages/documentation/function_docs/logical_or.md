---
layout: docs
title: Documentation
subtitle: Logical Operations-Or
---

## Logical Operations - Or

Join two images using the bitwise OR operator. Images must be the same size. This is a wrapper for the Opencv Function [bitwise_or](http://docs.opencv.org/modules/core/doc/operations_on_arrays.html).  

<font color='blue'><b>logical\_or(img1, img2, device, debug=False)</font></b><br>
<font color='orange'>**returns**</font> device, 'and' image
    
- **Parameters:**   
  - img1 - image object 1.
  - img2 - image object 2.
  - device - Counter for image processing steps
  - debug- Default value is False, if True, intermediate image will be printed 

- **Context:**  
  - Used to combine to images. Very useful when combining image channels that have been thresholded seperately.

- **Example use:**  

 - [Use In Tutorial](http://plantcv.danforthcenter.org/pages/documentation/function_docs/vis_tutorial.html)
 
  ```python
    import plantcv as pcv
    
    # Combine two images that have had different thresholds applied to them. For logical 'or' operation object pixel in either image object will be included in 'or' image.
    
    # Threshold the green-magenta channel
      device, maskeda_thresh = pcv.binary_threshold(masked_a, 122, 255, 'dark', device, args.debug)
    
    # Threshold the blue-yellow channel
      device, maskedb_thresh = pcv.binary_threshold(masked_b, 133, 255, 'light', device, args.debug)
      
    # Join the thresholded green-magenta and blue-yellow images (OR)
      device, ab = pcv.logical_or(maskeda_thresh, maskedb_thresh, device, args.debug)

  ```
  <a href="{{site.baseurl}}/img/documentation_images/logical_or/14_binary_threshold122_inv.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/logical_or/14_binary_threshold122_inv.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/logical_or/15_binary_threshold133.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/logical_or/15_binary_threshold133.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/logical_or/16_or_joined.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/logical_or/16_or_joined.png" width="200"></a><br>
  Figure 1. (Left) Original image 1. (Middle) Original image 2.(Right) Image combined with logical 'or' operation.  
 

