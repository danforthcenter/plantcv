---
layout: docs
title: Documentation
subtitle: Analyze FLU
---

## Analyze FLU Signal

Extract color data of objects and produce pseudocolored images, can extract data for RGB (Red, Green, Blue), HSV (Hue, Saturation, Value) and LAB (Lightness, Green-Magenta, Blue Yellow) channels.

<font color='blue'><b>fluor\_fvfm (fdark,fmin,fmax,mask, device,filename,bins=1000, debug=False)</b></font><br>
<font color='orange'><b>returns</b></font> device, FLU channel histogram headers, FLU channel histogram data, normalized color slice data<br>

- **Parameters:**   
  - fdark - image object, grayscale  
  - fmin - image object  grayscale
  - fmax - image object, grayscale
  - mask - binary mask of selected contours
  - device - Counter for image processing steps
  - filename - False or image name. If defined print image
  - bins - number of grayscale bins (0-256 for 8-bit images and 0 to 65,536), if you would like to bin data, you would alter this number
  - debug - Default value is False, if True, intermediate image with boundary line will be printed
   
   
- **Context:**  
  - Used to extract fv/fm per identified plant pixel.
  - Generates histogram of fv/fm data.
  - Generaes pseudocolored output image with fv/fm values per plant pixel.

- **Example use:**  

 - [Use In Tutorial](http://plantcv.danforthcenter.org/pages/documentation/function_docs/flu_tutorial.html)
 
  ```python
    import plantcv as pcv
    
    # Analyze Fv/Fm
        
     device, fvfm_header, fvfm_data=pcv.fluor_fvfm(fdark,fmin,fmax,kept_mask, device, filename, 1000, debug=True)

  ```
  <a href="{{site.baseurl}}/img/documentation_images/analyze_flu/FLUO_TV_z630_820438c.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/analyze_flu/FLUO_TV_z630_820438c.png" height="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/analyze_flu/FLUO_TV_z630_820439c.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/analyze_flu/FLUO_TV_z630_820439c.png" height="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/analyze_flu/FLUO_TV_z630_820440c.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/analyze_flu/FLUO_TV_z630_820440c.png" height="200"></a>  
  **Figure 1.** (Left)Fdark image. (Middle) Fmin image. (Right) Fmax image.

  <a href="{{site.baseurl}}/img/documentation_images/analyze_flu/FLUO_TV_z630_820440c_fvfm_hist.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/analyze_flu/FLUO_TV_z630_820440c_fvfm_hist.png" height="200"></a>
  <a href="{{site.baseurl}}/img/documentation_images/analyze_flu/FLUO_TV_z630_820440c_pseudo_fvfm.png" target="_blank">
  <img src="{{site.baseurl}}/img/documentation_images/analyze_flu/FLUO_TV_z630_820440c_pseudo_fvfm.png" height="200"></a>  
  **Figure 2.** (Left) Histogram of Fv/Fm values from id. (Right) Pseudocolored output image based on fv/fm values.
 

