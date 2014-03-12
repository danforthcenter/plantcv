#!/usr/bin/python
import sys, traceback
import cv2
import numpy as np
import argparse
import plantcv as pcv

### Parse command-line arguments
def options():
  parser = argparse.ArgumentParser(description="Imaging processing with opencv")
  parser.add_argument("-i", "--image", help="Input image file.", required=True)
  parser.add_argument("-m", "--roi", help="Input region of interest file.", required=True)
  parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", action="store_true")
  args = parser.parse_args()
  return args

### Main pipeline
def main():
  # Get options
  args = options()
  
  # Read image
  img = cv2.imread(args.image)
  roi = cv2.imread(args.roi)
  # plain white image the same size as your image is needed to display objects on white background
  w_back = cv2.imread('white.png')
  
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

if __name__ == '__main__':
  main()





