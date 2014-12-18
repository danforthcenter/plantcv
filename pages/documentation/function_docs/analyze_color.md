---
layout: docs
title: Documentation
subtitle: Analyze Color
---

## Analyze Color

Extract color data of objects and produce pseudocolored images, can extract data for RGB (Red, Green, Blue), HSV (Hue, Saturation, Value) and LAB (Lightness, Green-Magenta, Blue Yellow) channels.

<font color='blue'><b>analyze\_color(img, imgname, mask, bins, device, debug=False, hist\_plot\_type ='all', cslice\_type='rgb', pseudo\_channel='v', filename=False)</b></font><br>
<font color='orange'><b>returns</b></font> device, color channel histogram headers, color channel histogram data, normalized color slice data<br>

- **Parameters:**   
  - img - image object (most likely the original), color(RGB)
  - imgname - name of image
  - mask - binary mask of selected contours
  - bins - number of color bins (0-256), if you would like to bin data, you would alter this number
  - device - Counter for image processing steps
  - debug - Default value is False, if True, intermediate image with boundary line will be printed
  - hist\_plot\_type - 'None', 'all', 'rgb','lab' or 'hsv', this is the data to be printed to an SVG histogram file, however all (every channel) data is still stored to the database.
  - color\_slice\_type - 'None', 'rgb', 'hsv' or 'lab', this is the type of color-slice image to print. There is also an additional script [here]() to generate color slice images from data stored in the sqlite database.
  - pseudo\_channel - 'None', 'r'(red), 'g'(green), 'b'(blue), 'l' (lightness), 'm' (green-magenta), 'y' (blue-yellow), 'h'(hue),'s'(saturation), or 'v'(value), creates pseduocolored image based on the specified channel.
  - filename - False or image name. If defined print image
   
   
- **Context:**  
  - Used to extract color data from RGB, LAB, and HSV color channels.
  - Generates histogram of color channel data.
  - Generaes pseudocolored output image of one of the channels specified.
  - Generates color slice output image (for more information see [here]())

- **Example use:**  

 - [Use In Tutorial]()
 
  ```python
    import plantcv as pcv
    
    # Analyze Color
        
    device, color_header, color_data, norm_slice= pcv.analyze_color(img, imagename, mask, 256, device, debug=True, 'all', 'rgb', 'v', /home/malia/analyze_color.png)

  ```
  <a href="{{site.baseurl}}/img/documentation_images/analyze_color/Dp1AA002292-2014-02-05 16_28_08-D001dr_012014-VIS_TV_z1.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/analyze_color/Dp1AA002292-2014-02-05 16_28_08-D001dr_012014-VIS_TV_z1.png" width="200"><a><br>
  <a href="{{site.baseurl}}/img/documentation_images/analyze_color/Dp1AA002292-2014-02-05 16_28_08-D001dr_012014-VIS_TV_z1png_all_hist.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/analyze_color/Dp1AA002292-2014-02-05 16_28_08-D001dr_012014-VIS_TV_z1png_all_hist.png" width="200"><a>  
  <a href="{{site.baseurl}}/img/documentation_images/analyze_color/Dp1AA002292-2014-02-05 16_28_08-D001dr_012014-VIS_TV_z1png_v_pseduo_on_img.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/analyze_color/Dp1AA002292-2014-02-05 16_28_08-D001dr_012014-VIS_TV_z1png_v_pseduo_on_img.png" width="200"><a>
  <a href="{{site.baseurl}}/img/documentation_images/analyze_color/Dp1AA002292-2014-01-30 16_26_56-D001dr_012014-VIS_TV_z1000png_rgb_norm_slice.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/analyze_color/Dp1AA002292-2014-01-30 16_26_56-D001dr_012014-VIS_TV_z1000png_rgb_norm_slice.png" width="11" height="200"></a><br>  
  Figure 1. 
 

