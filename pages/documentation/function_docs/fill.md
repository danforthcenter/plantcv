---
layout: docs
title: Documentation
subtitle: Fill
---

## Fill

Identifies objects and fills objects that are less than specified size

<font color='blue'>**fill(img, mask, size, device, debug=False)**</font><br>
<font color='orange'>**returns**</font> device, filled image

    
- **Parameters:**   
  - img - binary image object. This image will be returned after filling.
  - mask - binary image object. This image will be used to identify image objects (contours).
  - size - minimum object area size in pixels (integer), smaller objects will be filled
  - device - Counter for image processing steps
  - debug- Default value is False, if True, filled intermediate image will be printed 

- **Context:**  
  - Used to reduce image noise

- **Example use:**  

 - [Use In Tutorial](http://plantcv.danforthcenter.org/pages/documentation/function_docs/vis_tutorial.html)
 
  ```python
    import plantcv as pcv
    
    # Apply fill to a binary image that has had a median blur applied.
    # Image mask is the same binary image with median blur.
    
    device, binary_img= pcv.median_blur(img, 5, device, debug=True)
    device, mask= pcv.median_blur(img, 5, device, debug=True)

    device, fill_image= pcv.fill(binary_img, mask, 200, device, debug=True)
  ```
  <a href="{{site.baseurl}}/img/documentation_images/fill/4_median_blur5.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/fill/4_median_blur5.png" width="200"></a>   <a href="{{site.baseurl}}/img/documentation_images/fill/5_fill200.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/fill/5_fill200.png" width="200"></a><br>
  Figure 1. (Left) Original binary image with median blur. (Right) Binary image with median blur and fill (200 pixels) applied.  
 

