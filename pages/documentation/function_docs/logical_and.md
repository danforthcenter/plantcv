---
layout: docs
title: Documentation
subtitle: Logical Operations-And
---

## Logical Operations - And

Join two images using the bitwise AND operator. Images must be the same size. This is a wrapper for the Opencv Function [bitwise_and](http://docs.opencv.org/modules/core/doc/operations_on_arrays.html).  

<font color='blue'><b>logical\_and(img1, img2, device, debug=False)</font></b><br>
<font color='orange'>**returns**</font> device, 'and' image
    
- **Parameters:**   
  - img1 - image object 1.
  - img2 - image object 2.
  - device - Counter for image processing steps
  - debug- Default value is False, if True, intermediate image will be printed 

- **Context:**  
  - Used to combine to images. Very useful when combining image channels that have been thresholded seperately.

- **Example use:**  

 - [Use In Tutorial]()
 
  ```python
    import plantcv as pcv
    
    # Combine two images that have had different thresholds applied to them. For logical 'and' operation object pixel must be in both images to be included in 'and' image.
    
    device, and_image = pcv.logical_and(s_threshold, b_threshold, device, args.debug)

  ```
  <a href="{{site.baseurl}}/img/documentation_images/logical_and/5_fill0.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/logical_and/5_fill0.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/logical_and/9_fill150.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/logical_and/9_fill150.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/logical_and/10_and_joined.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/logical_and/10_and_joined.png" width="200"></a><br>
  Figure 1. (Left) Original image 1. (Middle) Original image 2.(Right) Image combined with logical 'and' operation.  
 

