---
layout: docs
title: Documentation
subtitle: Histogram Equalization
---

## Histogram Equalization

This is a method used to normalize the distribution of signal intensity values within an image. If the image has low contrast it will make it easier to threshold.

<font color='blue'>**HistEqualization(img, device, debug=False)**</font><br>
<font color='orange'>**returns**</font> device, normalized image

    
- **Parameters:**   
  - img - the original 2 dimensional grayscale image for anaysis.
  - device - Counter for image processing steps
  - debug- Default value is False, if True, filled intermediate image will be printed

- **Context:**  
  - Used to normalize the distribution of a signal intensity within an image.

- **Example use:**  

 - [Use In Tutorial](http://plantcv.danforthcenter.org/pages/documentation/function_docs/vis_tutorial.html)
 
  ```python
    import plantcv as pcv
    
    # Examine signal distribution within an image
    # prints out an image histogram of signal within image
    
     device, he_img = pcv.HistEqualization(img, device, debug=True)

  ```
  <a href="{{site.baseurl}}/img/documentation_images/histogram_equalization/NIR_SV_270_z2500.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/histogram_equalization/NIR_SV_270_z2500.png" width="200"></a>   <a href="{{site.baseurl}}/img/documentation_images/histogram_equalization/3_hist_equal_img.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/histogram_equalization/3_hist_equal_img.png" width="200"></a><br>
  Figure 1. (Left) Original grayscale image. (Right) Image after histogram equalization.  
 

