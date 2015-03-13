---
layout: docs
title: Documentation
subtitle: Image_add
---

## Image add

This is a method used to perform pixelwise addition between images. The numpy addition function '+' is used. This is a modulo operation rather than the cv2.add fxn which is a saturation operation.

<font color='blue'>**image_add(img1, img2, device, debug=False)**</font><br>
<font color='orange'>**returns**</font> device, image of the sum of both images

    
- **Parameters:**   
  - img1 - image to add
  - img2 - image to add
  - device - Counter for image processing steps
  - debug- Default value is False, if True, filled intermediate image will be printed

- **Context:**  
  - Used to combine/stack the pixelwise intensity found in two images

- **Example use:**  

 - [Use In Tutorial](http://plantcv.danforthcenter.org/pages/documentation/function_docs/vis_tutorial.html)
 
  ```python
    import plantcv as pcv
    
    # Add two images together
    # Results to combine/stack the pixelwise intensity found in two images
    
     device, sum_img = pcv.image_add(img1, img2 device, debug=True)

  ```
  <a href="{{site.baseurl}}/img/documentation_images/image_add/6_sb_img_dx_1_dy_0_k_1.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/image_add/6_sb_img_dx_1_dy_0_k_1.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/image_add/7_sb_img_dx_0_dy_1_k_1.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/image_add/7_sb_img_dx_0_dy_1_k_1.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/image_add/8_added.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/image_add/8_added.png" width="200"></a>
 
  Figure 1. (Left) Image to add. (Middle) Image to add. (Right) Sum of both images.  
 

