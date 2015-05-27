---
layout: docs
title: Documentation
subtitle: Plot Histogram
---

## Plot Histogram

This is a plotting method used to examine the distribution of signal within an image.

<font color='blue'>**plot_hist(img, 'hist_name')**</font><br>
<font color='orange'>**returns**</font> no return value; makes a plot

    
- **Parameters:**   
  - img - the original 2-dimensional grayscale image for anaysis.
  - name - the name of the output plot

- **Context:**  
  - Examine the distribution of the signal, this help you select a value for binary thresholding.

- **Example use:**  

 - [Use In Tutorial](http://plantcv.danforthcenter.org/pages/documentation/function_docs/vis_tutorial.html)
 
  ```python
    import plantcv as pcv
    
    # Examine signal distribution within an image
    # prints out an image histogram of signal within image
    
    pcv.plot_hist(img, 'hist_img')

  ```
  <a href="{{site.baseurl}}/img/documentation_images/fill/4_median_blur5.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/fill/4_median_blur5.png" width="200"></a>   <a href="{{site.baseurl}}/img/documentation_images/fill/5_fill200.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/fill/5_fill200.png" width="200"></a><br>
  Figure 1. (Left) Original grayscale image. (Right) Histogram of signal intensity..  
 

