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
  device, s_mblur = pcv.median_blur(s_thresh, 5, device, args.debug)
  device, s_cnt = pcv.median_blur(s_thresh, 5, device, args.debug)
  
  # Fill small objects
  device, s_fill = pcv.fill(s_mblur, s_cnt, 0, device, args.debug)
  
  # Convert RGB to LAB and extract the Blue channel
  device, b = pcv.rgb2gray_lab(img, 'b', device, args.debug)
  
  # Threshold the blue image
  device, b_thresh = pcv.binary_threshold(b, 138, 255, 'light', device, args.debug)
  device, b_cnt = pcv.binary_threshold(b, 138, 255, 'light', device, args.debug)
  
  # Fill small objects
  device, b_fill = pcv.fill(b_thresh, b_cnt, 150, device, args.debug)
  
  # Join the thresholded saturation and blue-yellow images
  device, bs = pcv.logical_and(s_fill, b_fill, device, args.debug)
  
  # Apply Mask (for vis images, mask_color=white)
  device, masked = pcv.apply_mask(img, bs, 'white', device, args.debug)
  
  # Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
  device, masked_a = pcv.rgb2gray_lab(masked, 'a', device, args.debug)
  device, masked_b = pcv.rgb2gray_lab(masked, 'b', device, args.debug)
  
  # Threshold the green-magenta and blue images
  device, maskeda_thresh = pcv.binary_threshold(masked_a, 122, 255, 'dark', device, args.debug)
  device, maskedb_thresh = pcv.binary_threshold(masked_b, 133, 255, 'light', device, args.debug)
  
  # Join the thresholded saturation and blue-yellow images (OR)
  device, ab = pcv.logical_or(maskeda_thresh, maskedb_thresh, device, args.debug)
  device, ab_cnt = pcv.logical_or(maskeda_thresh, maskedb_thresh, device, args.debug)
  
  # Fill small objects
  device, ab_fill = pcv.fill(ab, ab_cnt, 200, device, args.debug)
  
  # Apply mask (for vis images, mask_color=white)
  device, masked2 = pcv.apply_mask(masked, ab_fill, 'white', device, args.debug)
  
  # Select area with black bars and find overlapping plant material
  device, roi1, roi_hierarchy1= pcv.define_roi(masked2,'rectangle', device, None, 'default', args.debug,True, 0, 0,-1900,0)
  device, id_objects1,obj_hierarchy1 = pcv.find_objects(masked2, ab_fill, device, args.debug)
  device,roi_objects1, hierarchy1, kept_mask1, obj_area1 = pcv.roi_objects(masked2,'cutto',roi1,roi_hierarchy1,id_objects1,obj_hierarchy1,device, args.debug)
  device, masked3 = pcv.apply_mask(masked2, kept_mask1, 'white', device, args.debug)
  device, masked_a1 = pcv.rgb2gray_lab(masked3, 'a', device, args.debug)
  device, masked_b1 = pcv.rgb2gray_lab(masked3, 'b', device, args.debug)
  device, maskeda_thresh1 = pcv.binary_threshold(masked_a1, 122, 255, 'dark', device, args.debug)
  device, maskedb_thresh1 = pcv.binary_threshold(masked_b1, 170, 255, 'light', device, args.debug)
  device, ab1 = pcv.logical_or(maskeda_thresh1, maskedb_thresh1, device, args.debug)
  device, ab_cnt1 = pcv.logical_or(maskeda_thresh1, maskedb_thresh1, device, args.debug)
  device, ab_fill1 = pcv.fill(ab1, ab_cnt1, 300, device, args.debug)

  
  device, roi2, roi_hierarchy2= pcv.define_roi(masked2,'rectangle', device, None, 'default', args.debug,True, 1900, 0,0,0)
  device, id_objects2,obj_hierarchy2 = pcv.find_objects(masked2, ab_fill, device, args.debug)
  device,roi_objects2, hierarchy2, kept_mask2, obj_area2 = pcv.roi_objects(masked2,'cutto',roi2,roi_hierarchy2,id_objects2,obj_hierarchy2,device, args.debug)
  device, masked4 = pcv.apply_mask(masked2, kept_mask2, 'white', device, args.debug)
  device, masked_a2 = pcv.rgb2gray_lab(masked4, 'a', device, args.debug)
  device, masked_b2 = pcv.rgb2gray_lab(masked4, 'b', device, args.debug)
  device, maskeda_thresh2 = pcv.binary_threshold(masked_a2, 122, 255, 'dark', device, args.debug)
  device, maskedb_thresh2 = pcv.binary_threshold(masked_b2, 170, 255, 'light', device, args.debug)
  device, ab2 = pcv.logical_or(maskeda_thresh2, maskedb_thresh2, device, args.debug)
  device, ab_cnt2 = pcv.logical_or(maskeda_thresh2, maskedb_thresh2, device, args.debug)
  device, ab_fill2 = pcv.fill(ab2, ab_cnt2, 200, device, args.debug)
  
  device, ab_cnt3 = pcv.logical_or(ab_fill1, ab_fill2, device, args.debug)
  device, masked3 = pcv.apply_mask(masked2, ab_cnt3, 'white', device, args.debug)
  
  # Identify objects
  device, id_objects3,obj_hierarchy3 = pcv.find_objects(masked2, ab_fill, device, args.debug)

  # Define ROI
  device, roi3, roi_hierarchy3= pcv.define_roi(masked2,'rectangle', device, None, 'default', args.debug,True, 500, 0,-450,-530)
 
  # Decide which objects to keep and combine with objects overlapping with black bars
  device,roi_objects3, hierarchy3, kept_mask3, obj_area1 = pcv.roi_objects(img,'cutto',roi3,roi_hierarchy3,id_objects3,obj_hierarchy3,device, args.debug)
  device, kept_mask4_1 = pcv.logical_or(ab_cnt3, kept_mask3, device, args.debug)
  device, kept_cnt = pcv.logical_or(ab_cnt3, kept_mask3, device, args.debug)
  device, kept_mask4 = pcv.fill(kept_mask4_1, kept_cnt, 200, device, args.debug)
  device, masked5 = pcv.apply_mask(masked2, kept_mask4, 'white', device, args.debug)
  device, id_objects4,obj_hierarchy4 = pcv.find_objects(masked5, kept_mask4, device, args.debug)
  device, roi4, roi_hierarchy4= pcv.define_roi(masked2,'rectangle', device, None, 'default', args.debug,False, 0, 0,0,0)
  device,roi_objects4, hierarchy4, kept_mask4, obj_area = pcv.roi_objects(img,'partial',roi4,roi_hierarchy4,id_objects4,obj_hierarchy4,device, args.debug)

 # Object combine kept objects
  device, obj, mask = pcv.object_composition(img, roi_objects4, hierarchy4, device, args.debug)
  
############## Analysis ################  
  
  # Find shape properties, output shape image (optional)
  device, shape_header,shape_data,shape_img = pcv.analyze_object(img, args.image, obj, mask, device,args.debug,args.outdir+'/'+filename)
   
  # Shape properties relative to user boundary line (optional)
  device, boundary_header,boundary_data, boundary_img1= pcv.analyze_bound(img, args.image,obj, mask, 950, device,args.debug,args.outdir+'/'+filename)
  
  # Tiller Tool Test
  device, tillering_header, tillering_data, tillering_img= pcv.tiller_count(img, args.image,obj, mask, 965, device,args.debug,args.outdir+'/'+filename)

  
  # Determine color properties: Histograms, Color Slices and Pseudocolored Images, output color analyzed images (optional)
  device, color_header,color_data,norm_slice= pcv.analyze_color(img, args.image, kept_mask4, 256, device, args.debug,'all','rgb','v',args.outdir+'/'+filename)
  
  # Output shape and color data
  pcv.print_results(args.image, shape_header, shape_data)
  pcv.print_results(args.image, color_header, color_data)
  pcv.print_results(args.image, boundary_header, boundary_data)
  pcv.print_results(args.image, tillering_header,tillering_data)
  
if __name__ == '__main__':
  main()#!/usr/bin/env python

