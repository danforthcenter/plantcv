#!/usr/bin/env python

# This is a computational pipeline which uses the plantcv module to sharpen, filter and analyze NIR images
# Pipeline designed for use with Setaria plants at zoom X3500
# The strategy/methodology is adopted from the textbook "Digital Image Processing" by Gonzalez and Woods
# Version 0.9 Max Feldman 7.29.14

import argparse
import scipy
from scipy import ndimage
import sys, os, traceback
import cv2
import numpy as np
from random import randrange
import pygtk
import matplotlib
if not os.getenv('DISPLAY'):
  matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import cm as cm
from Bio.Statistics.lowess import lowess
import plantcv as pcv

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
    if args.debug:
      print("Analyzing your image dude...")
    
    # Read image
    device = 0
    img = cv2.imread(args.image, flags=0)
    path, img_name = os.path.split(args.image)
    # Read in image which is average of average of backgrounds
    img_bkgrd = cv2.imread("bkgrd_ave_z3500.png", flags=0)

    # NIR images for burnin2 are up-side down. This may be fixed in later experiments
    img =  ndimage.rotate(img, 180)
    img_bkgrd =  ndimage.rotate(img_bkgrd, 180)

    # Subtract the image from the image background to make the plant more prominent
    device, bkg_sub_img = pcv.image_subtract(img, img_bkgrd, device, args.debug)
    if args.debug:
        pcv.plot_hist(bkg_sub_img, 'bkg_sub_img')
    device, bkg_sub_thres_img = pcv.binary_threshold(bkg_sub_img, 145, 255, 'dark', device, args.debug)
    bkg_sub_thres_img = cv2.inRange(bkg_sub_img, 30, 220)
    if args.debug:
        cv2.imwrite('bkgrd_sub_thres.png', bkg_sub_thres_img)

    #device, bkg_sub_thres_img = pcv.binary_threshold_2_sided(img_bkgrd, 50, 190, device, args.debug)

    # if a region of interest is specified read it in
    roi = cv2.imread(args.roi)

    # Start by examining the distribution of pixel intensity values
    if args.debug:
      pcv.plot_hist(img, 'hist_img')
      
    # Will intensity transformation enhance your ability to isolate object of interest by thesholding?
    device, he_img = pcv.HistEqualization(img, device, args.debug)
    if args.debug:
      pcv.plot_hist(he_img, 'hist_img_he')
    
    # Laplace filtering (identify edges based on 2nd derivative)
    device, lp_img = pcv.laplace_filter(img, 1, 1, device, args.debug)
    if args.debug:
      pcv.plot_hist(lp_img, 'hist_lp')
    
    # Lapacian image sharpening, this step will enhance the darkness of the edges detected
    device, lp_shrp_img = pcv.image_subtract(img, lp_img, device, args.debug)
    if args.debug:
      pcv.plot_hist(lp_shrp_img, 'hist_lp_shrp')
      
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
    
    # Perform dilation
    # device, dil_img = pcv.dilate(c1234_img, kern, 1, device, args.debug)
    device, comb_img = pcv.logical_or(c1234_img, bkg_sub_thres_img, device, args.debug)
    
    # Get masked image
    # The dilated image may contain some pixels which are not plant
    device, masked_erd = pcv.apply_mask(img, comb_img, 'black', device, args.debug)
    # device, masked_erd_dil = pcv.apply_mask(img, dil_img, 'black', device, args.debug)
    
    # Need to remove the edges of the image, we did that by generating a set of rectangles to mask the edges
    # img is (254 X 320)

    # mask for the bottom of the image
    device, box1_img, rect_contour1, hierarchy1 = pcv.rectangle_mask(img, (100,210), (230,252), device, args.debug)
    # mask for the left side of the image
    device, box2_img, rect_contour2, hierarchy2 = pcv.rectangle_mask(img, (1,1), (85,252), device, args.debug)
    # mask for the right side of the image
    device, box3_img, rect_contour3, hierarchy3 = pcv.rectangle_mask(img, (240,1), (318,252), device, args.debug)
    # mask the edges
    device, box4_img, rect_contour4, hierarchy4 = pcv.border_mask(img, (1,1), (318,252), device, args.debug)
    
    # combine boxes to filter the edges and car out of the photo
    device, bx12_img = pcv.logical_or(box1_img, box2_img, device, args.debug)
    device, bx123_img = pcv.logical_or(bx12_img, box3_img, device, args.debug)
    device, bx1234_img = pcv.logical_or(bx123_img, box4_img, device, args.debug)
    device, inv_bx1234_img = pcv.invert(bx1234_img, device, args.debug)
    

    # Make a ROI around the plant, include connected objects
    # Apply the box mask to the image
    # device, masked_img = pcv.apply_mask(masked_erd_dil, inv_bx1234_img, 'black', device, args.debug)
    device, edge_masked_img = pcv.apply_mask(masked_erd, inv_bx1234_img, 'black', device, args.debug)
    device, roi_img, roi_contour, roi_hierarchy = pcv.rectangle_mask(img, (100,75), (220,208), device, args.debug)
    plant_objects, plant_hierarchy = cv2.findContours(edge_masked_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    
    device, roi_objects, hierarchy5, kept_mask, obj_area = pcv.roi_objects(img, 'partial', roi_contour, roi_hierarchy, plant_objects, plant_hierarchy, device, args.debug)
    
      
    # Apply the box mask to the image
    # device, masked_img = pcv.apply_mask(masked_erd_dil, inv_bx1234_img, 'black', device, args.debug)
    device, masked_img = pcv.apply_mask(kept_mask, inv_bx1234_img, 'black', device, args.debug)
    rgb = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)

    # Generate a binary to send to the analysis function
    device, mask = pcv.binary_threshold(masked_img, 1, 255, 'light', device, args.debug)
    mask3d = np.copy(mask)
    plant_objects_2, plant_hierarchy_2 = cv2.findContours(mask3d,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    device, o, m = pcv.object_composition(rgb, roi_objects, hierarchy5, device, args.debug)
    
    ### Analysis ###
    device, hist_header, hist_data, h_norm = pcv.analyze_NIR_intensity(img, args.image, mask, 256, device, args.debug, args.outdir + '/' + img_name)
    device, shape_header, shape_data, ori_img = pcv.analyze_object(rgb, args.image, o, m, device, args.debug, args.outdir + '/' + img_name)
    
    pcv.print_results(args.image, hist_header, hist_data)
    pcv.print_results(args.image, shape_header, shape_data)
    
if __name__ == '__main__':
    main()
