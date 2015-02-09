---
layout: docs
title: Documentation
subtitle: Median Blur
---

## Median Blur

Applies a median blur filter. Applies median value to central pixel within a kernel size (ksize x ksize). The function is a wrapper for the OpenCV function [median blur](http://docs.opencv.org/doc/tutorials/imgproc/gausian_median_blur_bilateral_filter/gausian_median_blur_bilateral_filter.html_).  

<font color='blue'>**median\_blur(img, ksize, device, debug=False)**</font><br>
<font color='orange'>**returns**</font> device, blurred image

    
- **Parameters:**   
  - img - img object
  - ksize - kernel size => ksize x ksize box, must be an odd value
  - device - Counter for image processing steps
  - debug- Default value is False, if True, median blurred intermediate image will be printed 

- **Context:**  
  - Used to reduce image noise

- **Example use:**  

 - [Use In Tutorial](http://plantcv.danforthcenter.org/pages/documentation/function_docs/vis_tutorial.html)
 
  ```python
    import plantcv as pcv
    
    # Apply median blur to a binary image that has been previously thresholded.
    
   device, blur_5= pcv.median_blur(img, 5, device, debug=True)
  ```
  <a href="{{site.baseurl}}/img/documentation_images/median_blur/2_binary_threshold36.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/median_blur/2_binary_threshold36.png" width="200"></a>   <a href="{{site.baseurl}}/img/documentation_images/median_blur/4_median_blur5.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/median_blur/4_median_blur5.png" width="200"></a><br>
  Figure 1. (Left) Original thresholded image. (Right) Thresholded image with median blur (ksize=5) applied.  
 
  ```python
    import plantcv as pcv
    
    # Apply median blur to a binary image that has been previously thresholded.
    
   device, blur_11= pcv.median_blur(img, 11, device, debug=True)
  ```
  <a href="{{site.baseurl}}/img/documentation_images/median_blur/2_binary_threshold36.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/median_blur/2_binary_threshold36.png" width="200"></a>   <a href="{{site.baseurl}}/img/documentation_images/median_blur/3_median_blur11.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/median_blur/3_median_blur11.png" width="200"></a><br>
  Figure 2. (Left) Original thresholded image. (Right) Thresholded image with median blur (ksize=11) applied.  
   
