In the terminal:

```
./pipelinename.py -i /home/user/images/testimg.png -o /home/user/output-images -D 'print'
```

*  Always test pipelines (preferably with -D flag set to 'print') before running over a full image set

Python script: 

```python
#!/usr/bin/python
import os
import sys, traceback
import cv2
import numpy as np
import argparse
import string
from plantcv import plantcv as pcv

def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-m", "--roi", help="Input region of interest file.", required=False)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", action="store_true")
    args = parser.parse_args()
    return args

### Main pipeline
def main():
    # Get options
    args = options()
    
    pcv.params.debug=args.debug #set debug mode
    pcv.params.debug_outdir=args.outdir #set output directory
    
    # Read image (Note: flags=0 indicates to expect a grayscale image)
    img = cv2.imread(args.image, flags=0)
    
    # Get directory path and image name from command line arguments
    path, img_name = os.path.split(args.image)
    
    # Read in image which is the pixelwise average of background images
    img_bkgrd = cv2.imread("background_nir_z2500.png", flags=0)

    # Subtract the background image from the image with the plant.
    bkg_sub_img = pcv.image_subtract(img, img_bkgrd)
        
    # Threshold the image of interest using the two-sided cv2.inRange function (keep what is between 50-190)
    bkg_sub_thres_img = cv2.inRange(bkg_sub_img, 50, 190)
    if args.debug: #since we are using an OpenCV function we need to make it print
        pcv.print_image(bkg_sub_thres_img,'bkgrd_sub_thres.png')
    
    # Laplace filtering (identify edges based on 2nd derivative)
    lp_img = pcv.laplace_filter(img, 1, 1)
    if args.debug:
            pcv.plot_hist(lp_img, 'hist_lp')
    
    # Lapacian image sharpening, this step will enhance the darkness of the edges detected
    lp_shrp_img = pcv.image_subtract(img, lp_img)
    if args.debug:
            pcv.plot_hist(lp_shrp_img, 'hist_lp_sharp')
    
    # Sobel filtering
    # 1st derivative sobel filtering along horizontal axis, kernel = 1)
    sbx_img = pcv.sobel_filter(img, 1, 0, 1)
    
    # 1st derivative sobel filtering along vertical axis, kernel = 1)
    sby_img = pcv.sobel_filter(img, 0, 1, 1)
    
    # Combine the effects of both x and y filters through matrix addition
    # This will capture edges identified within each plane and emphasize edges found in both images
    sb_img = pcv.image_add(sbx_img, sby_img)
    
    # Use a lowpass (blurring) filter to smooth sobel image
    mblur_img = pcv.median_blur(sb_img, 1)
    mblur_invert_img = pcv.invert(mblur_img)
    
    # combine the smoothed sobel image with the laplacian sharpened image
    # combines the best features of both methods as described in "Digital Image Processing" by Gonzalez and Woods pg. 169
    edge_shrp_img = pcv.image_add(mblur_invert_img, lp_shrp_img)
    
    # Perform thresholding to generate a binary image
    tr_es_img = pcv.threshold.binary(edge_shrp_img, 145, 255, 'dark')
    
    # Do erosion with a 3x3 kernel
    e1_img = pcv.erode(tr_es_img, 3, 1)
    
    # Bring the two object identification approaches together.
    # Using a logical OR combine object identified by background subtraction and the object identified by derivative filter.
    comb_img = pcv.logical_or(e1_img, bkg_sub_thres_img)
    
    # Get masked image, Essentially identify pixels corresponding to plant and keep those.
    masked_erd = pcv.apply_mask(img, comb_img, 'black')
    
    # Need to remove the edges of the image, we did that by generating a set of rectangles to mask the edges
    # img is (254 X 320)
    # mask for the bottom of the image
    masked1, box1_img, rect_contour1, hierarchy1 = pcv.rectangle_mask(img, (120,184), (215,252))
    # mask for the left side of the image
    masked2, box2_img, rect_contour2, hierarchy2 = pcv.rectangle_mask(img, (1,1), (85,252))
    # mask for the right side of the image
    masked3, box3_img, rect_contour3, hierarchy3 = pcv.rectangle_mask(img, (240,1), (318,252))
    # mask the edges
    masked4, box4_img, rect_contour4, hierarchy4 = pcv.rectangle_mask(img, (1,1), (318,252))
    
    # combine boxes to filter the edges and car out of the photo
    bx12_img = pcv.logical_or(box1_img, box2_img)
    bx123_img = pcv.logical_or(bx12_img, box3_img)
    bx1234_img = pcv.logical_or(bx123_img, box4_img)
    
    # invert this mask and then apply it the masked image.
    inv_bx1234_img = pcv.invert(bx1234_img)
    edge_masked_img = pcv.apply_mask(masked_erd, inv_bx1234_img, 'black')
    
    # Identify objects
    id_objects,obj_hierarchy = pcv.find_objects(edge_masked_img, inv_bx1234_img)
    
    # Define ROI
    roi1, roi_hierarchy= pcv.roi.rectangle(x=100, y=100, h=200, w=200, img=edge_masked_img)
    
    # Decide which objects to keep
    roi_objects, hierarchy5, kept_mask, obj_area = pcv.roi_objects(edge_masked_img, 'partial', roi1, roi_hierarchy, id_objects, obj_hierarchy)
    
    rgb_img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    o, m = pcv.object_composition(rgb_img, roi_objects, hierarchy5)
    
    ### Analysis ###
    
    outfile=False
    if args.writeimg==True:
        outfile=args.outdir+"/"+img_name
    
    # Perform signal analysis
    nir_header, nir_data, nir_hist = pcv.analyze_nir_intensity(img, kept_mask, 256)
    
    # Pseudocolor the grayscale image to a colormap
    pseudocolored_img = pcv.pseudocolor(gray_img=img, mask=kept_mask, cmap='viridis')
    
    # Perform shape analysis
    shape_header, shape_data, shape_imgs = pcv.analyze_object(rgb_img, o, m)
    
    # Write shape and nir data to results file
    pcv.print_results(filename=args.result)
    
# Call program
if __name__ == '__main__':
    main()
```
