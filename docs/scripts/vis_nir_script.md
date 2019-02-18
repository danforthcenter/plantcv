In the terminal:

```
./pipelinename.py -i testimg.png -o ./output-images -r results.txt -w -D 'print'
```

*  Always test pipelines (preferably with -D flag set to 'print') before running over a full image set

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
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("-r","--result", help="result file.", required= False )
    parser.add_argument("-r2","--coresult", help="result file.", required= False )
    parser.add_argument("-w","--writeimg", help="write out images.", default=False)
    parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", default=None)
    args = parser.parse_args()
    return args

### Main pipeline
def main():
    # Get options
    args = options()
    
    pcv.params.debug=args.debug #set debug mode
    pcv.params.debug_outdir=args.outdir #set output directory
    
    # Read image
    img, path, filename = pcv.readimage(args.image)

    # Convert RGB to HSV and extract the saturation channel
    s = pcv.rgb2gray_hsv(img, 's')

    # Threshold the Saturation image
    s_thresh = pcv.threshold.binary(s, 30, 255, 'light')

    # Median Blur
    s_mblur = pcv.median_blur(s_thresh, 5)
    s_cnt = pcv.median_blur(s_thresh, 5)

    # Convert RGB to LAB and extract the blue channel
    b = pcv.rgb2gray_lab(img, 'b')
    
    # Threshold the blue image
    b_thresh = pcv.threshold.binary(b, 129, 255, 'light')
    b_cnt = pcv.threshold.binary(b, 19, 255, 'light')

    # Join the thresholded saturation and blue-yellow images
    bs = pcv.logical_and(s_mblur, b_cnt)

    # Apply Mask (for VIS images, mask_color=white)
    masked = pcv.apply_mask(img, bs, 'white')

    # Identify objects
    id_objects,obj_hierarchy = pcv.find_objects(masked, bs)

    # Define ROI
    roi1, roi_hierarchy= pcv.roi.rectangle(600,450,-600,-700, img)

    # Decide which objects to keep
    roi_objects, hierarchy, kept_mask, obj_area = pcv.roi_objects(img,'partial',roi1,roi_hierarchy,id_objects,obj_hierarchy)
    
    # Object combine kept objects
    obj, mask = pcv.object_composition(img, roi_objects, hierarchy)

############### Analysis ################  
  
    # Find shape properties, output shape image (optional)
    shape_header, shape_data, shape_img = pcv.analyze_object(img, obj, mask)
    
    # Shape properties relative to user boundary line (optional)
    boundary_header, boundary_data, boundary_img1 = pcv.analyze_bound_horizontal(img, obj, mask, 1680)
    
    # Determine color properties: Histograms, Color Slices, output color analyzed histogram (optional)
    color_header, color_data, color_histogram = pcv.analyze_color(img, kept_mask, 256, 'all')

    # Pseudocolor the grayscale image
    pseudocolored_img = pcv.pseudocolor(gray_img=s, mask=kept_mask, cmap='jet')

    # Write shape and color data to results file
    pcv.print_results(filename=args.result)
    
    # Will will print out results again, so clear the outputs before running NIR analysis 
    pcv.outputs.clear()
    
    if args.coresult is not None:
        nirpath = pcv.get_nir(path,filename)
        nir, path1, filename1 = pcv.readimage(nirpath)
        nir2 = cv2.imread(nirpath,0)

    nmask = pcv.resize(mask, 0.28,0.28)

    newmask = pcv.crop_position_mask(nir,nmask,40,3,"top","right")

    nir_objects, nir_hierarchy = pcv.find_objects(nir, newmask)

    #combine objects
    nir_combined, nir_combinedmask = pcv.object_composition(nir, nir_objects, nir_hierarchy)

    nhist_header, nhist_data, nir_imgs = pcv.analyze_nir_intensity(nir2, nir_combinedmask, 256)
    nshape_header, nshape_data, nir_hist = pcv.analyze_object(nir2, nir_combined, nir_combinedmask)

    # Plot out the image with shape data
    shape_image = nir_imgs[0]
    pcv.plot_image(shape_image)

    pcv.print_results(filename=args.coresult)
    
if __name__ == '__main__':
  main()
```
