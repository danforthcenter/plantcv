## Tutorial: PSII Image Pipeline

PlantCV is composed of modular functions that can be arranged (or rearranged) and adjusted quickly and easily.
Pipelines do not need to be linear (and often are not). Please see pipeline example below for more details.
A global variable "debug" allows the user to print out the resulting image.
The debug has three modes: either None, 'plot', or 'print'. If set to
'print' then the function prints the image out, or if using a [Jupyter](jupyter.md) notebook you could set debug to 'plot' to have
the images plot to the screen.
This allows users to visualize and optimize each step on individual test images and small test sets before pipelines are deployed over whole datasets.

PSII images (3 in a set; F0, Fmin, and Fmax) are captured directly following a saturating fluorescence pulse 
(red light; 630 nm). These three PSII images can be used to calculate Fv/Fm (efficiency of photosystem II) 
for each pixel of the plant. Unfortunately, our PSII imaging cabinet has a design flaw when capturing images 
of plants with vertical architecture. You can read more about how we validated this flaw using our PSII 
analysis pipelines in the [PlantCV Paper](http://dx.doi.org/10.1016/j.molp.2015.06.005). 
However, the pipelines to analyze PSII images are functional and a sample pipeline is outlined below.  

### Workflow
 
1.  Optimize pipeline on individual image with debug set to 'print' (or 'plot' if using a Jupyter notebook).
2.  Run pipeline on small test set (ideally that spans time and/or treatments).  
3.  Re-optimize pipelines on 'problem images' after manual inspection of test set.  
4.  Deploy optimized pipeline over test set using parallelization script.

### Running A Pipeline

To run a PSII pipeline over a single PSII image set (3 images) there are 4 required inputs:

1.  **Image 1:** F0 (a.k.a Fdark/null) image.
2.  **Image 2:** Fmin image.
3.  **Image 3:** Fmax image. 
5.  **Output directory:** If debug mode is set to 'print' output images from each step are produced,
otherwise ~4 final output images are produced.

Optional Inputs:

*  **Debug Flag:** Prints or plots (if in Jupyter or have x11 forwarding on) an image at each step
*  **Region of Interest:** The user can input their own binary region of interest or image mask 
(for PSII images we use a premade mask to remove the screws from the image). 
Make sure the input is the same size as your image or you will have problems.  

Sample command to run a pipeline on a single PSII image set:  

* Always test pipelines (preferably with -D flag for debug mode) before running over a full image set.

```
./pipelinename.py -i /home/user/images/testimg.png -o /home/user/output-images -D 'print'
```

### Walk Through A Sample Pipeline

Pipelines start by importing necessary packages, and by defining user inputs.

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
    parser.add_argument("-i1", "--fdark", help="Input image file.", required=True)
    parser.add_argument("-i2", "--fmin", help="Input image file.", required=True)
    parser.add_argument("-i3", "--fmax", help="Input image file.", required=True)
    parser.add_argument("-m", "--track", help="Input region of interest file.", required=False)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=True)
    parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", action="store_true")
    args = parser.parse_args()
    return args
```

The PSII pipeline first uses the Fmax image to create an image mask. Our PSII images are 16-bit grayscale, 
but we will initially [read](read_image.md) the Fmax image in as a 8-bit color image just to create the image mask.

```python
### Main pipeline
def main():
    # Get options
    args = options()
    
    pcv.params.debug=args.debug #set debug mode
    pcv.params.debug_outdir=args.outdir #set output directory
    
    # Read image (converting fmax and track to 8 bit just to create a mask, use 16-bit for all the math)
    mask, path, filename = pcv.readimage(args.fmax)
    #mask = cv2.imread(args.fmax)
    track = cv2.imread(args.track)
    
    mask1, mask2, mask3 = cv2.split(mask)
```

**Figure 1.** (Top) Fmax image that will be used to create a plant mask that will isolate the plant material in the image. 
(Bottom) Premade image mask for the screws and metallic bits that are auto-fluorescent.

![Screenshot](img/tutorial_images/psII/Fmax.jpg)

![Screenshot](img/tutorial_images/psII/mask.jpg)

We use a premade-mask for the screws on the car that consistently give background signal, but this is not required.
The track mask is an RGB image so a single channel is selected using the [RGB to HSV](rgb2hsv.md)
function and converted to a binary mask with a [binary threshold](binary_threshold.md).
The mask is [inverted](invert.md) since the screws were white in the track image.
The [apply mask function](apply_mask.md) is then used to apply the track mask to one channel of the Fmax image (mask1). 

```python
    # Mask pesky track autofluor
    track1 = pcv.rgb2gray_hsv(track, 'v')
    track_thresh = pcv.threshold.binary(track1, 0, 255, 'light')
    track_inv = pcv.invert(track_thresh)
    track_masked = pcv.apply_mask(mask1, track_inv, 'black')
```

**Figure 2.** (Top) Inverted mask (white portion is kept as objects).
(Bottom) Fmax image (Figure 1) with the inverted mask applied.  

![Screenshot](img/tutorial_images/psII/01_invert.jpg)

![Screenshot](img/tutorial_images/psII/02_bmasked.jpg)

The resulting image is then thresholded with a [binary threshold](binary_threshold.md) to capture the plant material.

```python
    # Threshold the image
    fmax_thresh = pcv.threshold.binary(track_masked, 20, 255, 'light')
```

**Figure 3.** Binary threshold on masked Fmax image.

![Screenshot](img/tutorial_images/psII/03_binary_threshold20.jpg)

Noise is reduced with the [median blur](median_blur.md) function.

```python
  # Median Filter
  s_mblur = pcv.median_blur(fmax_thresh, 5)
  s_cnt = pcv.median_blur(fmax_thresh, 5)
```

**Figure 4.** Median blur applied.

![Screenshot](img/tutorial_images/psII/04_median_blur5.jpg)

Noise is also reduced with the [fill](fill.md) function.

```python
    # Fill small objects
    s_fill = pcv.fill(s_mblur, 110)
    sfill_cnt = pcv.fill(s_mblur, 110)
```

**Figure 5.** Fill applied.  

![Screenshot](img/tutorial_images/psII/05_fill110.jpg)

Objects (OpenCV refers to them a contours) are then identified within the image using 
the [find objects](find_objects.md) function.

```python
    # Identify objects
    id_objects,obj_hierarchy = pcv.find_objects(mask, sfill_cnt)
```

**Figure 6.** All objects found within the image are identified.

![Screenshot](img/tutorial_images/psII/06_id_objects.jpg)

Next the region of interest is defined using the [rectangular region of interest](roi_rectangle.md) function.

```python
    # Define ROI
    roi1, roi_hierarchy = pcv.roi.rectangle(x=100, y=100, h=200, w=200, img=mask)
```

**Figure 7.** Region of interest is drawn on the image.

![Screenshot](img/tutorial_images/psII/07_roi.jpg)

The objects within and overlapping are kept with the [region of interest objects](roi_objects.md) function.
Alternately the objects can be cut to the region of interest.

```python
    # Decide which objects to keep
    roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(mask, 'partial', roi1, roi_hierarchy, id_objects, obj_hierarchy)
```

**Figure 8.** Objects in the region of interest are identified (green).  

![Screenshot](img/tutorial_images/psII/08_obj_on_img.jpg)

The isolated objects now should all be plant material. There can be more than one object that makes up a plant,
since sometimes leaves twist making them appear in images as separate objects. Therefore, in order for shape 
analysis to perform properly the plant objects need to be combined into one object using the [combine objects](object_composition.md) function.

```python
    # Object combine kept objects
    obj, masked = pcv.object_composition(mask, roi_objects, hierarchy3)
```

**Figure 9.** Combined plant object outlined in blue.

![Screenshot](img/tutorial_images/psII/09_objcomp.jpg)

The next step is to analyze the plant object for traits such as [shape](analyze_shape.md), or [PSII signal](fluor_fvfm.md).

For the PSII signal function the 16-bit F0, Fmin, and  Fmax images are read in so that they can be used 
along with the generated mask to calculate Fv/Fm.

```python
################ Analysis ################  
    
    outfile=False
    if args.writeimg==True:
        outfile=args.outdir+"/"+filename
    
    # Find shape properties, output shape image (optional)
    shape_header, shape_data, shape_img = pcv.analyze_object(mask, obj, masked)
    
    # Fluorescence Measurement (read in 16-bit images)
    fdark = cv2.imread(args.fdark, -1)
    fmin = cv2.imread(args.fmin, -1)
    fmax = cv2.imread(args.fmax, -1)
    
    fvfm_header, fvfm_data, fvfm_images = pcv.fluor_fvfm(fdark,fmin,fmax,kept_mask)

    # Store the two images
    fv_img = fvfm_images[0]
    fvfm_hist = fvfm_images[1]

    # Pseudocolor the Fv/Fm grayscale image that is calculated inside the fluor_fvfm function
    pseudocolored_img = pcv.pseudocolor(gray_img=fv_img, mask=kept_mask, cmap='jet')

    # Write shape and nir data to results file
    result=open(args.result,"a")
    result.write('\t'.join(map(str,shape_header)))
    result.write("\n")
    result.write('\t'.join(map(str,shape_data)))
    result.write("\n")
    for row in shape_img:  
        result.write('\t'.join(map(str,row)))
        result.write("\n")
    result.write('\t'.join(map(str,fvfm_header)))
    result.write("\n")
    result.write('\t'.join(map(str,fvfm_data)))
    result.write("\n")
    result.close()
  
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

To deploy a pipeline over a full image set please see tutorial on [pipeline parallelization](pipeline_parallel.md).
