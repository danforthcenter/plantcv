---
layout: docs
title: Documentation
subtitle: image_subtract    
---

## image_subtract
Obtain a image of the pixelwise input values within two image files. This is a wrapper for the OpenCV function [] (http://docs.opencv.org/modules/core/doc/operations_on_arrays.html)

<font color='blue'><b>image_subtract(img, img2, device, debug=False)</font></b><br>
<font color='orange'>**returns**</font> device, subtracted image

- **Parameters:**   
  - img - image to be analyzed
  - img2 - image to subtract  
  - device - Counter for image processing steps
  - debug- Default value is False, if True, masked intermediate image will be printed 

- **Context:**  
  - Get feautures that are different between images

- **Example use:**  

 - [Use In Tutorial](http://plantcv.danforthcenter.org/pages/documentation/function_docs/flu_tutorial.html)
 
  ```python
    import plantcv as pcv
    
    # Subtract image from another image. 
    
      device, subtracted_img = pcv.image_subtract(img, img2,  device, debug=True)
  ```
  
  <a href="{{site.baseurl}}/img/documentation_images/image_sub/NIR_SV_270_z2500.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/image_sub/NIR_SV_270_z2500.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/image_sub/4_lp_out_k_1_scale_1_.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/image_sub/4_lp_out_k_1_scale_1_.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/image_sub/5_subtracted.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/image_sub/5_subtracted.png" width="200"></a>

  Figure 1. (Left) Original image. (Middle) Image to subtract. (Right) Image of pixel difference between input images. 
 
