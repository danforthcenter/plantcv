## Tutorial: VIS Image Workflow

PlantCV is composed of modular functions that can be arranged (or rearranged) and adjusted quickly and easily.
Workflows do not need to be linear (and often are not). Please see workflow example below for more details.
A global variable "debug" allows the user to print out the resulting image. The debug has three modes: either None, 'plot', or 'print'.
If set to 'print' then the function prints the image out to a file, or if using a [Jupyter](jupyter.md) notebook you could set debug to 'plot' to have
the images plot to the screen. Debug mode allows users to visualize and optimize each step on individual test images and small test sets before workflows are deployed over whole datasets.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/vis_tutorial.ipynb) Check out our interactive VIS tutorial! 

Also see [here](#vis-script) for the complete script. 

**Workflow**

1.  Optimize workflow on individual image with debug set to 'print' (or 'plot' if using a Jupyter notebook).
2.  Run workflow on small test set (that ideally spans time and/or treatments).
3.  Re-optimize workflows on 'problem images' after manual inspection of test set.
4.  Deploy optimized workflow over test set using parallelization script.

**Running A Workflow**

To run a VIS workflow over a single VIS image there are two required inputs:

1.  **Image:** Images can be processed regardless of what type of VIS camera was used (high-throughput platform, digital camera, cell phone camera).
Image processing will work with adjustments if images are well lit and free of background that is similar in color to plant material.  
2.  **Output directory:** If debug mode is set to 'print' output images from each step are produced, otherwise ~4 final output images are produced.

**Optional inputs:**

*  **Result File:** File to print results to
*  **Write Image Flag:** Flag to write out images, otherwise no result images are printed (to save time).
*  **Debug Flag:** Prints an image at each step
*  **Region of Interest:** The user can input their own binary region of interest or image mask (make sure it is the same size as your image or you will have problems).

Sample command to run a workflow on a single image:  

*  Always test workflows (preferably with -D flag set to 'print') before running over a full image set

```
./workflowname.py -i testimg.png -o ./output-images -r results.txt -w -D 'print'

```

### Walk Through A Sample Workflow

#### Workflows start by importing necessary packages, and by defining user inputs.

```python

#!/usr/bin/env python
import os
import argparse
from plantcv import plantcv as pcv

### Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("-r","--result", help="result file.", required= False )
    parser.add_argument("-w","--writeimg", help="write out images.", default=False, action="store_true")
    parser.add_argument("-D", "--debug", help="can be set to 'print' or None (or 'plot' if in jupyter) prints intermediate images.", default=None)
    args = parser.parse_args()
    return args
    
```

#### Start of the Main/Customizable portion of the workflow.

The image input by the user is [read in](read_image.md).

```python

### Main workflow
def main():
    # Get options
    args = options()
    
    pcv.params.debug=args.debug #set debug mode
    pcv.params.debug_outdir=args.outdir #set output directory
    
    # Read image (readimage mode defaults to native but if image is RGBA then specify mode='rgb')
    # Inputs:
    #   filename - Image file to be read in 
    #   mode - Return mode of image; either 'native' (default), 'rgb', 'gray', 'envi', or 'csv'
    img, path, filename = pcv.readimage(filename=args.image, mode='rgb')
    
```

**Figure 1.** Original image.
This particular image was captured by a digital camera, just to show that PlantCV works on images not captured on a 
[high-throughput phenotyping system](http://www.danforthcenter.org/scientists-research/core-technologies/phenotyping) with idealized VIS image capture conditions.

![Screenshot](img/tutorial_images/vis/original_image.jpg)
  
In some workflows (especially ones captured with a high-throughput phenotyping systems, where background is predictable) we first threshold out background.
In this particular workflow we do some pre-masking of the background. The goal is to remove as much background as possible without losing any information from the plant.
In order to perform a binary threshold on an image you need to select one of the color channels H,S,V,L,A,B,R,G,B.
Here we convert the [RGB image to HSV](rgb2hsv.md) color space then extract the 's' or saturation channel, but any channel can be selected based on user need.
If some of the plant is missed or not visible then thresholded channels may be combined (a later step).

```python        
    # Convert RGB to HSV and extract the saturation channel
    
    # Inputs:
    #   rgb_image - RGB image data 
    #   channel - Split by 'h' (hue), 's' (saturation), or 'v' (value) channel
    s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')
    
```

**Figure 2.** Saturation channel from original RGB image converted to HSV color space.

![Screenshot](img/tutorial_images/vis/01_hsv_saturation.jpg)

Next, the saturation channel is thresholded.
The [threshold](binary_threshold.md) can be on either light or dark objects in the image.

Tip: This step is often one that needs to be adjusted depending on the lighting and configurations of your camera system.

```python
    # Threshold the saturation image
    
    # Inputs:
    #   gray_img - Grayscale image data 
    #   threshold- Threshold value (between 0-255)
    #   max_value - Value to apply above threshold (255 = white) 
    #   object_type - 'light' (default) or 'dark'. If the object is lighter than the 
    #                 background then standard threshold is done. If the object is 
    #                 darker than the background then inverse thresholding is done. 
    s_thresh = pcv.threshold.binary(gray_img=s, threshold=85, max_value=255, object_type='light')
    
```

**Figure 3.** Thresholded saturation channel image (Figure 2). Remaining objects are in white.

![Screenshot](img/tutorial_images/vis/02_binary_threshold85.jpg)

Again, depending on the lighting it will be possible to remove more/less background.
A [median blur](median_blur.md) can be used to remove noise.

Tip: Fill and median blur type steps should be used as sparingly as possible.
Depending on the plant type (esp. grasses with thin leaves that often twist) you can lose plant material with a blur that is too harsh.

```python
    # Median Blur
    # Inputs: 
    #   gray_img - Grayscale image data 
    #   ksize - Kernel size (integer or tuple), (ksize, ksize) box if integer input,
    #           (n, m) box if tuple input 
    s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
    s_cnt = pcv.median_blur(gray_img=s_thresh, ksize=5)
    
```

**Figure 4.** Thresholded saturation channel image with median blur.

![Screenshot](img/tutorial_images/vis/03_median_blur5.jpg)

Here is where the workflow branches.
The original image is converted from an [RGB image to LAB](rgb2lab.md) color space and we extract blue-yellow channel.
This image is again thresholded and there is an optional [fill](fill.md) step that wasn't needed in this workflow.

```python
    # Convert RGB to LAB and extract the Blue channel
    
    # Input:
    #   rgb_img - RGB image data 
    #   channel- Split by 'l' (lightness), 'a' (green-magenta), or 'b' (blue-yellow) channel
    b = pcv.rgb2gray_lab(rgb_img=img, channel='b')
    
    # Threshold the blue image
    b_thresh = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, 
                                    object_type='light')
    b_cnt = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, 
                                 object_type='light')
    
    # Fill small objects (optional)
    #b_fill = pcv.fill(b_thresh, 10)
    
```

**Figure 5.** (Top) Blue-yellow channel from LAB color space from original image. (Bottom) Thresholded blue-yellow channel image.

![Screenshot](img/tutorial_images/vis/05_lab_blue-yellow.jpg)

![Screenshot](img/tutorial_images/vis/06_binary_threshold160.jpg)

Join the binary images from Figure 4 and Figure 5 with the [logical or](logical_or.md) function.

```python
    # Join the thresholded saturation and blue-yellow images
    
    # Inputs: 
    #   bin_img1 - Binary image data to be compared to bin_img2
    #   bin_img2 - Binary image data to be compared to bin_img1
    bs = pcv.logical_or(bin_img1=s_mblur, bin_img2=b_cnt)
    
```

**Figure 6.** Joined binary images (Figure 4 and Figure 5).

![Screenshot](img/tutorial_images/vis/08_or_joined.jpg)

Next, apply the binary image (Figure 6) as an image [mask](apply_mask.md) over the original image.
The purpose of this mask is to exclude as much background with simple thresholding without leaving out plant material.

```python
    # Apply Mask (for VIS images, mask_color=white)
    
    # Inputs:
    #   img - RGB image data 
    #   mask - Binary mask image data 
    #   mask_color - 'white' or 'black' 
    masked = pcv.apply_mask(img=img, mask=bs, mask_color='white')
    
```

**Figure 7.** Masked image with background removed.

![Screenshot](img/tutorial_images/vis/09_wmasked.jpg)

Now we'll focus on capturing the plant in the masked image from Figure 7.
The masked green-magenta and blue-yellow channels are extracted.
Then the two channels are thresholded to capture different portions of the plant, and the three images are joined together.
The small objects are [filled](fill.md).
The resulting binary image is used to mask the masked image from Figure 7.

```python
    # Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
    masked_a = pcv.rgb2gray_lab(rgb_img=masked, channel='a')
    masked_b = pcv.rgb2gray_lab(rgb_img=masked, channel='b')
    
    # Threshold the green-magenta and blue images
    maskeda_thresh = pcv.threshold.binary(gray_img=masked_a, threshold=115, 
                                      max_value=255, object_type='dark')
    maskeda_thresh1 = pcv.threshold.binary(gray_img=masked_a, threshold=135, 
                                           max_value=255, object_type='light')
    maskedb_thresh = pcv.threshold.binary(gray_img=masked_b, threshold=128, 
                                          max_value=255, object_type='light')
    
    # Join the thresholded saturation and blue-yellow images (OR)
    ab1 = pcv.logical_or(bin_img1=maskeda_thresh, bin_img2=maskedb_thresh)
    ab = pcv.logical_or(bin_img1=maskeda_thresh1, bin_img2=ab1)
    
    # Fill small objects
    # Inputs: 
    #   bin_img - Binary image data 
    #   size - Minimum object area size in pixels (must be an integer), and smaller objects will be filled
    ab_fill = pcv.fill(bin_img=ab, size=200)
    
    # Apply mask (for VIS images, mask_color=white)
    masked2 = pcv.apply_mask(img=masked, mask=ab_fill, mask_color='white')
    
```

The sample image used had very green leaves, but often (especially with stress treatments) 
there are yellowing leaves, redish leaves, or regions of necrosis. The different thresholding
channels capture different regions of the plant, then are combined into a mask for the image 
that was previously masked (Figure 7).

**Figure 8.** RGB to LAB conversion. (Top) The green-magenta "a" channel image. (Bottom) The blue-yellow "b" channel image.

![Screenshot](img/tutorial_images/vis/10_lab_green-magenta.jpg)

![Screenshot](img/tutorial_images/vis/11_lab_blue-yellow.jpg)

**Figure 9.** Thresholded LAB channel images. (Top) "dark" threshold 115. (Middle) "light" threshold 135. (Bottom) "light" threshold 128.

![Screenshot](img/tutorial_images/vis/12_binary_threshold115_inv.jpg)

![Screenshot](img/tutorial_images/vis/13_binary_threshold135.jpg)

![Screenshot](img/tutorial_images/vis/14_binary_threshold128.jpg)

**Figure 9.** Combined thresholded images.

![Screenshot](img/tutorial_images/vis/15_or_joined.jpg)

![Screenshot](img/tutorial_images/vis/16_or_joined.jpg)

![Screenshot](img/tutorial_images/vis/17_or_joined.jpg)

 **Figure 10.** Fill in small objects. (Top) Image with objects < 200 px filled. (Bottom) Masked image.
 
![Screenshot](img/tutorial_images/vis/18_fill200.jpg)

![Screenshot](img/tutorial_images/vis/19_wmasked.jpg)

Now we need to [identify the objects](find_objects.md) (called contours in OpenCV) within the image.

```python
    # Identify objects
    id_objects, obj_hierarchy = pcv.find_objects(masked2, ab_fill)
    
```

**Figure 11.** Here the objects (purple) are identified from the image from Figure 10.
Even the spaces within an object are colored, but will have different hierarchy values.

![Screenshot](img/tutorial_images/vis/20_id_objects.jpg)

Next a [rectangular region of interest](roi_rectangle.md) is defined (this can be made on the fly).

```python
    # Define ROI
    
    # Inputs: 
    #   img - RGB or grayscale image to plot the ROI on 
    #   x - The x-coordinate of the upper left corner of the rectangle 
    #   y - The y-coordinate of the upper left corner of the rectangle 
    #   h - The height of the rectangle 
    #   w - The width of the rectangle 
    roi1, roi_hierarchy= pcv.roi.rectangle(img=masked2, x=100, y=100, h=200, w=200)
    
```

**Figure 12.** Region of interest drawn onto image. 

![Screenshot](img/tutorial_images/vis/21_roi.jpg)

Once the region of interest is defined you can decide to keep everything overlapping with the [region of interest](roi_objects.md)
or cut the objects to the shape of the region of interest.


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
    roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=img, roi_contour=roi1, 
                                                                   roi_hierarchy=roi_hierarchy, 
                                                                   object_contour=id_objects, 
                                                                   obj_hierarchy=obj_hierarchy,
                                                                   roi_type='partial')
    
```

**Figure 13.** Kept objects (green) drawn onto image.

![Screenshot](img/tutorial_images/vis/22_obj_on_img.jpg)

The isolated objects now should all be plant material. There can
be more than one object that makes up a plant since sometimes leaves twist
making them appear in images as separate objects. Therefore, in order for
shape analysis to perform properly the plant objects need to be combined into 
one object using the [combine objects](object_composition.md) function.

```python
    # Object combine kept objects
    # Inputs:
    #   img - RGB or grayscale image data for plotting 
    #   contours - Contour list 
    #   hierarchy - Contour hierarchy array 
    obj, mask = pcv.object_composition(img=img, contours=roi_objects, hierarchy=hierarchy3)
    
```

**Figure 14.** Outline (blue) of combined objects on the image. 

![Screenshot](img/tutorial_images/vis/23_objcomp.jpg)

The next step is to analyze the plant object for traits such as [horizontal height](analyze_bound_horizontal.md),
[shape](analyze_shape.md), or [color](analyze_color.md).

```python
    ############### Analysis ################
  
    outfile = False
    if args.writeimg == True:
        outfile = os.path.join(args.outdir, filename)
  
    # Find shape properties, output shape image (optional)
    
    # Inputs:
    #   img - RGB or grayscale image data 
    #   obj- Single or grouped contour object
    #   mask - Binary image mask to use as mask for moments analysis  
    #   label - Optional label parameter, modifies the variable name of observations recorded   
    shape_img = pcv.analyze_object(img=img, obj=obj, mask=mask, label="default")
    
    # Shape properties relative to user boundary line (optional)
    
    # Inputs:
    #   img - RGB or grayscale image data 
    #   obj - Single or grouped contour object 
    #   mask - Binary mask of selected contours 
    #   line_position - Position of boundary line (a value of 0 would draw a line 
    #                   through the bottom of the image)
    #   label - Optional label parameter, modifies the variable name of observations recorded  
    boundary_img1 = pcv.analyze_bound_horizontal(img=img, obj=obj, mask=mask, 
                                                   line_position=1680, label="default")
    
    # Determine color properties: Histograms, Color Slices, output color analyzed histogram (optional)
    
    # Inputs:
    #   rgb_img - RGB image data
    #   mask - Binary mask of selected contours 
    #   hist_plot_type - None (default), 'all', 'rgb', 'lab', or 'hsv'
    #                    This is the data to be printed to the SVG histogram file 
    #   label - Optional label parameter, modifies the variable name of observations recorded  
    color_histogram = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type='all', label="default")

    # Pseudocolor the grayscale image
    
    # Inputs:
    #     gray_img - Grayscale image data
    #     obj - Single or grouped contour object (optional), if provided the pseudocolored image gets 
    #           cropped down to the region of interest.
    #     mask - Binary mask (optional) 
    #     background - Background color/type. Options are "image" (gray_img, default), "white", or "black". A mask 
    #                  must be supplied.
    #     cmap - Colormap
    #     min_value - Minimum value for range of interest
    #     max_value - Maximum value for range of interest
    #     dpi - Dots per inch for image if printed out (optional, if dpi=None then the default is set to 100 dpi).
    #     axes - If False then the title, x-axis, and y-axis won't be displayed (default axes=True).
    #     colorbar - If False then the colorbar won't be displayed (default colorbar=True)
    pseudocolored_img = pcv.visualize.pseudocolor(gray_img=s, mask=mask, cmap='jet')

    # Write shape and color data to results file
    pcv.outputs.save_results(filename=args.result)
  
if __name__ == '__main__':
    main()
    
```

**Figure 15.** Shape analysis output image.

![Screenshot](img/tutorial_images/vis/24_shapes.jpg)

**Figure 16.** Boundary line output image.

![Screenshot](img/tutorial_images/vis/25_boundary.jpg)

**Figure 17.** Pseudocolored image (based on value channel).

![Screenshot](img/tutorial_images/vis/26_pseudo_on_img.jpg)

**Figure 18.** Histogram of color values for each plant pixel.

![Screenshot](img/tutorial_images/vis/27_all_hist.jpg)

### Additional examples

To demonstrate the importance of camera settings on workflow construction
here are different species of plants captured with the same imaging setup 
(digital camera) and processed with the same imaging workflow as above (no settings changed).

**Figure 19.** Output images from Cassava trait analysis. (From top to bottom) Original image, shape output image, boundary line output image, pseudocolored image (based on value channel), histogram of color values for each plant pixel.

![Screenshot](img/tutorial_images/vis/cassava_1_shapes.jpg)

![Screenshot](img/tutorial_images/vis/cassava_2_boundary.jpg)

![Screenshot](img/tutorial_images/vis/cassava_3_pseudo_on_img.jpg)

![Screenshot](img/tutorial_images/vis/cassava_4_all_hist.jpg)

**Figure 20.** Output images from Tomato trait analysis. (From top to bottom) Original image, shape output image, boundary line output image, pseudocolored image (based on value channel), histogram of color values for each plant pixel.

![Screenshot](img/tutorial_images/vis/tomato_1_shapes.jpg)

![Screenshot](img/tutorial_images/vis/tomato_1_shapes.jpg)

![Screenshot](img/tutorial_images/vis/tomato_2_boundary.jpg)

![Screenshot](img/tutorial_images/vis/tomato_3_pseudo_on_img.jpg)

![Screenshot](img/tutorial_images/vis/tomato_4_all_hist.jpg)



To deploy a workflow over a full image set please see tutorial on 
[workflow parallelization](pipeline_parallel.md).


## VIS Script
In the terminal:

```
./workflowname.py -i testimg.png -o ./output-images -r results.txt -w -D 'print'

```
*  Always test workflows (preferably with -D flag set to 'print') before running over a full image set

Python script: 

```python
#!/usr/bin/env python
import os
import argparse
from plantcv import plantcv as pcv


### Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("-r", "--result", help="result file.", required=False)
    parser.add_argument("-w", "--writeimg", help="write out images.", default=False, action="store_true")
    parser.add_argument("-D", "--debug",
                        help="can be set to 'print' or None (or 'plot' if in jupyter) prints intermediate images.",
                        default=None)
    args = parser.parse_args()
    return args

#### Start of the Main/Customizable portion of the workflow.

### Main workflow
def main():
    # Get options
    args = options()

    pcv.params.debug = args.debug  # set debug mode
    pcv.params.debug_outdir = args.outdir  # set output directory

    # Read image
    img, path, filename = pcv.readimage(filename=args.image)

    # Convert RGB to HSV and extract the saturation channel
    s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')

    # Threshold the saturation image
    s_thresh = pcv.threshold.binary(gray_img=s, threshold=85, max_value=255, object_type='light')

    # Median Blur
    s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
    s_cnt = pcv.median_blur(gray_img=s_thresh, ksize=5)

    # Convert RGB to LAB and extract the Blue channel
    b = pcv.rgb2gray_lab(rgb_img=img, channel='b')

    # Threshold the blue image
    b_thresh = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, object_type='light')
    b_cnt = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, object_type='light')

    # Fill small objects
    # b_fill = pcv.fill(b_thresh, 10)

    # Join the thresholded saturation and blue-yellow images
    bs = pcv.logical_or(bin_img1=s_mblur, bin_img2=b_cnt)

    # Apply Mask (for VIS images, mask_color=white)
    masked = pcv.apply_mask(img=img, mask=bs, mask_color='white')

    # Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
    masked_a = pcv.rgb2gray_lab(rgb_img=masked, channel='a')
    masked_b = pcv.rgb2gray_lab(rgb_img=masked, channel='b')

    # Threshold the green-magenta and blue images
    maskeda_thresh = pcv.threshold.binary(gray_img=masked_a, threshold=115, max_value=255, object_type='dark')
    maskeda_thresh1 = pcv.threshold.binary(gray_img=masked_a, threshold=135, max_value=255, object_type='light')
    maskedb_thresh = pcv.threshold.binary(gray_img=masked_b, threshold=128, max_value=255, object_type='light')

    # Join the thresholded saturation and blue-yellow images (OR)
    ab1 = pcv.logical_or(bin_img1=maskeda_thresh, bin_img2=maskedb_thresh)
    ab = pcv.logical_or(bin_img1=maskeda_thresh1, bin_img2=ab1)

    # Fill small objects
    ab_fill = pcv.fill(bin_img=ab, size=200)

    # Apply mask (for VIS images, mask_color=white)
    masked2 = pcv.apply_mask(img=masked, mask=ab_fill, mask_color='white')

    # Identify objects
    id_objects, obj_hierarchy = pcv.find_objects(img=masked2, mask=ab_fill)

    # Define ROI
    roi1, roi_hierarchy= pcv.roi.rectangle(img=masked2, x=100, y=100, h=200, w=200)

    # Decide which objects to keep
    roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=img, roi_contour=roi1, 
                                                               roi_hierarchy=roi_hierarchy, 
                                                               object_contour=id_objects, 
                                                               obj_hierarchy=obj_hierarchy,
                                                               roi_type='partial')

    # Object combine kept objects
    obj, mask = pcv.object_composition(img=img, contours=roi_objects, hierarchy=hierarchy3)

    ############### Analysis ################

    outfile = False
    if args.writeimg == True:
        outfile = os.path.join(args.outdir, filename)

    # Find shape properties, output shape image (optional)
    shape_imgs = pcv.analyze_object(img=img, obj=obj, mask=mask, label="default")

    # Shape properties relative to user boundary line (optional)
    boundary_img1 = pcv.analyze_bound_horizontal(img=img, obj=obj, mask=mask, line_position=1680, label="default")

    # Determine color properties: Histograms, Color Slices, output color analyzed histogram (optional)
    color_histogram = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type='all', label="default")

    # Pseudocolor the grayscale image
    pseudocolored_img = pcv.visualize.pseudocolor(gray_img=s, mask=mask, cmap='jet')

    # Write shape and color data to results file
    pcv.outputs.save_results(filename=args.result)

if __name__ == '__main__':
    main()
    
```
