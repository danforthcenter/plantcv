---
layout: docs
title: Documentation
subtitle: Erode
---

## Erode

Perform morphological 'erosion' filtering. Keeps pixel in center of the kernel if conditions set in kernel are true, otherwise removes pixel.

<font color='blue'>**erode(img, kernel, i, device, debug=False)**</font><br>
<font color='orange'>**returns**</font> device, image after erosion

    
- **Parameters:**   
  - img1 - Input image
  - kernel - Filtering window, you'll need to make your own using as such:  kernal = np.zeros((x,y), dtype=np.uint8), then fill the kernal with appropriate values
  - i - Iterations, i.e. the number of consecutive filtering passes
  - device - Counter for image processing steps
  - debug- Default value is False, if True, filled intermediate image will be printed

- **Context:**  
  - Used to perform morphological erosion filtering. Helps remove isolated noise pixels or remove boundary of objects.

- **Example use:**  

 - [Use In Tutorial](http://plantcv.danforthcenter.org/pages/documentation/function_docs/vis_tutorial.html)
 
  ```python
    import plantcv as pcv
    
    # Perform erosion filtering
    # Results in removal of isolated pixels or boundary of object removal
    
     device, er_img = pcv.erosion(img, kernel, 1 device, debug=True)

  ```
  <a href="{{site.baseurl}}/img/documentation_images/erosion/12_binary_threshold145_inv.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/erosion/12_binary_threshold145_inv.png" width="200"></a>   <a href="{{site.baseurl}}/img/documentation_images/erosion/16_er_image_itr_1.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/erosion/16_er_image_itr_1.png" width="200"></a><br>
  Figure 1. (Left) Original grayscale image. (Right) Image after erosion.  
 

