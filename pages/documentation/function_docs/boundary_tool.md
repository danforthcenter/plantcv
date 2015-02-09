---
layout: docs
title: Documentation
subtitle: Boundary Tool
---

## Boundary Tool

Set boundary line with boundary tool, this allows the user to find the extent-y ('height') above and below as well as the area above and below the boundary line. This tool functions best if the pot size/position of the plant remains relatively constant.
 
<font color='blue'><b>analyze\_bound(img,imgname, obj, mask, line\_position, device , debug=False, filename=False)</b></font><br>
<font color='orange'><b>returns</b></font> device, boundary headers, boundary data, image with boundary data<br>

- **Parameters:**   
  - img - image object (most likely the original), color(RGB)
  - imgname - name of image
  - obj - single or grouped contour object
  - mask - binary mask of selected contours
  - line\_position = position of boundry line (a value of 0 would draw the line through the bottom of the image)
  - device - Counter for image processing steps
  - debug - Default value is False, if True, intermediate image with boundary line will be printed 
  - filename - False or image name. If defined print image

- **Context:**  
  - Used to define a boundary line for the image, to find the height above and below as well as area above and below a boundary line.
  - Could also be used as a method of flagging images about to go out-of-bounds (this QC tool will be added later)

- **Example use:**  

 - [Use In Tutorial](http://plantcv.danforthcenter.org/pages/documentation/function_docs/vis_tutorial.html)
 
  ```python
    import plantcv as pcv
    
    # Set Boundary Line
        
    device, boundary_header,boundary_data, boundary_img1= pcv.analyze_bound(img, imgname,obj, mask, 950, device, debug=True,/home/malia/setaria_boundary_img.png)

  ```
  <a href="{{site.baseurl}}/img/documentation_images/boundary_line/Dp1AA002296-2014-01-28 14_00_16-D001dr_012014-VIS_SV_90_z1000 copy.png_boundary950.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/boundary_line/Dp1AA002296-2014-01-28 14_00_16-D001dr_012014-VIS_SV_90_z1000 copy.png_boundary950.png" width="200">
  <a href="{{site.baseurl}}/img/documentation_images/boundary_line/Dr2AB000332-2013-12-18 12_16_05-B2_120513-VIS_SV_270_z700.png_boundary_shapes.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/boundary_line/Dr2AB000332-2013-12-18 12_16_05-B2_120513-VIS_SV_270_z700.png_boundary_shapes.png" width="200"></a><br>  
  Figure 1. (Left) Boundary line set at 950, purple line is boundary line, blue line is extent y above boundary line, green is area above boundary line. (Right) Boundary line set at 330, purple is boundary line, blue line is extent y above boundary line, green line is extent y below boundary line, green is area above boundary line and red is area below boundary line. 
 

