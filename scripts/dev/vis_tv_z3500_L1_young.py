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
  brass_mask = cv2.imread(args.roi)
  
  # Pipeline step
  device = 0

  # Convert RGB to HSV and extract the Saturation channel
  device, s = pcv.rgb2gray_hsv(img, 's', device, args.debug)
  
  # Threshold the Saturation image
  device, s_thresh = pcv.binary_threshold(s, 49, 255, 'light', device, args.debug)
  
  # Median Filter
  device, s_mblur = pcv.median_blur(s_thresh, 5, device, args.debug)
  device, s_cnt = pcv.median_blur(s_thresh, 5, device, args.debug)
  
  # Fill small objects
  device, s_fill = pcv.fill(s_mblur, s_cnt, 150, device, args.debug)
  
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
  
  # Mask pesky brass piece
  device, brass_mask1 = pcv.rgb2gray_hsv(brass_mask, 'v', device, args.debug)
  device, brass_thresh = pcv.binary_threshold(brass_mask1, 0, 255, 'light', device, args.debug)
  device, brass_inv=pcv.invert(brass_thresh, device, args.debug)
  device, brass_masked = pcv.apply_mask(masked, brass_inv, 'white', device, args.debug)
  
  # Further mask soil and car
  device, masked_a = pcv.rgb2gray_lab(brass_masked, 'a', device, args.debug)
  device, soil_car = pcv.binary_threshold(masked_a, 128, 255, 'dark', device, args.debug)
  device, soil_masked = pcv.apply_mask(brass_masked, soil_car, 'white', device, args.debug)
  
  # Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
  device, soil_a = pcv.rgb2gray_lab(soil_masked, 'a', device, args.debug)
  device, soil_b = pcv.rgb2gray_lab(soil_masked, 'b', device, args.debug)
  
  # Threshold the green-magenta and blue images
  device, soila_thresh = pcv.binary_threshold(soil_a, 118, 255, 'dark', device, args.debug)
  device, soilb_thresh = pcv.binary_threshold(soil_b, 140, 255, 'light', device, args.debug)

  # Join the thresholded saturation and blue-yellow images (OR)
  device, soil_ab = pcv.logical_or(soila_thresh, soilb_thresh, device, args.debug)
  device, soil_ab_cnt = pcv.logical_or(soila_thresh, soilb_thresh, device, args.debug)

  # Fill small objects
  device, soil_fill = pcv.fill(soil_ab, soil_ab_cnt, 200, device, args.debug)

  # Median Filter
  device, soil_mblur = pcv.median_blur(soil_fill, 5, device, args.debug)
  device, soil_cnt = pcv.median_blur(soil_fill, 5, device, args.debug)
  
  # Apply mask (for vis images, mask_color=white)
  device, masked2 = pcv.apply_mask(soil_masked, soil_cnt, 'white', device, args.debug)
  
  # Identify objects
  device, id_objects,obj_hierarchy = pcv.find_objects(masked2, soil_cnt, device, args.debug)

  # Define ROI
  device, roi1, roi_hierarchy= pcv.define_roi(img,'circle', device, None, 'default', args.debug,True, 0,50,-700,-700)
  
  # Decide which objects to keep
  device,roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img,'partial',roi1,roi_hierarchy,id_objects,obj_hierarchy,device, args.debug)
  
  # Object combine kept objects
  device, obj, mask = pcv.object_composition(img, roi_objects, hierarchy3, device, args.debug)
  
############## Analysis ################  
  
  # Find shape properties, output shape image (optional)
  device, shape_header,shape_data,shape_img = pcv.analyze_object(img, args.image, obj, mask, device,args.debug,args.outdir+'/'+filename)
  
  # Determine color properties: Histograms, Color Slices and Pseudocolored Images, output color analyzed images (optional)
  device, color_header,color_data,norm_slice= pcv.analyze_color(img, args.image, kept_mask, 256, device, args.debug,'all','rgb','v','img',300,args.outdir+'/'+filename)
  
  # Output shape and color data
  pcv.print_results(args.image, shape_header, shape_data)
  pcv.print_results(args.image, color_header, color_data)
  
if __name__ == '__main__':
  main()
