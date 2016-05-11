---
layout: docs
title: Documentation
subtitle: VIS Pipeline
---

## Tutorial: VIS Image Pipeline

PlantCV is composed of modular functions that can be arranged (or rearranged) and adjusted quickly and easily.
Pipelines do not need to be linear (and often are not). Please see pipeline example below for more details.
Every function has a optional debug mode that prints out the resulting image.
This allows users to visualize and optimize each step on individual test images and small test sets before pipelines are deployed over whole data-sets.

**Workflow**  
1.  Optimize pipeline on individual image in debug mode.  
2.  Run pipeline on small test set (ideally that spans time and/or treatments).  
3.  Re-optimize pipelines on 'problem images' after manual inspection of test set.  
4.  Deploy optimized pipeline over test set using parallelization script.

**Running A Pipeline**

To run a VIS pipeline over a single VIS image there are two required inputs:

1.  **Image:** Images can be processed regardless of what type of VIS camera was used (High-throughput platform, digital camera, cell phone camera).
Image processing will work with adjustments if images are well lit and free of background that is similar in color to plant material.  
2.  **Output directory:** If debug mode is on output images from each step are produced, otherwise ~4 final output images are produced.

Optional inputs:  

*  **Debug Flag:**Prints an image at each step
*  **Region of Interest:**The user can input their own binary region of interest or image mask (make sure it is the same size as your image or you will have problems).

Sample command to run a pipeline on a single image:  

*  <font color='red'><b>Always test pipelines (preferably with -D flag for debug mode) before running over a full image set</b> </font>

<font color='orange'><b>[mgehan@pegasus]</b></font><font color='blue'><b> /home/mgehan/plantcv/scripts/dev/pipelinename.py -i /home/mgehan/images/testimg.png -o /home/mgehan/output-images -D</b></font>


**Walk Through A Sample Pipeline**

*  **Pipelines start by importing necessary packages, and by defining user inputs.**  

```python

#!/usr/bin/python
import sys, traceback
import cv2
import numpy as np
import argparse
import string
import plantcv as pcv

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Imaging processing with opencv")
  parser.add_argument("-i", "--image", help="Input image file.", required=True)
  parser.add_argument("-m", "--roi", help="Input region of interest file.", required=False)
  parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=True)
  parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", action="store_true")
  args = parser.parse_args()
  return args

```

*  **Start of the Main/Customizable portion of the pipeline.**  
*  **The image inputed by the used is read in.**  
*  **The device variable is just a counter so that each debug image is labeled in numerical order.**  

```python
### Main pipeline
def main():
  # Get options
  args = options()
  
  # Read image
  img, path, filename = pcv.readimage(args.image)
  #roi = cv2.imread(args.roi)
  
  # Pipeline step
  device = 0

```

<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3276_90.JPG" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3276_90.JPG" height="200"></a>    


**Figure 1.** Original image that has been read in.
This particular image was captured by a digital camera, just to show that PlantCV works on images not captured on a
[high-throughput phenotyping system](http://www.danforthcenter.org/scientists-research/core-technologies/phenotyping)
with idealized vis image capture conditions.

*  **In some pipelines (especially ones captured with a high-throughput phenotyping systems, where background is predictable) we first threshold out background**  
*  **In this particular pipeline we do some premasking of the background. The goal is to remove as much background as possible without thresholding-out the plant**  
*  **In order to perform a binary threshold on an image you need to select one of the color channels H,S,V,L,A,B,R,G,B.**  
*  **Here we convert the RGB image to HSV colorspace then extract the 's' or saturation channel (see more info [here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/rgb2hsv.html)), any channel can be selected based on user need.**  
*  **If some of the plant is missed or not visible then thresholded channels may be combined (a later step)**  

```python

  # Convert RGB to HSV and extract the Saturation channel
  device, s = pcv.rgb2gray_hsv(img, 's', device, args.debug)

```

<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/1_hsv_saturation.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/1_hsv_saturation.png" height="200"></a>  

**Figure 2.** Saturation channel from original RGB image converted to HSV colorspace.

*  **Next, the saturation channel is thresholded. The threshold can be on either light or dark objects in the image (see more info on threshold function [here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/binary_threshold.html)).**
*  **<font color='blue'>Tip: This step is often one that needs to be adjusted depending on the lighting and configurations of your camera system</font>** 

```python

  # Threshold the Saturation image
  device, s_thresh = pcv.binary_threshold(s, 85, 255, 'light', device, args.debug)

```
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/2_binary_threshold85.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/2_binary_threshold85.png" height="200"></a>  

**Figure 3.** Thresholded saturation channel image (Figure 2). Remaining objects are in white.  

*  **Again depending on the lighting, it will be possible to remove more/less background.**  
*  **A median blur (more info [here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/median_blur.html)) can be used to remove noise.**  
*  **<font color='blue'>Tip: Fill and median blur type steps should be used as sparingly as possible. Depending on the plant type (esp. grasses with thin leaves that often twist) you can lose plant material with a median blur that is too harsh.</font>**  

```python
  # Median Filter
  device, s_mblur = pcv.median_blur(s_thresh, 5, device, args.debug)
  device, s_cnt = pcv.median_blur(s_thresh, 5, device, args.debug)
  
```
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/3_median_blur5.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/3_median_blur5.png" height="200"></a>  

**Figure 4.** Thresholded saturation channel image with median blur.  

*  **<font color='orange'>Here is where the pipeline branches</font>**  
*  **The original image is used again to select the blue-yellow channel from LAB colorspace (more info on the function [here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/rgb2lab.html)).**  
*  **This image is again thresholded and there is an optional fill step that wasn't needed in this pipeline.**  

```python
# Convert RGB to LAB and extract the Blue channel
  device, b = pcv.rgb2gray_lab(img, 'b', device, args.debug)
  
  # Threshold the blue image
  device, b_thresh = pcv.binary_threshold(b, 160, 255, 'light', device, args.debug)
  device, b_cnt = pcv.binary_threshold(b, 160, 255, 'light', device, args.debug)
  
  # Fill small objects
  #device, b_fill = pcv.fill(b_thresh, b_cnt, 10, device, args.debug)
```
  
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3276_90.JPG" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3276_90.JPG" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/5_lab_blue-yellow.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/5_lab_blue-yellow.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/6_binary_threshold160.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/6_binary_threshold160.png" height="200"></a>

**Figure 5.** (Left) Original image. (Middle) Blue-yellow channel from LAB colorspace from original image. (Right) Thresholded blue-yellow channel image.

*  **Join the binary images from Figure 4 and Figure 5 with the Logical Or function (for more info on the Logical Or function see [here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/logical_or.html))**

```
  # Join the thresholded saturation and blue-yellow images
  device, bs = pcv.logical_or(s_mblur, b_cnt, device, args.debug)
  
```

<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/8_or_joined.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/8_or_joined.png" height="200"></a>

**Figure 6.** Joined binary images (Figure 4 and Figure 5).

*  **Next is to apply the binary image (Figure 6) as an image mask over the original image (For more info on mask function see [here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/apply_mask.html).
The point of this mask is really to exclude as much background with simple thresholding without leaving out plant material**

```
  # Apply Mask (for vis images, mask_color=white)
  device, masked = pcv.apply_mask(img, bs, 'white', device, args.debug)
```  
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3276_90.JPG" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3276_90.JPG" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/9_wmasked.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/9_wmasked.png" height="200"></a>

**Figure 7.** (Left) Original image. (Right) Masked image with background removed.

*  **<font color='orange'>Now we'll focus on capturing the plant in the masked image from Figure 7.</font>**    
*  **The masked green-magenta and blue-yellow channels are extracted**  
*  **Then the two channels are thresholded to capture different portions of the plant and the three images are joined together**
*  **The small objects are filled (for more info on the fill function see [here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/fill.html))**
*  **The resulting binary image is used to mask the masked image from figure 7.**  

```
  # Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
  device, masked_a = pcv.rgb2gray_lab(masked, 'a', device, args.debug)
  device, masked_b = pcv.rgb2gray_lab(masked, 'b', device, args.debug)
  
  # Threshold the green-magenta and blue images
  device, maskeda_thresh = pcv.binary_threshold(masked_a, 115, 255, 'dark', device, args.debug)
  device, maskeda_thresh1 = pcv.binary_threshold(masked_a, 135, 255, 'light', device, args.debug)
  device, maskedb_thresh = pcv.binary_threshold(masked_b, 128, 255, 'light', device, args.debug)
 
  # Join the thresholded saturation and blue-yellow images (OR)
  device, ab1 = pcv.logical_or(maskeda_thresh, maskedb_thresh, device, args.debug)
  device, ab = pcv.logical_or(maskeda_thresh1, ab1, device, args.debug)
  device, ab_cnt = pcv.logical_or(maskeda_thresh1, ab1, device, args.debug)
  
  # Fill small objects
  device, ab_fill = pcv.fill(ab, ab_cnt, 200, device, args.debug)

  # Apply mask (for vis images, mask_color=white)
  device, masked2 = pcv.apply_mask(masked, ab_fill, 'white', device, args.debug)

```
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/9_wmasked.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/9_wmasked.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/10_lab_green-magenta.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/10_lab_green-magenta.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/11_lab_blue-yellow.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/11_lab_blue-yellow.png" height="200"></a>  
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/12_binary_threshold115_inv.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/12_binary_threshold115_inv.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/13_binary_threshold135.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/13_binary_threshold135.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/14_binary_threshold128.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/14_binary_threshold128.png" height="200"></a>  
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/15_or_joined.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/15_or_joined.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/16_or_joined.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/16_or_joined.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/17_or_joined.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/17_or_joined.png" height="200"></a>  
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/18_fill200.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/18_fill200.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/19_wmasked.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/19_wmasked.png" height="200"></a>

**Figure 8.** Thresholding for plant material. The sample image used had very green leaves, but often (especially with stress treatments) there are yellowing or redish leaves or regions of necrosis.
The different thresholded channels capture different regions of the plant, then are combined into a mask for the image that was previously masked (figure 7).

*  **Now we need to identify the objects (called contours in OpenCV) within the image. For more information on this function see [here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/find_objects.html)**

```
  # Identify objects
  device, id_objects,obj_hierarchy = pcv.find_objects(masked2, ab_fill, device, args.debug)
```

<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/20_id_objects.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/20_id_objects.png" height="200"></a>

**Figure 9.** Here the objects (purple) are idenfied from the image from Figure 8. Even the spaces within an object are colored, but will have different hierarchy values.

*  **Next the region of interest is defined (this can be made on the fly, for more information see [here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/roi.html))**

```
  # Define ROI
  device, roi1, roi_hierarchy= pcv.define_roi(masked2,'rectangle', device, None, 'default', args.debug,True, 550, 0,-500,-1900)
```

<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/21_roi.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/21_roi.png" height="200"></a>

**Figure 10.** Region of interest drawn onto image. 

*  **Once the region of interest is defined you can decide to keep all of the contained and overlapping with that region of interest or cut the objects to the shape of the region of interest.
for more information see [here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/roi_objects.html)**

```
  # Decide which objects to keep
  device,roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img,'partial',roi1,roi_hierarchy,id_objects,obj_hierarchy,device, args.debug)
```

<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/22_obj_on_img.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/22_obj_on_img.png" height="200"></a>

**Figure 11.** Kept objects (green) drawn onto image.

*  **The isolated objects now should all be plant material. There, can however, be more than one object that makes up a plant, since
sometimes leaves twist making them appear in images as seperate objects. Therefore, in order for shape analysis to perform properly the plant
objects need to be combined into one object using the Combine Objects function
(for more info see [here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/object_composition.html)).**

```
  # Object combine kept objects
  device, obj, mask = pcv.object_composition(img, roi_objects, hierarchy3, device, args.debug)
```

<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/23_objcomp.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/23_objcomp.png" height="200"></a>

**Figure 12.** Outline (blue) of combined objects on the image. 

*  **<font color='orange'>The next step is to analyze the plant object for traits such as shape, or color.
For more info see Shape Function [here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/analyze_shape.html),
Color Function [here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/analyze_color.html),
and Boundary tool function [here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/boundary_tool.html)</font>**

```
############### Analysis ################  
  
  # Find shape properties, output shape image (optional)
  device, shape_header,shape_data,shape_img = pcv.analyze_object(img, args.image, obj, mask, device,args.debug,args.outdir+'/'+filename)
    
  # Shape properties relative to user boundary line (optional)
  device, boundary_header,boundary_data, boundary_img1= pcv.analyze_bound(img, args.image,obj, mask, 1680, device,args.debug,args.outdir+'/'+filename)
  
  # Determine color properties: Histograms, Color Slices and Pseudocolored Images, output color analyzed images (optional)
  device, color_header,color_data,norm_slice= pcv.analyze_color(img, args.image, kept_mask, 256, device, args.debug,'all','rgb','v','img',300,args.outdir+'/'+filename)
  
  # Output shape and color data
  pcv.print_results(args.image, shape_header, shape_data)
  pcv.print_results(args.image, color_header, color_data)
  pcv.print_results(args.image, boundary_header, boundary_data)
  
if __name__ == '__main__':
  main()

```
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3276_90_shapes.JPG" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3276_90_shapes.JPG" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3276_90_boundary1680.JPG" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3276_90_boundary1680.JPG" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3276_90_v_pseudo_on_img.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3276_90_v_pseudo_on_img.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3276_90_all_hist.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3276_90_all_hist.png" height="200"></a>

**Figure 13.** Output images from Sweet Potato trait analysis. (From left to right)Shape output image, boundary line output image, pseudocolored image (based on value channel), histogram of color values for each plant pixel.

##To demonstrate the importance of camera settings on pipeline construction, here are different species of plants captured with the same imaging setup (digital camera) and processed with the same imaging pipeline as above (no settings changed).

<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3275_90_shapes.JPG" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3275_90_shapes.JPG" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3275_90_boundary1680.JPG" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3275_90_boundary1680.JPG" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3275_90_v_pseudo_on_img.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3275_90_v_pseudo_on_img.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3275_90_all_hist.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3275_90_all_hist.png" height="200"></a>

**Figure 14.** Output images from Cassava trait analysis. (From left to right)Shape output image, boundary line output image, pseudocolored image (based on value channel), histogram of color values for each plant pixel.

<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3277_90_shapes.JPG" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3277_90_shapes.JPG" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3277_90_boundary1680.JPG" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3277_90_boundary1680.JPG" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3277_90_v_pseudo_on_img.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3277_90_v_pseudo_on_img.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3277_90_all_hist.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-vis-pipeline/IMG_3277_90_all_hist.png" height="200"></a>

**Figure 15.** Output images from Tomato trait analysis. (From left to right)Shape output image, boundary line output image, pseudocolored image (based on value channel), histogram of color values for each plant pixel.


##To deploy a pipeline over a full image set please see tutorial on Pipeline Parallelization [here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/pipeline_parallel.html).