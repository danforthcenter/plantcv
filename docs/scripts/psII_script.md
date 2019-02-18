In the terminal:

```
./pipelinename.py -i /home/user/images/testimg.png -o /home/user/output-images -D 'print'
```

* Always test pipelines (preferably with -D flag for debug mode) before running over a full image set.

Python script:

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

    # Mask pesky track autofluor
    track1 = pcv.rgb2gray_hsv(track, 'v')
    track_thresh = pcv.threshold.binary(track1, 0, 255, 'light')
    track_inv = pcv.invert(track_thresh)
    track_masked = pcv.apply_mask(mask1, track_inv, 'black')

    # Threshold the image
    fmax_thresh = pcv.threshold.binary(track_masked, 20, 255, 'light')

    # Median Filter
    s_mblur = pcv.median_blur(fmax_thresh, 5)
    s_cnt = pcv.median_blur(fmax_thresh, 5)

    # Fill small objects
    s_fill = pcv.fill(s_mblur, 110)
    sfill_cnt = pcv.fill(s_mblur, 110)

    # Identify objects
    id_objects,obj_hierarchy = pcv.find_objects(mask, sfill_cnt)

    # Define ROI
    roi1, roi_hierarchy = pcv.roi.rectangle(x=100, y=100, h=200, w=200, img=mask)

    # Decide which objects to keep
    roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(mask, 'partial', roi1, roi_hierarchy, id_objects, obj_hierarchy)

    # Object combine kept objects
    obj, masked = pcv.object_composition(mask, roi_objects, hierarchy3)

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
    pcv.print_results(filename=args.result)
  
if __name__ == '__main__':
    main()
```
