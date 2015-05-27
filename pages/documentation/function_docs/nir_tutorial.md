---
layout: docs
title: Documentation
subtitle: NIR Pipeline
---

## Tutorial: NIR Image Pipeline

PlantCV is composed of modular functions that can be arranged (or rearranged) and adjusted quickly and easily. We hope that you can use these functions and pipelines as a starting place for your project. The goal is to provide practical examples of image processing algorithms.


Pipelines do not need to be linear (and often as are not, as seen in this example).
Every PlantCV function has a optional debug mode that prints out the resulting image.
This allows users to visualize and optimize each step on individual test images and small test sets before pipelines are deployed over whole image data sets.

**Workflow**  
1.  Optimize pipeline on individual image in debug mode.  
2.  Run pipeline on small test set (ideally that spans time and/or treatments).  
3.  Re-optimize pipelines on 'problem images' after manual inspection of test set.  
4.  Deploy optimized pipeline over test set using parallelization script.

**Running A Pipeline**

To run a NIR pipeline over a single NIR image there are three required inputs:

1.  **Image:** NIR images are grayscale matricies (1 dimensional).
In principle, image processing will work on any grayscale image with adjustments if images are well lit and there is appreciable contrast difference between the object of interest and the background.  
2.  **Output directory:** If debug mode is on output images from each step are produced, otherwise ~4 final output images are produced.
3.  **Image of estimated background:** Right now this is hardcoded into the pipeline (different background at each zoom level) and not implemented as an argument.

Optional inputs:  

*  **Debug Flag:**Prints an image at each step
*  **Region of Interest:**The user can input their own binary region of interest or image mask (make sure it is the same size as your image or you will have problems).

Sample command to run a pipeline on a single image:  

*  <font color='red'><b>Always test pipelines (preferably with -D flag for debug mode) before running over a full image set</b> </font>

<font color='orange'><b>[user@servername]</b></font><font color='blue'><b> /home/user/plantcv/scripts/dev/pipelinename.py -i /home/user/images/testimg.png -o /home/user/output-images -D</b></font>


##Walk through a sample pipeline##

*  **Pipelines start by importing necessary packages, and by defining user inputs.**  

```python

#!/usr/bin/python
import sys, traceback
import cv2
import numpy as np
import argparse
import string
import plantcv as pcv

def options():
parser = argparse.ArgumentParser(description="Imaging processing with opencv")
parser.add_argument("-i", "--image", help="Input image file.", required=True)
parser.add_argument("-m", "--roi", help="Input region of interest file.", required=False)
parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", action="store_true")
args = parser.parse_args()
return args

```

*  **Start of the Main/Customizable portion of the pipeline.**  
*  **The image selected by the -i flag is read in.**  
*  **The device variable is just a counter so that each debug image is labeled in numerical order.**

##Lets start by using a background subtraction approach to object identification

```python
### Main pipeline
def main():

  # Get options
  args = options()

  if args.debug:
  print("Debug mode turned on...")
  
  # Read image (Note: flags=0 indicates to expect a grayscale image)
  img = cv2.imread(args.image, flags=0)
  
  # Get directory path and image name from command line arguments
  path, img_name = os.path.split(args.image)
  
  # Read in image which is the pixelwise average of background images
  img_bkgrd = cv2.imread("/home/user/LemnaTec/ddpsc_image_git/docs/background_nir_z2500.png", flags=0)


  # Pipeline step
  device = 0

```

<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/NIR_SV_270_z2500_347831.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/NIR_SV_270_z2500_347831.png" height="200"></a> 
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/bkgrd_ave_z2500.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/bkgrd_ave_z2500.png" height="200"></a>    


**Figure 1.** (Left) Original image that has been read in. (Right) The average signal of the empty pots calculated across all days.
These are representative side view images captured using a NIR camera at the [Bellweather Foundation Phenotyping Facility](http://www.danforthcenter.org/scientists-research/core-technologies/phenotyping).

*  **Notice that sometimes it is easier to use pre-built OpenCV functions. In most situations the documentation is quite good. However for more complex operations (those that require multiple OpenCV functions), I would recommend writing a PlantCV subroutine.**
*  **First lets examine how efficently we can capture the plant, then we will worry about masking problematic background objects.**


```python
  # Subtract the background image from the image with the plant. 
  device, bkg_sub_img = pcv.image_subtract(img, img_bkgrd, device, args.debug)
  
  # Threshold the image of interest using the two-sided cv2.inRange function (keep what is between 50-190)
  bkg_sub_thres_img = cv2.inRange(bkg_sub_img, 50, 190)
  if args.debug:
    cv2.imwrite('bkgrd_sub_thres.png', bkg_sub_thres_img)
```

<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/1_subtracted_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/1_subtracted_t.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/bkgrd_sub_thres_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/bkgrd_sub_thres_t.png" height="200"></a>  

**Figure 2.** (Left) Image after subtraction of average background pixels. (Right) Image after two-sided thresholding applied to isolate plant material.

* **Images were subtracted using the PlantCV image_subtract function. This function is built using the numpy '-' operator. It is a modulo operator rather than a saturation operator.**
* **Thresholding was done using the OpenCV inRange function. Pixels that have a signal value less than 50 and greater than 190 will be set to 0 (black), while those with a value between these two will be set to 255 (white).**
* **This approach works very well if you have image of the background without plant material.**

##Image sharpening approach to improve object of interest thresholding 

* **This will improve your ability to maximize the amount of plant material captured, and is particularily useful if estimating background pixel intensity is problematic.**

```python
  # Laplace filtering (identify edges based on 2nd derivative)
  device, lp_img = pcv.laplace_filter(img, 1, 1, device, args.debug)
  if args.debug:
    pcv.plot_hist(lp_img, 'hist_lp')

  # Lapacian image sharpening, this step will enhance the darkness of the edges detected
  device, lp_shrp_img = pcv.image_subtract(img, lp_img, device, args.debug)
  if args.debug:
    pcv.plot_hist(lp_shrp_img, 'hist_lp_shrp')
```

<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/4_lp_out_k_1_scale_1_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/4_lp_out_k_1_scale_1_t.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/5_subtracted_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/5_subtracted_t.png" height="200"></a>  

**Figure 3.** (Left) Result after second derivative Laplacian filter is applied to the original grayscale image. (Right) Result after subtracting the Laplacian filtered image from the original image (sharpening).

* **Subtracting this filtered image from the original image increases the contrast between plant and background if the border between the two objects is distinct.**
* **Notice the plant is darker in this image than it was in the original image.**

```python
  # Sobel filtering  
  # 1st derivative sobel filtering along horizontal axis, kernel = 1, unscaled)
  device, sbx_img = pcv.sobel_filter(img, 1, 0, 1, 1, device, args.debug)
  if args.debug:
    pcv.plot_hist(sbx_img, 'hist_sbx')

  # 1st derivative sobel filtering along vertical axis, kernel = 1, unscaled)
  device, sby_img = pcv.sobel_filter(img, 0, 1, 1, 1, device, args.debug)
  if args.debug:
    pcv.plot_hist(sby_img, 'hist_sby')

  # Combine the effects of both x and y filters through matrix addition
  # This will capture edges identified within each plane and emphesize edges found in both images
  device, sb_img = pcv.image_add(sbx_img, sby_img, device, args.debug)
  if args.debug:
    pcv.plot_hist(sb_img, 'hist_sb_comb_img')
```

<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/6_sb_img_dx_1_dy_0_k_1_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/6_sb_img_dx_1_dy_0_k_1_t.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/7_sb_img_dx_0_dy_1_k_1_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/7_sb_img_dx_0_dy_1_k_1_t.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/8_added_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/8_added_t.png" height="200"></a>  

**Figure 4.** (Left) Result after first derivative Sobel filter is applied to the x-axis of the original image. (Middle)  Result after first derivative Sobel filter is applied to the y-axis of the original image. (Right) Result after adding the two Sobel filtered images together.

* **First derivative (Sobel) filters highlight more ambigious boundaries within the image. These are typically applied across each axis individually.**
* **Combining both Sobel filters images through addition high-lights these regions where the texture changes across both axis.**

```python
  # Use a lowpass (blurring) filter to smooth sobel image
  device, mblur_img = pcv.median_blur(sb_img, 1, device, args.debug)
  device, mblur_invert_img = pcv.invert(mblur_img, device, args.debug)

  # combine the smoothed sobel image with the laplacian sharpened image
  # combines the best features of both methods as described in "Digital Image Processing" by Gonzalez and Woods pg. 169 
  device, edge_shrp_img = pcv.image_add(mblur_invert_img, lp_shrp_img, device, args.debug)
  if args.debug:
    pcv.plot_hist(edge_shrp_img, 'hist_edge_shrp_img')

  # Perform thresholding to generate a binary image
    device, tr_es_img = pcv.binary_threshold(edge_shrp_img, 145, 255, 'dark', device, args.debug)
```

<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/10_invert_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/10_invert_t.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/11_added_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/11_added_t.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/12_binary_threshold145_inv_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/12_binary_threshold145_inv_t.png" height="200"></a>  

**Figure 5.** (Right) Sobel filtered image after application of a median blur filter and inversion. (Middle) Resulting image after adding the image on the right to the Laplacian sharpened image. (Left) Resulting image after binary thresholding of sharpened image.

* **Median blur filtering decreases the amount of noise present in Sobel filtered images.**
* **Adding this (inverted, Sobel filtered) image to the Laplacian filtered image further increases the contrast between the plant and background.**
* **Increased contrast enables effective binary thresholding.**

```python
  # Prepare a few small kernels for morphological filtering
  kern = np.zeros((3,3), dtype=np.uint8)
  kern1 = np.copy(kern)
  kern1[1,1:3]=1
  kern2 = np.copy(kern)
  kern2[1,0:2]=1
  kern3 = np.copy(kern)
  kern3[0:2,1]=1
  kern4 = np.copy(kern)
  kern4[1:3,1]=1

  # Prepare a larger kernel for dilation
  kern[1,0:3]=1
  kern[0:3,1]=1

  # Perform erosion with 4 small kernels
  device, e1_img = pcv.erode(tr_es_img, kern1, 1, device, args.debug)
  device, e2_img = pcv.erode(tr_es_img, kern2, 1, device, args.debug)
  device, e3_img = pcv.erode(tr_es_img, kern3, 1, device, args.debug)
  device, e4_img = pcv.erode(tr_es_img, kern4, 1, device, args.debug)

  # Combine eroded images
  device, c12_img = pcv.logical_or(e1_img, e2_img, device, args.debug)
  device, c123_img = pcv.logical_or(c12_img, e3_img, device, args.debug)
  device, c1234_img = pcv.logical_or(c123_img, e4_img, device, args.debug)
```

<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/13_er_image_itr_1_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/13_er_image_itr_1_t.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/14_er_image_itr_1_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/14_er_image_itr_1_t.png" height="200"></a> 

<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/15_er_image_itr_1_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/15_er_image_itr_1_t.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/16_er_image_itr_1_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/16_er_image_itr_1_t.png" height="200"></a> 

<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/19_or_joined_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/19_or_joined_t.png" height="200"></a> 

**Figure 6.** (Top Left) Erosion with kernel 1. (Top Right) Erosion with kernel 2. (Middle Left) Erosion with kernel 3. (Middle Right) Erosion with kernel 4. (Bottom) Logical join of all eroded images.

* **Erosion steps help eliminate background noise (pixels called plant that are isolated and are part of background).**
* **Erosion was performed with 4 different kernels. The focal pixel (one in the middle of the 3X3 grid) is retained if the correspodning other pixel in the kernel non zero.**
* **Logical join combines these individually eroded images keeping pixels within found within individual images, but also removing some of the object of interest pixels.**


##Merging results from both the background subtraction and derivative filter methods is better at capturing the object (plant) than either method alone.

```python
  # Bring the two object identification approaches together.
  # Using a logical OR combine object identified by background subtraction and the object identified by derivative filter.
  device, comb_img = pcv.logical_or(c1234_img, bkg_sub_thres_img, device, args.debug)

  # Get masked image, Essentially identify pixels corresponding to plant and keep those.
  device, masked_erd = pcv.apply_mask(img, comb_img, 'black', device, args.debug)
```

<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/bkgrd_sub_thres_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/bkgrd_sub_thres_t.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/19_or_joined_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/19_or_joined_t.png" height="200"></a>

<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/20_or_joined_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/20_or_joined_t.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/21_bmasked_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/21_bmasked_t.png" height="200"></a>

**Figure 7.** (Top Left) Binary image obtained from background subtraction method. (Top Right) Binary image obtained from derivative filter method. (Bottom Left) Logical join between binary images. (Bottom Right) Original image masked with binary derived from the logical join of both methods.

* **The background subtract method does a good job of identifying most of the plant but not so good where leaves meet stem**
* **The derivative filter method does a good job of identifying edges of the plant but not so good identifying interior of leaves**
* **Combining these methods improves our ability to capture more plant and less background.**

```python
  # Need to remove the edges of the image, we did that by generating a set of rectangles to mask the edges
  # img is (254 X 320)
  # mask for the bottom of the image
  device, box1_img, rect_contour1, hierarchy1 = pcv.rectangle_mask(img, (120,184), (215,252), device, args.debug)
  # mask for the left side of the image
  device, box2_img, rect_contour2, hierarchy2 = pcv.rectangle_mask(img, (1,1), (85,252), device, args.debug)
  # mask for the right side of the image
  device, box3_img, rect_contour3, hierarchy3 = pcv.rectangle_mask(img, (240,1), (318,252), device, args.debug)
  # mask the edges
  device, box4_img, rect_contour4, hierarchy4 = pcv.border_mask(img, (1,1), (318,252), device, args.debug)
```

<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/22_roi_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/22_roi_t.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/23_roi_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/23_roi_t.png" height="200"></a>

<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/24_roi_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/24_roi_t.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/25_brd_mskd_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/25_brd_mskd_t.png" height="200"></a>

**Figure 8.** (Top Left) Make a mask to hide the pot. (Top Right) Make a mask to hide left panel. (Bottom Left) Make a mask to hide right panel. (Bottom Right) Make a mask to hide the very edge of the image.

* **Making image masks is a very useful method to ignore/remove objects in your image that are difficult to remove through thresholding.**
* **Note that the top left corner has coordinate values (1,1) and these coordinate values increase as you move right and down (row, column).**

```python
  # combine boxes to filter the edges and car out of the photo
  device, bx12_img = pcv.logical_or(box1_img, box2_img, device, args.debug)
  device, bx123_img = pcv.logical_or(bx12_img, box3_img, device, args.debug)
  device, bx1234_img = pcv.logical_or(bx123_img, box4_img, device, args.debug)

  # invert this mask and then apply it the masked image.
  device, inv_bx1234_img = pcv.invert(bx1234_img, device, args.debug)
  device, edge_masked_img = pcv.apply_mask(masked_erd, inv_bx1234_img, 'black', device, args.debug)
```

<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/29_invert_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/29_invert_t.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/30_bmasked_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/30_bmasked_t.png" height="200"></a>

**Figure 9.** (Left) Combined background masks after inversion. (Right) Masked image from above after masking with background mask.

* **Note the plant is almost entirely isolate from the background.**

```python
  # assign the coordinates of an area of interest (rectangle around the area you expect the plant to be in)
  device, roi_img, roi_contour, roi_hierarchy = pcv.rectangle_mask(img, (120,75), (200,184), device, args.debug)

  # get the coordinates of the plant from the masked object
  plant_objects, plant_hierarchy = cv2.findContours(edge_masked_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

  # Obtain the coordinates of the plant object which are partially within the area of interest
  device, roi_objects, hierarchy5, kept_mask, obj_area = pcv.roi_objects(img, 'partial', roi_contour, roi_hierarchy, plant_objects, plant_hierarchy, device, args.debug)

  # Apply the box mask to the image to ensure no background
  device, masked_img = pcv.apply_mask(kept_mask, inv_bx1234_img, 'black', device, args.debug)
```


<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/31_roi_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/31_roi_t.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/32_obj_on_img_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/32_obj_on_img_t.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/33_bmasked_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/33_bmasked_t.png" height="200"></a>

**Figure 10.** (Left) Select an area where you expect the plant to be. (Middle) Plant falls within area. (Right) Include all continuous portions within the plant that fall within the area of interest (rectangle).

* **This step helps to remove any other areas of background that were not removed during any other filtering steps.**

```python
  device, masked_img = pcv.apply_mask(kept_mask, inv_bx1234_img, 'black', device, args.debug)
  rgb = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
  # Generate a binary to send to the analysis function
  device, mask = pcv.binary_threshold(masked_img, 1, 255, 'light', device, args.debug)
  mask3d = np.copy(mask)
  plant_objects_2, plant_hierarchy_2 = cv2.findContours(mask3d,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
  device, o, m = pcv.object_composition(rgb, roi_objects, hierarchy5, device, args.debug)

  # Get final masked image
  device, masked_img = pcv.apply_mask(kept_mask, inv_bx1234_img, 'black', device, args.debug)
  # Obtain a 3 dimensional representation of this grayscale image (for pseudocoloring)
  rgb = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)

  # Generate a binary to send to the analysis function
  device, mask = pcv.binary_threshold(masked_img, 1, 255, 'light', device, args.debug)

  # Make a copy of this mask for pseudocoloring
  mask3d = np.copy(mask)

  # Extract coordinates of plant for pseudocoloring of plant
  plant_objects_2, plant_hierarchy_2 = cv2.findContours(mask3d,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
  device, o, m = pcv.object_composition(rgb, roi_objects, hierarchy5, device, args.debug)
```
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/35_objcomp_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/35_objcomp_t.png" height="200"></a>  

**Figure 11.** This is an outline of the contours of the captured plant drawn onto the original image.

* **Now that the plant has been sepearted from the background we can analyze the pixel composition and shape of the plant.**
* **In order to pseudocolor the plant by signal intensity the image needs to be converted from grayscale (1-dimension) to pseudocolor (3-dimension). This is done by replicating the grayscale image 3X and combining them into a single 3-dimensional matrix (rgb = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)).**
* **All masks, countours, etc... need to be converted to 3-dimensions for pseudocoloring.**


##Now we can perform the analysis of pixelwise signal value and object shape attributes.

```python
  ### Analysis ###
  # Perform signal analysis
  device, hist_header, hist_data, h_norm = pcv.analyze_NIR_intensity(img, args.image, mask, 256, device, args.debug, args.outdir + '/' + img_name)
  # Perform shape analysis
  device, shape_header, shape_data, ori_img = pcv.analyze_object(rgb, args.image, o, m, device, args.debug, args.outdir + '/' + img_name)

  # Print the results to STDOUT
  pcv.print_results(args.image, hist_header, hist_data)
  pcv.print_results(args.image, shape_header, shape_data)

# Call program
if __name__ == '__main__':
  main()
```
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/NIR_SV_270_z2500_347831_nir_pseudo_col_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/NIR_SV_270_z2500_347831_nir_pseudo_col_t.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/NIR_SV_270_z2500_347831_shapes_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/NIR_SV_270_z2500_347831_shapes_t.png" height="200"></a>
<a href="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/NIR_SV_270_z2500_347831_nir_hist_t.png" target="_blank">
<img src="{{site.baseurl}}/img/documentation_images/tutorial-nir-pipeline/NIR_SV_270_z2500_347831_nir_hist_t.png" height="200"></a>

**Figure 12.** (Left) A image of the object pseudocolored by signal intensity (darker green is more black, yellow is more white). (Middle) Shape attributes of the plant printed on the original image. (Right) Histogram of the signal intensity values.

* **Values are printed to STDOUT.**
* **Notice how part of one leaf isn't captured. What would you change the pipeline to fix this? Improving these pipelines is an on going project for our community.**



##To deploy a pipeline over a full image set please see tutorial on Pipeline Parallelization [here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/pipeline_parallel.html).