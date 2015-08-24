#!/usr/bin/python
import sys, traceback
import cv2
import numpy as np
import argparse
import string
import plantcv as pcv

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Imaging processing with opencv")
  parser.add_argument("-i", "--image", help="Input image file.", required=True)
  parser.add_argument("-m", "--roi", help="Input region of interest file.", required=False)
  parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=True)
  parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", action="store_true")
  args = parser.parse_args()
  return args

### Main pipeline
def main():
   # Get options
  args = options()
  
  # Read image
  img, path, filename = pcv.readimage(args.image)
  #roi = cv2.imread(args.roi)
  
  # Pipeline step
  device = 0

  # Convert RGB to HSV and extract the Saturation channel
  device, s = pcv.rgb2gray_hsv(img, 's', device, args.debug)
  
  # Threshold the Saturation image
  device, s_thresh = pcv.binary_threshold(s, 36, 255, 'light', device, args.debug)
  
  # Median Filter
  device, s_mblur = pcv.median_blur(s_thresh, 0, device, args.debug)
  device, s_cnt = pcv.median_blur(s_thresh, 0, device, args.debug)
  
  # Fill small objects
  #device, s_fill = pcv.fill(s_mblur, s_cnt, 0, device, args.debug)
  
  # Convert RGB to LAB and extract the Blue channel
  device, b = pcv.rgb2gray_lab(img, 'b', device, args.debug)
  
  # Threshold the blue image
  device, b_thresh = pcv.binary_threshold(b, 137, 255, 'light', device, args.debug)
  device, b_cnt = pcv.binary_threshold(b, 137, 255, 'light', device, args.debug)
  
  # Fill small objects
  #device, b_fill = pcv.fill(b_thresh, b_cnt, 150, device, args.debug)
  
  # Join the thresholded saturation and blue-yellow images
  device, bs = pcv.logical_and(s_mblur, b_cnt, device, args.debug)
  
  # Apply Mask (for vis images, mask_color=white)
  device, masked = pcv.apply_mask(img, bs, 'white', device, args.debug)
  
  # Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
  device, masked_a = pcv.rgb2gray_lab(masked, 'a', device, args.debug)
  device, masked_b = pcv.rgb2gray_lab(masked, 'b', device, args.debug)
  
  # Threshold the green-magenta and blue images
  device, maskeda_thresh = pcv.binary_threshold(masked_a, 127, 255, 'dark', device, args.debug)
  device, maskedb_thresh = pcv.binary_threshold(masked_b, 128, 255, 'light', device, args.debug)
  
  # Join the thresholded saturation and blue-yellow images (OR)
  device, ab = pcv.logical_or(maskeda_thresh, maskedb_thresh, device, args.debug)
  device, ab_cnt = pcv.logical_or(maskeda_thresh, maskedb_thresh, device, args.debug)
  
  # Fill small noise
  device, ab_fill1 = pcv.fill(ab, ab_cnt, 2, device, args.debug)
  
  # Dilate to join small objects with larger ones
  device, ab_cnt1=pcv.dilate(ab_fill1, 3, 2, device, args.debug)
  device, ab_cnt2=pcv.dilate(ab_fill1, 3, 2, device, args.debug)

  # Fill dilated image mask
  device, ab_cnt3=pcv.fill(ab_cnt2,ab_cnt1,150,device,args.debug)
  device, masked2 = pcv.apply_mask(masked, ab_cnt3, 'white', device, args.debug)
  
  # Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
  device, masked2_a = pcv.rgb2gray_lab(masked2, 'a', device, args.debug)
  device, masked2_b = pcv.rgb2gray_lab(masked2, 'b', device, args.debug)
  
  # Threshold the green-magenta and blue images
  device, masked2a_thresh = pcv.binary_threshold(masked2_a, 127, 255, 'dark', device, args.debug)
  device, masked2b_thresh = pcv.binary_threshold(masked2_b, 128, 255, 'light', device, args.debug)
  device, ab_fill = pcv.logical_or(masked2a_thresh, masked2b_thresh, device, args.debug)
  
  # Identify objects
  device, id_objects,obj_hierarchy = pcv.find_objects(masked2, ab_fill, device, args.debug)

  # Define ROI
  device, roi1, roi_hierarchy= pcv.define_roi(masked2,'rectangle', device, None, 'default', args.debug,True, 525, 0,-490,-150)
  
  # Decide which objects to keep
  device,roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img,'partial',roi1,roi_hierarchy,id_objects,obj_hierarchy,device, args.debug)
  
  # Object combine kept objects
  device, obj, mask = pcv.object_composition(img, roi_objects, hierarchy3, device, args.debug)
  
############## Analysis ################  
  
  # Find shape properties, output shape image (optional)
  device, shape_header,shape_data,shape_img = pcv.analyze_object(img, args.image, obj, mask, device,args.debug,args.outdir+'/'+filename)
   
  # Shape properties relative to user boundary line (optional)
  device, boundary_header,boundary_data, boundary_img1= pcv.analyze_bound(img, args.image,obj, mask, 295, device,args.debug,args.outdir+'/'+filename)
  
  # Determine color properties: Histograms, Color Slices and Pseudocolored Images, output color analyzed images (optional)
  device, color_header,color_data,color_img= pcv.analyze_color(img, args.image, mask, 256, device, args.debug,None,'v','img',300,args.outdir+'/'+filename)
  
  # Output shape and color data
  pcv.print_results(args.image, shape_header, shape_data)
  pcv.print_results(args.image, color_header, color_data)
  pcv.print_results(args.image, boundary_header, boundary_data)
  
if __name__ == '__main__':
  main()#!/usr/bin/env python

