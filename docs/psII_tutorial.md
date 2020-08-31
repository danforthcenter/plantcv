## Tutorial: PSII Image Workflow

PlantCV is composed of modular functions that can be arranged (or rearranged) and adjusted quickly and easily.
Workflows do not need to be linear (and often are not). Please see workflow example below for more details.
A global variable "debug" allows the user to print out the resulting image.
The debug has three modes: either None, 'plot', or 'print'. If set to
'print' then the function prints the image out, or if using a [Jupyter](jupyter.md) notebook you could set debug to 'plot' to have
the images plot to the screen.
This allows users to visualize and optimize each step on individual test images and small test sets before workflows are deployed over whole datasets.

PSII images (3 in a set; F0, Fmin, and Fmax) are captured directly following a saturating fluorescence pulse 
(red light; 630 nm). These three PSII images can be used to calculate Fv/Fm (efficiency of photosystem II) 
for each pixel of the plant. Unfortunately, our PSII imaging cabinet has a design flaw when capturing images 
of plants with vertical architecture. You can read more about how we validated this flaw using our PSII 
analysis workflows in the [PlantCV Paper](http://dx.doi.org/10.1016/j.molp.2015.06.005). 
However, the workflows to analyze PSII images are functional and a sample workflow is outlined below.  

Also see [here](#psii-script) for the complete script. 

### Workflow
 
1.  Optimize workflow on individual image with debug set to 'print' (or 'plot' if using a Jupyter notebook).
2.  Run workflow on small test set (ideally that spans time and/or treatments).  
3.  Re-optimize workflows on 'problem images' after manual inspection of test set.  
4.  Deploy optimized workflow over test set using parallelization script.

### Running A Workflow

To run a PSII workflow over a single PSII image set (3 images) there are 4 required inputs:

1.  **Image 1:** F0 (a.k.a Fdark/null) image.
2.  **Image 2:** Fmin image.
3.  **Image 3:** Fmax image. 
5.  **Output directory:** If debug mode is set to 'print' output images from each step are produced.

This tutorial showcases an example workflow for fluorescence images taken with the [CropReporter system](https://www.phenovation.com/cropreporter/). 
CropReporter images are stored in .DAT files where multiple frames, depending on the measurement protocol, are stored into a single file. Users with different data formats can still 
analyze fluorescence images by reading in individual images for each. Image sets that don't have an `fdark` frame can create a null image of the same size with `np.zeros`. 

Optional Inputs:

*  **Debug Flag:** Prints or plots (if in Jupyter or have x11 forwarding on) an image at each step 

Sample command to run a workflow on a single PSII image set:  

* Always test workflows (preferably with -D flag for debug mode) before running over a full image set.

```
./workflowname.py -i /home/user/images/PSII_PSD_testimg_22_rep6.DAT.DAT -o /home/user/output-images -D 'print'

```

### Walk Through A Sample Workflow

Workflows start by importing necessary packages, and by defining user inputs.

```python
#!/usr/bin/python
import sys, traceback
import cv2
import numpy as np
import argparse
import string
from plantcv import plantcv as pcv

### Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=True)
    parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", action="store_true")
    args = parser.parse_args()
    return args
    
```

All required frames are contained within a single `.DAT` file. See the documentation page for [`plantcv.photosynthesis.read_dat()`](photosynthesis_read_dat.md) to see more detail on
how this type of data is read in.

```python
### Main workflow
def main():
    # Get options
    args = options()
    
    pcv.params.debug = args.debug #set debug mode
    pcv.params.debug_outdir = args.outdir #set output directory
    
    # Read fluorescence image data 
    fdark1, fmin1, fmax1 = pcv.photosynthesis.read_dat(args.image)
    
```

**Figure 1.** `Fdark` frame 

![Screenshot](img/tutorial_images/psII/fdark.jpg)

**Figure 2.** `Fmin` frame 

![Screenshot](img/tutorial_images/psII/fmin.jpg)

**Figure 3.** `Fmax` frame. This will be used to create a plant mask that will isolate the plant material in the image. 

![Screenshot](img/tutorial_images/psII/fmax_rescaled_sideways.jpg)

```python
    # Rotate each frame so that plant is upright 
    
    # Inputs:
    #   img             - Image data 
    #   rotation_deg    - Rotation angle in degrees, can be a negative number, positive values move counter clockwise
    #   crop            - If crop is set to True, image will be cropped to original image dimensions. If set to False, the image size will be adjusted to accommodate new image dimensions.
    fdark = pcv.rotate(img=fdark1, rotation_deg=-90, crop=False)
    fmin = pcv.rotate(img=fmin1, rotation_deg=-90, crop=False)
    fmax = pcv.rotate(img=fmax1, rotation_deg=-90, crop=False)
    
    
```

**Figure 4.** Rotated `fmax` frame  

![Screenshot](img/tutorial_images/psII/fmax_rescaled.jpg)

The resulting image is then thresholded with a [binary threshold](binary_threshold.md) to capture the plant material. In most cases, it is expected that pixel values 
range between 0 and 255, but our example image has pixel values from 0 to over 7000. Trial and error a common method for selecting an appropriate threshold value. 

```python
    # Threshold the `fmax` image
    
    # Inputs:
    #   gray_img        - Grayscale image data 
    #   threshold       - Threshold value (usually between 0-255)
    #   max_value       - Value to apply above threshold (255 = white) 
    #   object_type     - 'light' (default) or 'dark'. If the object is lighter than the 
    #                       background then standard threshold is done. If the object is 
    #                       darker than the background then inverse thresholding is done. 
    plant_mask = pcv.threshold.binary(gray_img=fmax, threshold=855, max_value=255, object_type="light")
   
```

**Figure 3.** Binary threshold on masked Fmax image.

![Screenshot](img/tutorial_images/psII/plant_mask.jpg)

###############################################################################################################################################################################################
###############################################################################################################################################################################################

###############################################################################################################################################################################################
###############################################################################################################################################################################################

###############################################################################################################################################################################################
###############################################################################################################################################################################################
Noise is reduced with the [median blur](median_blur.md) function.

```python
    # Median Filter
    
    # Inputs:
    #   gray_img - Grayscale image data 
    #   ksize - Kernel size. Integer or tuple; (ksize, ksize) box if integer is input, 
    #           (n, m) size box if tuple is given.
    s_mblur = pcv.median_blur(gray_img=fmax_thresh, ksize=5)
    s_cnt = pcv.median_blur(gray_img=fmax_thresh, ksize=5)
    
```

**Figure 4.** Median blur applied.

![Screenshot](img/tutorial_images/psII/04_median_blur5.jpg)

Noise is also reduced with the [fill](fill.md) function.

```python
    # Fill small objects
    
    # Inputs:
    #   bin_img - Binary image data 
    #   size - Minimum object area size in pixels (integer), smaller objects get filled in. 
    s_fill = pcv.fill(bin_img=s_mblur, size=110)
    sfill_cnt = pcv.fill(bin_img=s_mblur, size=110)
    
```

**Figure 5.** Fill applied.  

![Screenshot](img/tutorial_images/psII/05_fill110.jpg)

Objects (OpenCV refers to them a contours) are then identified within the image using 
the [find objects](find_objects.md) function.

```python
    # Identify objects
    
    # Inputs:
    #   img - RGB or grayscale image data for plotting
    #   mask - Binary mask used for detecting contours
    id_objects,obj_hierarchy = pcv.find_objects(img=mask, mask=sfill_cnt)
    
```

**Figure 6.** All objects found within the image are identified.

![Screenshot](img/tutorial_images/psII/id_obj.jpg)

Next the region of interest is defined using the [rectangular region of interest](roi_rectangle.md) function.

```python
    # Define ROI
    
    # Inputs: 
    #   img - RGB or grayscale image to plot the ROI on 
    #   x - The x-coordinate of the upper left corner of the rectangle 
    #   y - The y-coordinate of the upper left corner of the rectangle 
    #   h - The height of the rectangle 
    #   w - The width of the rectangle 
    roi1, roi_hierarchy = pcv.roi.rectangle(img=mask, x=100, y=100, h=200, w=200)
    
```

**Figure 7.** Region of interest is drawn on the image.

![Screenshot](img/tutorial_images/psII/07_roi.jpg)

The objects within and overlapping are kept with the [region of interest objects](roi_objects.md) function.
Alternately the objects can be cut to the region of interest.

```python
    # Decide which objects to keep
    
    # Inputs:
    #    img            = img to display kept objects
    #    roi_contour    = contour of roi, output from any ROI function
    #    roi_hierarchy  = contour of roi, output from any ROI function
    #    object_contour = contours of objects, output from pcv.find_objects function
    #    obj_hierarchy  = hierarchy of objects, output from pcv.find_objects function
    #    roi_type       = 'partial' (default, for partially inside), 'cutto', or 
    #    'largest' (keep only largest contour)
    roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=mask, roi_contour=roi1, 
                                                               roi_hierarchy=roi_hierarchy, 
                                                               object_contour=id_objects, 
                                                               obj_hierarchy=obj_hierarchy, 
                                                               roi_type='partial')
    
```

**Figure 8.** Objects in the region of interest are identified (green).  

![Screenshot](img/tutorial_images/psII/08_obj_on_img.jpg)

The isolated objects now should all be plant material. There can be more than one object that makes up a plant,
since sometimes leaves twist making them appear in images as separate objects. Therefore, in order for shape 
analysis to perform properly the plant objects need to be combined into one object using the [combine objects](object_composition.md) function.

```python
    # Object combine kept objects
    
    # Inputs:
    #   img - RGB or grayscale image data for plotting 
    #   contours - Contour list 
    #   hierarchy - Contour hierarchy array 
    obj, masked = pcv.object_composition(img=mask, contours=roi_objects, hierarchy=hierarchy3)
    
```

**Figure 9.** Combined plant object outlined in blue.

![Screenshot](img/tutorial_images/psII/09_objcomp.jpg)

The next step is to analyze the plant object for traits such as [shape](analyze_shape.md), or [PSII signal](fluor_fvfm.md).

For the PSII signal function the 16-bit F0, Fmin, and  Fmax images are read in so that they can be used 
along with the generated mask to calculate Fv/Fm.

```python
################ Analysis ################  
    
    outfile = False
    if args.writeimg == True:
        outfile = os.path.join(args.outdir, filename)
    
    # Find shape properties, output shape image (optional)
    
    # Inputs:
    #   img - RGB or grayscale image data 
    #   obj- Single or grouped contour object
    #   mask - Binary image mask to use as mask for moments analysis 
    shape_img = pcv.analyze_object(img=mask, obj=obj, mask=masked)
    
    # Fluorescence Measurement (read in 16-bit images)
    fdark, darkpath, darkname = pcv.readimage(args.fdark)
    fmin, minpath, minname = pcv.readimage(args.fmin)
    fmax, maxpath, maxname = pcv.readimage(args.fmax)
    
    
    # Inputs:
    #   fdark - Grayscale image 
    #   fmin - Grayscale image 
    #   fmax - Grayscale image 
    #   mask - Binary mask of selected contours 
    #   bins - Number of grayscale bins (0-256 for 8-bit img, 0-65536 for 16-bit). Default bins = 256
    fvfm_images = pcv.fluor_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=kept_mask, bins=256)

    # Store the two images
    fv_img = fvfm_images[0]
    fvfm_hist = fvfm_images[1]

    # Pseudocolor the Fv/Fm grayscale image that is calculated inside the fluor_fvfm function
    
    # Inputs:
    #     gray_img - Grayscale image data
    #     obj - Single or grouped contour object (optional), if provided the pseudocolored image gets cropped down to the region of interest.
    #     mask - Binary mask (optional) 
    #     background - Background color/type. Options are "image" (gray_img), "white", or "black". A mask must be supplied.
    #     cmap - Colormap (https://matplotlib.org/tutorials/colors/colormaps.html)
    #     min_value - Minimum value for range of interest
    #     max_value - Maximum value for range of interest
    #     dpi - Dots per inch for image if printed out (optional, if dpi=None then the default is set to 100 dpi).
    #     axes - If False then the title, x-axis, and y-axis won't be displayed (default axes=True).
    #     colorbar - If False then the colorbar won't be displayed (default colorbar=True)
    pseudocolored_img = pcv.visualize.pseudocolor(gray_img=fv_img, mask=kept_mask, cmap='jet')

    # Write shape and nir data to results file
    pcv.print_results(filename=args.result)
  
if __name__ == '__main__':
    main()
    
```

**Figure 10.** Input images from top to bottom: F0 (null image also known as Fdark); Fmin image; Fmax image.

![Screenshot](img/tutorial_images/psII/Fdark.jpg)

![Screenshot](img/tutorial_images/psII/Fmin.jpg)

![Screenshot](img/tutorial_images/psII/Fmax.jpg)

**Figure 11.** (Top) Image pseudocolored by Fv/Fm values. (Bottom) Histogram of raw Fv/Fm values.

![Screenshot](img/tutorial_images/psII/10_pseudo_fvfm.jpg)

![Screenshot](img/tutorial_images/psII/11_fvfm_hist.jpg)

To deploy a workflow over a full image set please see tutorial on [workflow parallelization](pipeline_parallel.md).

## PSII Script

In the terminal:

```
./workflowname.py -i /home/user/images/testimg.png -o /home/user/output-images -D 'print'

```

* Always test workflows (preferably with -D flag for debug mode) before running over a full image set.

Python script:

```python
#!/usr/bin/env python
import cv2
import argparse
from plantcv import plantcv as pcv

### Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i1", "--fdark", help="Input image file.", required=True)
    parser.add_argument("-i2", "--fmin", help="Input image file.", required=True)
    parser.add_argument("-i3", "--fmax", help="Input image file.", required=True)
    parser.add_argument("-m", "--track", help="Input region of interest file.", required=False)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=True)
    parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", action="store_true")
    args = parser.parse_args()
    return args

### Main workflow
def main():
    # Get options
    args = options()
    
    pcv.params.debug = args.debug #set debug mode
    pcv.params.debug_outdir = args.outdir #set output directory
    
    # Read image (converting fmax and track to 8 bit just to create a mask, use 16-bit for all the math)
    mask, path, filename = pcv.readimage(args.fmax)
    track, trackpath, trackname = pcv.readimage(args.track)
    
    # Mask pesky track autofluor
    track1 = pcv.rgb2gray_hsv(rgb_img=track, channel='v')
    track_thresh = pcv.threshold.binary(gray_img=track1, threshold=0, max_value=255, object_type='light')
    track_inv = pcv.invert(gray_img=track_thresh)
    track_masked = pcv.apply_mask(img=mask, mask=track_inv, mask_color='black')

    # Threshold the image
    fmax_thresh = pcv.threshold.binary(gray_img=track_masked, threshold=20, max_value=255, 
                                   object_type='light')

    # Median Filter
    s_mblur = pcv.median_blur(gray_img=fmax_thresh, ksize=5)
    s_cnt = pcv.median_blur(gray_img=fmax_thresh, ksize=5)

    # Fill small objects
    s_fill = pcv.fill(bin_img=s_mblur, size=110)
    sfill_cnt = pcv.fill(bin_img=s_mblur, size=110)

    # Identify objects
    id_objects,obj_hierarchy = pcv.find_objects(img=mask, mask=sfill_cnt)

    # Define ROI
    roi1, roi_hierarchy = pcv.roi.rectangle(img=mask, x=100, y=100, h=200, w=200)

    # Decide which objects to keep
    roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=mask, roi_contour=roi1, 
                                                               roi_hierarchy=roi_hierarchy, 
                                                               object_contour=id_objects, 
                                                               obj_hierarchy=obj_hierarchy, 
                                                               roi_type='partial')
    # Object combine kept objects
    obj, masked = pcv.object_composition(img=mask, contours=roi_objects, hierarchy=hierarchy3)
    
    ################ Analysis ################  
    
    outfile = False
    if args.writeimg == True:
        outfile = os.path.join(args.outdir, filename)
    
    # Find shape properties, output shape image (optional)
    shape_img = pcv.analyze_object(img=mask, obj=obj, mask=masked)
    
    # Fluorescence Measurement (read in 16-bit images)
    fdark, darkpath, darkname = pcv.readimage(args.fdark)
    fmin, minpath, minname = pcv.readimage(args.fmin)
    fmax, maxpath, maxname = pcv.readimage(args.fmax)
    
    fvfm_images = pcv.fluor_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=kept_mask, bins=256)

    # Store the two images
    fv_img = fvfm_images[0]
    fvfm_hist = fvfm_images[1]

    # Pseudocolor the Fv/Fm grayscale image that is calculated inside the fluor_fvfm function
    pseudocolored_img = pcv.visualize.pseudocolor(gray_img=fv_img, mask=kept_mask, cmap='jet')

    # Write shape and nir data to results file
    pcv.print_results(filename=args.result)
  
if __name__ == '__main__':
    main()
    
```
