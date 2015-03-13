---
layout: docs
title: Documentation
subtitle: Sobel Filter
---

## Sobel Filter

This is a filtering method used to identify and highlight coarse changes in pixel intensity based on the 1st derivative.

<font color='blue'>**sobel_filter(img, k, scale, device, debug=False)**</font><br>
<font color='orange'>**returns**</font> device, filtered image

    
- **Parameters:**   
  - img - binary image object. This image will be returned after filling.
  - dx - derivative of x to analyze (1-3)
  - dy = derivative of y to analyze (1-3)
  - k - apertures size used to calculate 2nd derivative filter, specifies the size of the kernel (must be an odd integer: 1,3,5...)
  - scale - scaling factor applied (multiplied) to computed Laplacian values (scale = 1 is unscaled) 
  - device - Counter for image processing steps
  - debug- Default value is False, if True, filled intermediate image will be printed 

- **Context:**  
  - Used to define edges within and around objects

- **Example use:**  

 - [Use In Tutorial](http://plantcv.danforthcenter.org/pages/documentation/function_docs/vis_tutorial.html)
 
  ```python
    import plantcv as pcv
    
    # Apply to a grayscale image
    # Filtered image will highlight areas of coarse pixel intensity change based on 1st derivative
    
    device, lp_img= pcv.sobel_filter(img, 1, 0, 1, device, debug=True)
    device, lp_img= pcv.sobel_filter(img, 0, 1, 1, device, debug=True)

  ```
  <a href="{{site.baseurl}}/img/documentation_images/sobel_filter/NIR_SV_270_z2500.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/sobel_filter/NIR_SV_270_z2500.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/sobel_filter/6_sb_img_dx_1_dy_0_k_1.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/sobel_filter/6_sb_img_dx_1_dy_0_k_1.png" width="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/sobel_filter/7_sb_img_dx_0_dy_1_k_1.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/sobel_filter/7_sb_img_dx_0_dy_1_k_1.png" width="200"></a>
  
  Figure 1. (Left) Original grayscale image.(Middle) Image after Sobel filter applied to x-axis. (Right) Image after Sobel filter applied to y-axis.  
 

