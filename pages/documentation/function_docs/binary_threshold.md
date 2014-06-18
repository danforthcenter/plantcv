---
layout: docs
title: Documentation
subtitle: Binary Threshold
---

## Binary Threshold

Creates a binary image from a gray image based on the threshold values. The object target can be specified as dark or light.

<font color='blue'><b>binary\_threshold(img, threshold, maxValue, object\_type, device, debug=False)</b></font><br>
<font color='orange'><b>returns</b></font> device, thresholded image

- **Parameters:**   
  - img - grayscale img object
  - threshold - threshold value (0-255)
  - maxValue - value to apply above threshold (255 = white)
  - objecttype - 'light' or 'dark', is target image light or dark?
  - device- Counter for image processing steps
  - debug- Default value is False, if True, thresholded intermediate image will be printed 

- **Context:**  
  - Used to help differentiate plant and background

- **Example use:**  

 - [Use In Tutorial]()
 
  ```python
    import plantcv as pcv
    
    # Create binary image from a gray image based on threshold values. Targeting light objects in the image.
    
   device, threshold_light= pcv.binary_threshold(img, 36, 255, 'light', device, debug=True)
  ```
  <a href="{{site.baseurl}}/img/documentation_images/binary_threshold/1_hsv_saturation.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/binary_threshold/1_hsv_saturation.png" width="200"></a>   <a href="{{site.baseurl}}/img/documentation_images/binary_threshold/2_binary_threshold36.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/binary_threshold/2_binary_threshold36.png" width="200"></a><br>
  Figure 1. (Left) Original gray image. (Right) Thresholded image.  

   ```python
    import plantcv as pcv
    
    # Create binary image from a gray image based on threshold values. Targeting dark objects in the image.
    
    device, threshold_dark= pcv.binary_threshold(img, 36, 255, 'dark', device, debug=True)
  ```  
  <a href="{{site.baseurl}}/img/documentation_images/binary_threshold/1_hsv_saturation.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/binary_threshold/1_hsv_saturation.png" width="200"></a>   <a href="{{site.baseurl}}/img/documentation_images/binary_threshold/2_binary_threshold36_inv.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/binary_threshold/2_binary_threshold36_inv.png" width="200"></a><br>
  Figure 2. (Left) Original gray image. (Right) thresholded image.  

   
