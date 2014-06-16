---
layout: docs
title: Documentation
subtitle: Apply Mask    
---

## Apply Mask

Join two images using the bitwise AND operator. Images must be the same size. This is a wrapper for the Opencv Function [bitwise_and](http://docs.opencv.org/modules/core/doc/operations_on_arrays.html).  

<font color='blue'><b><plaintext>apply_mask(img, mask, mask_color, device, debug=False)</plaintext></font></b><br>
<font color='orange'>**returns**</font> device, masked image
    
- **Parameters:**   
  - img = image object to be masked
  - mask= binary image object (black background with white object)
  - mask_color= 'white' or 'black'  
  - device- Counter for image processing steps
  - debug- Default value is False, if True, masked intermediate image will be printed 

- **Context:**  
  - Apply a binary image mask over a grayscale or RGB image. Useful for seperating plant and background materials.

- **Example use:**  

 - [Use In Tutorial]()
 
  ```python
    import plantcv as pcv
    
    # Apply binary mask over an image. 
    
      device, masked_image = pcv.apply_mask(img, mask, 'white', device, debug=True)

  ```
  <a href="{{site.baseurl}}/img/documentation_images/logical_and/5_fill0.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/logical_and/5_fill0.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/logical_and/9_fill150.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/logical_and/9_fill150.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/logical_and/10_and_joined.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/logical_and/10_and_joined.png" width="200"></a><br>
  Figure 1. (Left) Original image 1. (Middle) Original image 2.(Right) Image combined with logical 'and' operation.  
 

