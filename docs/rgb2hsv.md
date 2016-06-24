---
baseurl: https://github.com/{{ github_user }}/{{ github_repo }}/blob/{{ github_version }}{{ conf_py_path }}
---

## RGB to HSV

Convert image from RGB colorspace to HSV colorspace and split the channels.

<font color='blue'>**rgb2gray\_hsv(img, channel, device, debug=False)**</font><br>
<font color='orange'>**returns**</font> device, split image (h, s, or v channel)  
    
- **Parameters:**   
  - img- Image to be converted
  - channel- Split 'h' (hue), 's' (saturation), or 'v' (value) channel
  - device- Counter for image processing steps
  - debug- Default value is False, if True, RGB to HSV intermediate image will be printed 

- **Context:**  
  - Used to help differentiate plant and background

- **Example use:**  

 - [Use In Tutorial](http://plantcv.danforthcenter.org/pages/documentation/function_docs/vis_tutorial.html)
 
 
  ```python
    import plantcv as pcv
    
    # image converted from RGB to HSV, channels are then split. Hue ('h') channel is outputed.
    
    device, h_channel=pcv.rgb2gray_hsv(img, 'h', device, debug=True)
  ```
  
  <a href="{{baseurl}}/img/documentation_images/rgb2hsv/Dr7AB001192-2014-02-04 17_01_09-D001dr_012014-VIS_SV_180_z500.png" target="_blank"><img src="{{baseurl}}/img/documentation_images/rgb2hsv/Dr7AB001192-2014-02-04 17_01_09-D001dr_012014-VIS_SV_180_z500.png" width="200"></a>   <a href="{{baseurl}}/img/documentation_images/rgb2hsv/1_hsv_hue.png" target="_blank"><img src="{{baseurl}}/img/documentation_images/rgb2hsv/1_hsv_hue.png" width="200"></a><br>
  Figure 1. (Left) Original RGB image. (Right) Hue channel.  

   ```python
    import plantcv as pcv
    
    # image converted from RGB to HSV, channels are then split. Saturation ('s') channel is outputed.
    
    device, s_channel= pcv.rgb2gray_hsv(img, 's', device, debug=True)
  ```  

  <a href="{{baseurl}}/img/documentation_images/rgb2hsv/Dr7AB001192-2014-02-04 17_01_09-D001dr_012014-VIS_SV_180_z500.png" target="_blank"><img src="{{baseurl}}/img/documentation_images/rgb2hsv/Dr7AB001192-2014-02-04 17_01_09-D001dr_012014-VIS_SV_180_z500.png" width="200"></a>   <a href="{{baseurl}}/img/documentation_images/rgb2hsv/1_hsv_saturation.png" target="_blank"><img src="{{baseurl}}/img/documentation_images/rgb2hsv/1_hsv_saturation.png" width="200"></a><br>
  Figure 2. (Left) Original RGB image. (Right) Saturation channel.  

   
   ```python
    import plantcv as pcv
    
    # image converted from RGB to HSV, channels are then split. Value ('v') channel is outputed.
    
    device, v_channel=pcv.rgb2gray_hsv(img, 'v', device, debug=True)
  ```  
  
  <a href="{{baseurl}}/img/documentation_images/rgb2hsv/Dr7AB001192-2014-02-04 17_01_09-D001dr_012014-VIS_SV_180_z500.png" target="_blank"><img src="{{baseurl}}/img/documentation_images/rgb2hsv/Dr7AB001192-2014-02-04 17_01_09-D001dr_012014-VIS_SV_180_z500.png" width="200"></a>   <a href="{{baseurl}}/img/documentation_images/rgb2hsv/1_hsv_value.png" target="_blank"><img src="{{baseurl}}/img/documentation_images/rgb2hsv/1_hsv_value.png" width="200"></a><br>
  Figure 3. (Left) Original RGB image. (Right) Value channel.  

