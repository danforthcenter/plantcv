---
layout: docs
title: Documentation
subtitle: RGB to LAB
---

## RGB to LAB

Convert image from RGB colorspace to LAB colorspace and split the channels.

<font color='blue'>**rgb2gray\_hsv(img, channel, device, debug=False)**</font><br>
<font color='orange'>**returns**</font> device, split image (l, a, or b channel)  
    
- **Parameters:**   
  - img- Image to be converted
  - channel- Split 'l' (lightness), 'a' (green-magenta), or 'b' (blue-yellow) channel
  - device- Counter for image processing steps
  - debug- Default value is False, if True, RGB to LAB intermediate image will be printed 

- **Context:**  
  - Used to help differentiate plant and background

- **Example use:**  

 - [Use In Tutorial](http://plantcv.danforthcenter.org/pages/documentation/function_docs/vis_tutorial.html)
 
 
  ```python
    import plantcv as pcv
    
    # image converted from RGB to LAB, channels are then split. Lightness ('l') channel is outputed.
    
    device, l_channel=pcv.rgb2gray_lab(img, 'l', device, debug=True)
  ```
  
  <a href="{{site.baseurl}}/img/documentation_images/rgb2lab/Dr7AB001192-2014-02-04 17_01_09-D001dr_012014-VIS_SV_180_z500.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/rgb2lab/Dr7AB001192-2014-02-04 17_01_09-D001dr_012014-VIS_SV_180_z500.png" width="200"></a>   <a href="{{site.baseurl}}/img/documentation_images/rgb2lab/6_lab_lightness.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/rgb2lab/6_lab_lightness.png" width="200"></a><br>
  Figure 1. (Left) Original RGB image. (Right) Lightness channel.  

   ```python
    import plantcv as pcv
    
    # image converted from RGB to LAB, channels are then split. Green-Magenta ('a') channel is outputed.
    
    device, a_channel= pcv.rgb2gray_lab(img, 'a', device, debug=True)
  ```  

  <a href="{{site.baseurl}}/img/documentation_images/rgb2lab/Dr7AB001192-2014-02-04 17_01_09-D001dr_012014-VIS_SV_180_z500.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/rgb2lab/Dr7AB001192-2014-02-04 17_01_09-D001dr_012014-VIS_SV_180_z500.png" width="200"></a>   <a href="{{site.baseurl}}/img/documentation_images/rgb2lab/6_lab_green-magenta.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/rgb2lab/6_lab_green-magenta.png" width="200"></a><br>
  Figure 2. (Left) Original RGB image. (Right) Green-Magenta channel.  

   
   ```python
    import plantcv as pcv
    
    # image converted from RGB to Lab, channels are then split. Blue-Yellow ('b') channel is outputed.
    
    device, b_channel=pcv.rgb2gray_lab(img, 'b', device, debug=True)
  ```  
  
  <a href="{{site.baseurl}}/img/documentation_images/rgb2lab/Dr7AB001192-2014-02-04 17_01_09-D001dr_012014-VIS_SV_180_z500.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/rgb2lab/Dr7AB001192-2014-02-04 17_01_09-D001dr_012014-VIS_SV_180_z500.png" width="200"></a>   <a href="{{site.baseurl}}/img/documentation_images/rgb2lab/6_lab_blue-yellow.png" target="_blank"><img src="{{site.baseurl}}/img/documentation_images/rgb2lab/6_lab_blue-yellow.png" width="200"></a><br>
  Figure 3. (Left) Original RGB image. (Right) Blue-Yellow channel.  

