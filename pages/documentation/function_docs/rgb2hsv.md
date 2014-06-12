---
layout: docs
title: Documentation
subtitle: RGB to HSV
---

## RGB to HSV

Convert image from RGB colorspace to HSV colorspace and split the channels.

<font color='blue'>**rgb2gray_hsv(img, channel, device, debug=False)**</font> 
    
- **Parameters:**   
  - img- Image to be converted
  - channel- Split 'h' (hue), 's' (saturation), or 'v' (value) channel
  - device- Counter for image processing steps
  - debug- Default value is False, if True, RGB to HSV intermediate image will be printed 

- **Context:**  
  - Used to help differentiate plant and background

- **Example use:**

 - [Use In Tutorial]()
 
  ```python
    import plantcv as pcv
    
    # image converted from RGB to HSV, channels are then split. Saturation ('h') channel is outputed.
    
    pcv.rgb2gray_hsv(img, 'h', device, debug='True')
  ```
  
  <a href="{{site.baseurl}}/img/documentation_images/rgb2hsv/Dr7AB001192-2014-02-04 17_01_09-D001dr_012014-VIS_SV_180_z500.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/rgb2hsv/Dr7AB001192-2014-02-04 17_01_09-D001dr_012014-VIS_SV_180_z500.png" width="200"></a>   <a href="{{site.baseurl}}/img/documentation_images/rgb2hsv/1_hsv_hue.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/rgb2hsv/1_hsv_hue.png" width="200"></a>

   ```python
    import plantcv as pcv
    
    # image converted from RGB to HSV, channels are then split. Saturation ('s') channel is outputed.
    
    pcv.rgb2gray_hsv(img, 's', device, debug='True')
  ```  

  <a href="{{site.baseurl}}/img/documentation_images/rgb2hsv/Dr7AB001192-2014-02-04 17_01_09-D001dr_012014-VIS_SV_180_z500.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/rgb2hsv/Dr7AB001192-2014-02-04 17_01_09-D001dr_012014-VIS_SV_180_z500.png" width="200"></a>   <a href="{{site.baseurl}}/img/documentation_images/rgb2hsv/1_hsv_saturation.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/rgb2hsv/1_hsv_saturation.png" width="200"></a>

   
   ```python
    import plantcv as pcv
    
    # image converted from RGB to HSV, channels are then split. Saturation ('v') channel is outputed.
    
    pcv.rgb2gray_hsv(img, 'v', device, debug='True')
  ```  
  
  <a href="{{site.baseurl}}/img/documentation_images/rgb2hsv/Dr7AB001192-2014-02-04 17_01_09-D001dr_012014-VIS_SV_180_z500.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/rgb2hsv/Dr7AB001192-2014-02-04 17_01_09-D001dr_012014-VIS_SV_180_z500.png" width="200"></a>   <a href="{{site.baseurl}}/img/documentation_images/rgb2hsv/1_hsv_value.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/rgb2hsv/1_hsv_value.png" width="200"></a>

