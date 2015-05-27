---
layout: docs
title: Documentation
subtitle: Laplace Filter
---

## Laplace Filter

This is a filtering method used to identify and highlight fine edges based on the 2nd derivative.

<font color='blue'>**laplace_filter(img, k, scale, device, debug=False)**</font><br>
<font color='orange'>**returns**</font> device, filtered image

    
- **Parameters:**   
  - img - binary image object. This image will be returned after filling.
  - k - apertures size used to calculate 2nd derivative filter, specifies the size of the kernel (must be an odd integer: 1,3,5...)
  - scale - scaling factor applied (multiplied) to computed Laplacian values (scale = 1 is unscaled) 
  - device - Counter for image processing steps
  - debug- Default value is False, if True, filled intermediate image will be printed 

- **Context:**  
  - Used to define edges around objects

- **Example use:**  

 - [Use In Tutorial](http://plantcv.danforthcenter.org/pages/documentation/function_docs/vis_tutorial.html)
 
  ```python
    import plantcv as pcv
    
    # Apply to a grayscale image
    # Filtered image will highlight areas of rapid pixel intensity change
    
    device, lp_img= pcv.laplace_filter(img, 1, 1, device, debug=True)

  ```
  <a href="{{site.baseurl}}/img/documentation_images/laplace_filter/NIR_SV_270_z2500.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/laplace_filter/NIR_SV_270_z2500.png" width="200"></a>   <a href="{{site.baseurl}}/img/documentation_images/laplace_filter/4_lp_out_k_1_scale_1_.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/laplace_filter/4_lp_out_k_1_scale_1_.png" width="200"></a><br>
  Figure 1. (Left) Original grayscale image. (Right) Image after Laplace filter applied.  
 

