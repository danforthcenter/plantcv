---
layout: docs
title: Documentation
subtitle: Apply Mask    
---

## Apply Mask

Apply binary mask to an image.

<font color='blue'><b>apply\_mask(img, mask, mask\_color, device, debug=False)</font></b><br>
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

 - [Use In Tutorial](http://plantcv.danforthcenter.org/pages/documentation/function_docs/vis_tutorial.html)
 
  ```python
    import plantcv as pcv
    
    # Apply binary 'white' mask over an image. 
    
      device, masked_image = pcv.apply_mask(img, mask, 'white', device, debug=True)
  ```
  
  <a href="{{site.baseurl}}/img/documentation_images/apply_mask/VIS_SV_180_z2500_349810.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/apply_mask/VIS_SV_180_z2500_349810.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/apply_mask/10_and_joined.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/apply_mask/10_and_joined.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/apply_mask/11_wmasked.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/apply_mask/11_wmasked.png" width="200"></a><br>
  Figure 1. (Left) Original image. (Middle) Binary mask. (Right) White masked image. 
 
  ```python
    import plantcv as pcv
    
    # Apply binary 'black' mask over an image. 
    
      device, masked_image = pcv.apply_mask(img, mask, 'black', device, debug=True)
  ```
  
  <a href="{{site.baseurl}}/img/documentation_images/apply_mask/VIS_SV_180_z2500_349810.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/apply_mask/VIS_SV_180_z2500_349810.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/apply_mask/10_and_joined.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/apply_mask/10_and_joined.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/apply_mask/11_bmasked.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/apply_mask/11_bmasked.png" width="200"></a><br>
  Figure 2. (Left) Original image. (Middle) Binary mask. (Right) Black masked image. 
