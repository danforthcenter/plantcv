#!/usr/bin/python
import sys, traceback
import cv2
import numpy as np

### Error handling
def fatal_error(error):
  # Print out the error message that gets passed, then quit the program
  # Error = error message text
  raise RuntimeError(error)

### Print image to file
def print_image(img, filename):
  # Write the image object to the file specified
  # img = image object
  # filename = name of image file
  try:
    cv2.imwrite(filename, img)
  except:
    fatal_error("Unexpected error: " + sys.exc_info()[0])

### RGB -> HSV -> Gray
def rgb2gray_hsv(img, channel, device, debug=False):
  # Convert image from RGB colorspace to HSV colorspace
  # Returns the specified subchannel as a gray image
  # img = image object, RGB colorspace
  # channel = color subchannel (h = hue, s = saturation, v = value/intensity/brightness)
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print image
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  # Split HSV channels
  h,s,v = cv2.split(hsv)
  device += 1
  if channel == 'h':
    if debug:
      print_image(h, str(device) + '_hsv_hue.png')
    return device, h
  elif channel == 's':
    if debug:
      print_image(s, str(device) + '_hsv_saturation.png')
    return device, s
  elif channel == 'v':
    if debug:
      print_image(v, str(device) + '_hsv_value.png')
    return device, v
  else:
    fatal_error('Channel ' + channel + ' is not h, s or v!')

### RGB -> LAB -> Gray
def rgb2gray_lab(img, channel, device, debug=False):
  # Convert image from RGB colorspace to LAB colorspace
  # Returns the specified subchannel as a gray image
  # img = image object, RGB colorspace
  # channel = color subchannel (l = lightness, a = green-magenta, b = blue-yellow)
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print image
  lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
  # Split HSV channels
  l,a,b = cv2.split(lab)
  device += 1
  if channel == 'l':
    if debug:
      print_image(l, str(device) + '_lab_lightness.png')
    return device, l
  elif channel == 'a':
    if debug:
      print_image(a, str(device) + '_lab_green-magenta.png')
    return device, a
  elif channel == 'b':
    if debug:
      print_image(b, str(device) + '_lab_blue-yellow.png')
    return device, b
  else:
    fatal_error('Channel ' + channel + ' is not l, a or b!')

### Binary image threshold device
def binary_threshold(img, threshold, maxValue, object_type, device, debug=False):
  # Creates a binary image from a gray image based on the threshold value
  # img = img object, grayscale
  # threshold = threshold value (0-255)
  # maxValue = value to apply above threshold (usually 255 = white)
  # object_type = light or dark
  # If object is light then standard thresholding is done
  # If object is dark then inverse thresholding is done
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print image
  device += 1
  if object_type == 'light':
    ret,t_img = cv2.threshold(img, threshold, maxValue, cv2.THRESH_BINARY)
    if debug:
      print_image(t_img, str(device) + '_binary_threshold' + str(threshold) + '.png')
    return device, t_img
  elif object_type == 'dark':
    ret,t_img = cv2.threshold(img, threshold, maxValue, cv2.THRESH_BINARY_INV)
    if debug:
      print_image(t_img, str(device) + '_binary_threshold' + str(threshold) + '_inv.png')
    return device, t_img
  else:
    fatal_error('Object type ' + object_type + ' is not "light" or "dark"!')

### Median blur device
def median_blur(img, ksize, device, debug=False):
  # Applies a median blur filter (applies median value to central pixel within a kernel size ksize x ksize)
  # img = img object
  # ksize = kernel size => ksize x ksize box
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print image
  img_mblur = cv2.medianBlur(img, ksize)
  device += 1
  if debug:
    print_image(img_mblur, str(device) + '_median_blur' + str(ksize) + '.png')
  return device, img_mblur

### Object fill device
def fill(img, mask, size, device, debug=False):
  # Identifies objects and fills objects that are less than size
  # img = image object, grayscale. img will be returned after filling
  # mask = image object, grayscale. This image will be used to identify contours
  # size = minimum object area size in pixels (integer)
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print image
  device += 1
  
  # Find contours
  contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
  
  # Loop through contours, fill contours less than or equal to size in area
  for cnt in contours:
    area = cnt.size
    if area <= size:
      cv2.fillPoly(img, pts = cnt, color=(0,0,0))

  if debug:
    print_image(img, str(device) + '_fill' + str(size) + '.png')

  return device, img

### Invert gray image
def invert(img, device, debug=False):
  # Inverts grayscale images
  # img = image object, grayscale
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print image
  device += 1
  img_inv = cv2.bitwise_not(img)
  if debug:
    print_image(img_inv, str(device) + '_invert.png')
  return device, img_inv

### Join images
def logical_and(img1, img2, device, debug=False):
  # Join two images using the bitwise AND operator
  # img1, img2 = image objects, grayscale
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print image
  device += 1
  merged = cv2.bitwise_and(img1, img2)
  if debug:
    print_image(merged, str(device) + '_joined.png')
  return device, merged

### Apply White or Black Background Mask
def apply_mask(img, mask, mask_color, device, debug=False):
  # Apply white image mask to image, with bitwise AND operator bitwise NOT operator and ADD operator
  # img = image object, color(RGB)
  # mask= image object, binary (black background with white object)
  # mask_color= white or black  
  # device = device number. Used to count steps in the pipeline
  # debug= True/False. If True, print image
  device += 1
  if mask_color=='white':
    # Mask image
    masked_img= cv2.bitwise_and(img,img, mask = mask)
    # Create inverted mask for background
    mask_inv=cv2.bitwise_not(mask)
    # Invert the background so that it is white, but apply mask_inv so you don't white out the plant
    white_mask= cv2.bitwise_not(masked_img,mask=mask_inv)
    # Add masked image to white background (can't just use mask_inv because that is a binary)
    white_masked= cv2.add(masked_img, white_mask)
    if debug:
      print_image(white_masked, str(device) + '_wmasked.png')
    return device, white_masked
  elif mask_color=='black':
    masked_img= cv2.bitwise_and(img,img, mask = mask)
    if debug:
      print_image(masked_img, str(device) + '_bmasked.png')
    return device, masked_img
  else:
      fatal_error('Mask Color' + mask_color + ' is not "white" or "black"!')