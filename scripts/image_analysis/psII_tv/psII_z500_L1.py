#!/usr/bin/env python
import sys, traceback
import cv2
import numpy as np
import argparse
import string
import plantcv as pcv

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
  
  # Read image (converting fmax and track to 8 bit just to create a mask, use 16-bit for all the math)
  mask, path, filename = pcv.readimage(args.fmax)
  #mask = cv2.imread(args.fmax)
  track = cv2.imread(args.track)
  
  mask1, mask2, mask3= cv2.split(mask)
  
  # Pipeline step
  device = 0
  
  # Mask pesky track autofluor
  device, track1= pcv.rgb2gray_hsv(track, 'v', device, args.debug)
  device, track_thresh = pcv.binary_threshold(track1, 0, 255, 'light', device, args.debug)
  device, track_inv=pcv.invert(track_thresh, device, args.debug)
  device, track_masked = pcv.apply_mask(mask1, track_inv, 'black', device, args.debug)
  
  # Threshold the Saturation image
  device, fmax_thresh = pcv.binary_threshold(track_masked, 20, 255, 'light', device, args.debug)
  
  # Median Filter
  device, s_mblur = pcv.median_blur(fmax_thresh, 5, device, args.debug)
  device, s_cnt = pcv.median_blur(fmax_thresh, 5, device, args.debug)
  
  # Fill small objects
  device, s_fill = pcv.fill(s_mblur, s_cnt, 110, device, args.debug)
  device, sfill_cnt = pcv.fill(s_mblur, s_cnt, 110, device, args.debug)
  
  # Identify objects
  device, id_objects,obj_hierarchy = pcv.find_objects(mask, sfill_cnt, device, args.debug)
  
  # Define ROI
  device, roi1, roi_hierarchy= pcv.define_roi(mask,'circle', device, None, 'default', args.debug,True, 0,0,-50,-50)
  
  # Decide which objects to keep
  device,roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(mask,'partial',roi1,roi_hierarchy,id_objects,obj_hierarchy,device, args.debug)
  
  # Object combine kept objects
  device, obj, masked = pcv.object_composition(mask, roi_objects, hierarchy3, device, args.debug)
  
################ Analysis ################  
  
  # Find shape properties, output shape image (optional)
  device, shape_header,shape_data,shape_img = pcv.analyze_object(mask, args.fmax, obj, masked, device,args.debug, args.outdir+'/'+filename)
  
  # Fluorescence Measurement (read in 16-bit images)
  fdark=cv2.imread(args.fdark, -1)
  fmin=cv2.imread(args.fmin, -1)
  fmax=cv2.imread(args.fmax, -1)
  
  device, fvfm_header, fvfm_data=pcv.fluor_fvfm(fdark,fmin,fmax,kept_mask, device, args.outdir+'/'+filename, 1000, args.debug)

  # Output shape and color data
  pcv.print_results(args.fmax, shape_header, shape_data)
  pcv.print_results(args.fmax, fvfm_header, fvfm_data)
  
if __name__ == '__main__':
  main()
