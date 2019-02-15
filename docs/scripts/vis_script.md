In the terminal:

```
./pipelinename.py -i testimg.png -o ./output-images -r results.txt -w -D 'print'
```
*  Always test pipelines (preferably with -D flag set to 'print') before running over a full image set

Python script: 

```python
# !/usr/bin/python
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
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("-r", "--result", help="result file.", required=False)
    parser.add_argument("-w", "--writeimg", help="write out images.", default=False, action="store_true")
    parser.add_argument("-D", "--debug",
                        help="can be set to 'print' or None (or 'plot' if in jupyter) prints intermediate images.",
                        default=None)
    args = parser.parse_args()
    return args

#### Start of the Main/Customizable portion of the pipeline.

### Main pipeline
def main():
    # Get options
    args = options()

    pcv.params.debug = args.debug  # set debug mode
    pcv.params.debug_outdir = args.outdir  # set output directory

    # Read image
    img, path, filename = pcv.readimage(args.image)

    # Convert RGB to HSV and extract the saturation channel
    s = pcv.rgb2gray_hsv(img, 's')

    # Threshold the saturation image
    s_thresh = pcv.threshold.binary(s, 85, 255, 'light')

    # Median Blur
    s_mblur = pcv.median_blur(s_thresh, 5)
    s_cnt = pcv.median_blur(s_thresh, 5)

    # Convert RGB to LAB and extract the Blue channel
    b = pcv.rgb2gray_lab(img, 'b')

    # Threshold the blue image
    b_thresh = pcv.threshold.binary(b, 160, 255, 'light')
    b_cnt = pcv.threshold.binary(b, 160, 255, 'light')

    # Fill small objects
    # b_fill = pcv.fill(b_thresh, 10)

    # Join the thresholded saturation and blue-yellow images
    bs = pcv.logical_or(s_mblur, b_cnt)

    # Apply Mask (for VIS images, mask_color=white)
    masked = pcv.apply_mask(img, bs, 'white')

    # Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
    masked_a = pcv.rgb2gray_lab(masked, 'a')
    masked_b = pcv.rgb2gray_lab(masked, 'b')

    # Threshold the green-magenta and blue images
    maskeda_thresh = pcv.threshold.binary(masked_a, 115, 255, 'dark')
    maskeda_thresh1 = pcv.threshold.binary(masked_a, 135, 255, 'light')
    maskedb_thresh = pcv.threshold.binary(masked_b, 128, 255, 'light')

    # Join the thresholded saturation and blue-yellow images (OR)
    ab1 = pcv.logical_or(maskeda_thresh, maskedb_thresh)
    ab = pcv.logical_or(maskeda_thresh1, ab1)

    # Fill small objects
    ab_fill = pcv.fill(ab, 200)

    # Apply mask (for VIS images, mask_color=white)
    masked2 = pcv.apply_mask(masked, ab_fill, 'white')

    # Identify objects
    id_objects, obj_hierarchy = pcv.find_objects(masked2, ab_fill)

    # Define ROI
    roi1, roi_hierarchy= pcv.roi.rectangle(x=100, y=100, h=200, w=200, img=masked2)

    # Decide which objects to keep
    roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img, 'partial', roi1, roi_hierarchy, id_objects, obj_hierarchy)

    # Object combine kept objects
    obj, mask = pcv.object_composition(img, roi_objects, hierarchy3)

    ############### Analysis ################

    outfile=False
    if args.writeimg == True:
        outfile = args.outdir + "/" + filename

    # Find shape properties, output shape image (optional)
    shape_header, shape_data, shape_imgs = pcv.analyze_object(img, obj, mask)

    # Shape properties relative to user boundary line (optional)
    boundary_header, boundary_data, boundary_img1 = pcv.analyze_bound_horizontal(img, obj, mask, 1680)

    # Determine color properties: Histograms, Color Slices, output color analyzed histogram (optional)
    color_header, color_data, color_histogram = pcv.analyze_color(img, kept_mask, 256, 'all')

    # Pseudocolor the grayscale image
    pseudocolored_img = pcv.pseudocolor(gray_img=s, mask=kept_mask, cmap='jet')

    # Write shape and color data to results file
    pcv.print_results(filename=args.result)

if __name__ == '__main__':
    main()
```