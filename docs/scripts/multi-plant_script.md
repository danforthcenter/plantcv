In the terminal:

```
./pipelinename.py -i multi-plant-img.png -o ./output-images -n names.txt -D 'print'
```

*  Always test pipelines (preferably with -D flag set to 'print') before running over a full image set

Python script: 

```python
#!/usr/bin/python

import sys, traceback
import cv2
import os
import re
import numpy as np
import argparse
import string
from plantcv import plantcv as pcv

### Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=True)
    parser.add_argument("-n", "--names", help="path to txt file with names of genotypes to split images into", required =False)
    parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", action=None)
    args = parser.parse_args()
    return args

### Main pipeline
def main():
    # Get options
    args = options()
    
    # Read image
    img, path, filename = pcv.readimage(args.image)
    
    pcv.params.debug=args.debug #set debug mode
 
    # STEP 1: Check if this is a night image, for some of these dataset's images were captured
    # at night, even if nothing is visible. To make sure that images are not taken at
    # night we check that the image isn't mostly dark (0=black, 255=white).
    # if it is a night image it throws a fatal error and stops the pipeline.
    
    if np.average(img) < 50:
        pcv.fatal_error("Night Image")
    else:
        pass
        
    # STEP 2: Normalize the white color so you can later
    # compare color between images.
    # Inputs:
    #   img = image object, RGB colorspace
    #   roi = region for white reference, if none uses the whole image,
    #         otherwise (x position, y position, box width, box height)
    
    # white balance image based on white toughspot
    
    img1 = pcv.white_balance(img,roi=(400,800,200,200))
    
    # STEP 3: Rotate the image
    
    rotate_img = pcv.rotate(img1, -1)
    
    # STEP 4: Shift image. This step is important for clustering later on.
    # For this image it also allows you to push the green raspberry pi camera
    # out of the image. This step might not be necessary for all images.
    # The resulting image is the same size as the original.
    # Inputs:
    #   img    = image object
    #   number = integer, number of pixels to move image
    #   side   = direction to move from "top", "bottom", "right","left"
    
    shift1 = pcv.shift_img(img1, 300, 'top')
    img1 = shift1
    
    # STEP 5: Convert image from RGB colorspace to LAB colorspace
    # Keep only the green-magenta channel (grayscale)
    # Inputs:
    #    img     = image object, RGB colorspace
    #    channel = color subchannel ('l' = lightness, 'a' = green-magenta , 'b' = blue-yellow)
    
    a = pcv.rgb2gray_lab(img1, 'a')
    
    # STEP 6: Set a binary threshold on the saturation channel image
    # Inputs:
    #    img         = img object, grayscale
    #    threshold   = threshold value (0-255)
    #    maxValue    = value to apply above threshold (usually 255 = white)
    #    object_type = light or dark
    #       - If object is light then standard thresholding is done
    #       - If object is dark then inverse thresholding is done
    
    img_binary = pcv.threshold.binary(a, 120, 255, 'dark')
    #                                     ^
    #                                     |
    #                                 adjust this value
    
    # STEP 7: Fill in small objects (speckles)
    # Inputs:
    #    img  = image object, grayscale. img will be returned after filling
    #    size = minimum object area size in pixels (integer)
    
    fill_image = pcv.fill(img_binary, 100)
    #                                  ^
    #                                  |
    #                         adjust this value
    
    # STEP 8: Dilate so that you don't lose leaves (just in case)
    # Inputs:
    #    img    = input image
    #    kernel = integer
    #    i      = iterations, i.e. number of consecutive filtering passes
    
    dilated = pcv.dilate(fill_image, 1, 1)
    
    # STEP 9: Find objects (contours: black-white boundaries)
    # Inputs:
    #    img  = image that the objects will be overlayed
    #    mask = what is used for object detection
    
    id_objects, obj_hierarchy = pcv.find_objects(img1, dilated)
    
    # STEP 10: Define region of interest (ROI)
    # Inputs:
    #    x_adj     = adjust center along x axis
    #    y_adj     = adjust center along y axis
    #    w_adj     = adjust width
    #    h_adj     = adjust height
    #    img       = img to overlay roi
    # roi_contour, roi_hierarchy = pcv.roi.rectangle(10, 500, -10, -100, img1)
    #                                                ^                ^
    #                                                |________________|
    #                                            adjust these four values
    
    roi_contour, roi_hierarchy = pcv.roi.rectangle(10, 500, -10, -100, img1)
    
    # STEP 11: Keep objects that overlap with the ROI
    # Inputs:
    #    img            = img to display kept objects
    #    roi_type       = 'cutto' or 'partial' (for partially inside)
    #    roi_contour    = contour of roi, output from "View and Ajust ROI" function
    #    roi_hierarchy  = contour of roi, output from "View and Ajust ROI" function
    #    object_contour = contours of objects, output from "Identifying Objects" fuction
    #    obj_hierarchy  = hierarchy of objects, output from "Identifying Objects" fuction
    
    roi_objects, roi_obj_hierarchy, kept_mask, obj_area = pcv.roi_objects(img1, 'partial', roi_contour, roi_hierarchy,
                                                                          id_objects, obj_hierarchy)
    
    # STEP 12: This function take a image with multiple contours and
    # clusters them based on user input of rows and columns
    
    # Inputs:
    #    img               = An RGB image
    #    roi_objects       = object contours in an image that are needed to be clustered.
    #    roi_obj_hierarchy = object hierarchy
    #    nrow              = number of rows to cluster (this should be the approximate  number of desired rows in the entire image even if there isn't a literal row of plants)
    #    ncol              = number of columns to cluster (this should be the approximate number of desired columns in the entire image even if there isn't a literal row of plants)
    
    clusters_i, contours, hierarchies = pcv.cluster_contours(img1, roi_objects, roi_obj_hierarchy, 4, 6)
    
    # STEP 13: This function takes clustered contours and splits them into multiple images,
    # also does a check to make sure that the number of inputted filenames matches the number
    # of clustered contours. If no filenames are given then the objects are just numbered
    # Inputs:
    #    img                     = ideally a masked RGB image.
    #    grouped_contour_indexes = output of cluster_contours, indexes of clusters of contours
    #    contours                = contours to cluster, output of cluster_contours
    #    hierarchy               = object hierarchy
    #    outdir                  = directory for output images
    #    file                    = the name of the input image to use as a base name , output of filename from read_image function
    #    filenames               = input txt file with list of filenames in order from top to bottom left to right (likely list of genotypes)
    
    # Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
    pcv.params.debug = "print"
    
    out = args.outdir
    names = args.names
    
    output_path = pcv.cluster_contour_splitimg(img1, clusters_i, contours, hierarchies, out, file=filename, filenames=names)
    
# Call program
if __name__ == '__main__':
    main()
``` 
