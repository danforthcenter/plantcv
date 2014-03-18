#!/usr/bin/python
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
    
#################################################################################################################################################
   
"""Object Idenfication and Shape Functions Below"""

#################################################################################################################################################


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
    
### RGB -> Gray
def rgb2gray(img, device, debug=False):
  # Convert image from RGB colorspace to Gray
  # img = image object, RGB colorspace
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print image
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  device += 1
  if debug:
    print_image(gray, str(device) + '_gray.png')
  return device, gray

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
  for c,cnt in enumerate(contours):
    if hierarchy[0][c][0] == -1:
      m = cv2.moments(cnt)
      area = m['m00']
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

### Join images (AND)
def logical_and(img1, img2, device, debug=False):
  # Join two images using the bitwise AND operator
  # img1, img2 = image objects, grayscale
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print image
  device += 1
  merged = cv2.bitwise_and(img1, img2)
  if debug:
    print_image(merged, str(device) + '_and_joined.png')
  return device, merged

### Join images (OR)
def logical_or(img1, img2, device, debug=False):
  # Join two images using the bitwise OR operator
  # img1, img2 = image objects, grayscale
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print image
  device += 1
  merged = cv2.bitwise_or(img1, img2)
  if debug:
    print_image(merged, str(device) + '_or_joined.png')
  return device, merged

### Join images (XOR)
def logical_xor(img1, img2, device, debug=False):
  # Join two images using the bitwise XOR operator
  # img1, img2 = image objects, grayscale
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print image
  device += 1
  merged = cv2.bitwise_xor(img1, img2)
  if debug:
    print_image(merged, str(device) + '_xor_joined.png')
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

### Find Objects
def find_objects(img, mask, device, debug=False):
  # find all objects and color them blue
  # img = image that the objects will be overlayed
  # mask = what is used for object detection
  # device = device number.  Used to count steps in the pipeline
  # debug = True/False. If True, print image
  device += 1
  mask1=np.copy(mask)
  objects,hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
  cv2.drawContours(img,objects,-1, (255,0,0),-1, lineType=8,hierarchy=hierarchy)
  if debug:
    print_image(img, str(device) + '_id_objects.png')
  
  return device, objects, hierarchy

### View and Adjust ROI
def define_roi(img, roi, roi_input, shape, device, debug=False, adjust=False, x_adj=0, y_adj=0, w_adj=0, h_adj=0, ):
  # img = img to overlay roi 
  # roi_base = user input ROI image, object area should be white and background should be black, only one ROI can be specified at once
  # roi_input = type of file roi_base is, either 'binary' or 'rgb'
  # shape = desired shape of final roi, either 'rectangle' or 'circle', if  user inputs rectangular roi but chooses 'circle' for shape then a circle is fitted around rectangular roi (and vice versa)
  # device = device number.  Used to count steps in the pipeline
  # debug = True/False. If True, print image
  # adjust= either 'True' or 'False', if 'True' allows user to adjust ROI
  # x_adj = adjust center along x axis
  # y_adj = adjust center along y axis
  # w_adj = adjust width
  # h_adj = adjust height
  
  device += 1
  ori_img=np.copy(img)
  
  # Allows user to enter either RGB or binary image (made with imagej or some other program) as a base ROI (that can be adjusted below)
  if roi_input== 'rgb':
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    ret,v_img = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY)
    roi_contour,hierarchy = cv2.findContours(v_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
  elif roi_input== 'binary':
    roi_contour,hierarchy = cv2.findContours(rois,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)  
  else:
    fatal_error('ROI Input' + roi_input + ' is not "binary" or "rgb"!')
    
  # If the ROI is exactly in the 'correct' position 
  if adjust==False:    
    for cnt in roi_contour:
      size = 2056,2454, 3
      background = np.zeros(size, dtype=np.uint8)
      if shape=='rectangle':
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(background,(x,y),(x+w,y+h),(0,255,0),5)
        rect = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
        rect_contour,hierarchy = cv2.findContours(rect,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(ori_img,rect_contour[0],-1, (255,0,0),5)
        if debug:
          print_image(ori_img, str(device) + '_roi.png')
        return device, rect_contour, hierarchy
      elif shape== 'circle':
        x,y,w,h = cv2.boundingRect(cnt)
        center = (int(w/2),int(h/2))
        if h>w:
          radius = int(w/2)
          cv2.circle(background,center,radius,(255,255,255),-1)
          circle = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
          circle_contour,hierarchy = cv2.findContours(circle,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
          cv2.drawContours(ori_img,circle_contour[0],-1, (255,0,0),5)
          if debug:
            print_image(ori_img, str(device) + '_roi.png')
          return device, circle_contour, hierarchy
        else:
          radius = int(h/2)
          cv2.circle(background,center,radius,(255,255,255),-1)
          circle = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
          circle_contour,hierarchy = cv2.findContours(circle,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
          cv2.drawContours(ori_img,circle_contour[0],-1, (255,0,0),5)
          if debug:
            print_image(ori_img, str(device) + '_roi.png')
          return device, circle_contour, hierarchy
      elif shape== 'ellipse': 
        x,y,w,h = cv2.boundingRect(cnt)
        center = (int(w/2),int(h/2))
        if w>h:
          cv2.ellipse(background,center,(w/2,h/2),0,0,360, (0,255,0), 2)
          ellipse = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
          ellipse_contour,hierarchy = cv2.findContours(ellipse,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
          cv2.drawContours(ori_img,ellipse_contour[0],-1, (255,0,0),5)
          if debug:
            print_image(ori_img, str(device) + '_roi.png')
          return device, ellipse_contour, hierarchy
        else:
          cv2.ellipse(ori_img,center,(h/2,w/2),0,0,360, (0,255,0), 2)
          cv2.ellipse(background,center,(h/2,w/2),0,0,360, (0,255,0), 2)
          ellipse = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
          ellipse_contour,hierarchy = cv2.findContours(ellipse,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
          cv2.drawContours(ori_img,ellipse_contour[0],-1, (255,0,0),5)
          if debug:
            print_image(ori_img, str(device) + '_roi.png')
          return device, ellipse_contour, hierarchy
      else:
          fatal_error('Shape' + shape + ' is not "rectangle", "circle", or "ellipse"!')
          
  # If the user wants to change the shape of the ROI or adjust ROI size or position   
  if adjust==True:
    if x_adj==0 and y_adj==0 and w_adj==0 and h_adj==0:
      fatal_error( 'If Adjust is True then x_adj, y_adj, w_adj or h_adj must have a non-zero value')
    else:
      for cnt in roi_contour:
        size = 2056,2454, 3
        background = np.zeros(size, dtype=np.uint8)
        if shape=='rectangle':
          x,y,w,h = cv2.boundingRect(cnt)
          x1=x+x_adj
          y1=y+y_adj
          w1=w+w_adj
          h1=h+h_adj
          cv2.rectangle(background,(x1,y1),(x+w1,y+h1),(0,255,0),1)
          rect = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
          rect_contour,hierarchy = cv2.findContours(rect,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
          cv2.drawContours(ori_img,rect_contour[0],-1, (255,0,0),5)
          if debug:
            print_image(ori_img, str(device) + '_roi.png')
          return device, rect_contour, hierarchy
        elif shape== 'circle':
          x,y,w,h = cv2.boundingRect(cnt)
          x1=x+x_adj
          y1=y+y_adj
          w1=w+w_adj
          h1=h+h_adj
          center = (int((w+x1)/2),int((h+y1)/2))
          if h>w:
            radius = int(w1/2)
            cv2.circle(background,center,radius,(255,255,255),-1)
            circle = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
            circle_contour,hierarchy = cv2.findContours(circle,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(ori_img,circle_contour[0],-1, (255,0,0),5)
            if debug:
              print_image(ori_img, str(device) + '_roi.png')
            return device, circle_contour, hierarchy
          else:
            radius = int(h1/2)
            cv2.circle(background,center,radius,(255,255,255),-1)
            circle = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
            circle_contour,hierarchy = cv2.findContours(circle,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(ori_img,circle_contour[0],-1, (255,0,0),5)
            if debug:
              print_image(ori_img, str(device) + '_roi.png')
            return device, circle_contour, hierarchy
        elif shape== 'ellipse': 
          x,y,w,h = cv2.boundingRect(cnt)
          x1=x+x_adj
          y1=y+y_adj
          w1=w+w_adj
          h1=h+h_adj
          center = (int((w+x1)/2),int((h+y1)/2))
          if w>h:
            cv2.ellipse(background,center,(w1/2,h1/2),0,0,360, (0,255,0), 2)
            ellipse = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
            ellipse_contour,hierarchy = cv2.findContours(ellipse,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(ori_img,ellipse_contour[0],-1, (255,0,0),5)
            if debug:
              print_image(ori_img, str(device) + '_roi.png')
            return device, ellipse_contour, hierarchy
          else:
            cv2.ellipse(background,center,(h1/2,w1/2),0,0,360, (0,255,0), 2)
            ellipse = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
            ellipse_contour,hierarchy = cv2.findContours(ellipse,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(ori_img,ellipse_contour[0],-1, (255,0,0),5)
            if debug:
              print_image(ori_img, str(device) + '_roi.png')
            return device, ellipse_contour, hierarchy
        else:
            fatal_error('Shape' + shape + ' is not "rectangle", "circle", or "ellipse"!')
        
### Find Objects Partially Inside Region of Interest or Cut Objects to Region of Interest
def roi_objects(img,roi_type,roi_contour, roi_hierarchy,object_contour, obj_hierarchy, device, debug=False):
 # img = img to display kept objects
 # roi_type = 'cutto' or 'partial' (for partially inside)
 # roi_contour = contour of roi, output from "View and Ajust ROI" function
 # roi_hierarchy = contour of roi, output from "View and Ajust ROI" function
 # object_contour = contours of objects, output from "Identifying Objects" fuction
 # obj_hierarchy = hierarchy of objects, output from "Identifying Objects" fuction
 # device = device number.  Used to count steps in the pipeline
  device +=1
  size = 2056,2454, 3
  background = np.zeros(size, dtype=np.uint8)
  ori_img=np.copy(img)
  w_back=background+255
  background1 = np.zeros(size, dtype=np.uint8)
  background2 = np.zeros(size, dtype=np.uint8)

  # Allows user to find all objects that are completely inside or overlapping with ROI
  if roi_type=='partial':
    for c,cnt in enumerate(object_contour):
      length=(len(cnt)-1)
      stack=np.vstack(cnt)
      test=[]
      keep=False
      for i in range(0,length):
        pptest=cv2.pointPolygonTest(roi_contour[0], (stack[i][0],stack[i][1]), False)
        if int(pptest)!=-1:
          keep=True
      if keep==True:
        if obj_hierarchy[0][c][3]>-1:
          cv2.drawContours(w_back,object_contour,c, (255,255,255),-1, lineType=8,hierarchy=obj_hierarchy)
        else:  
          cv2.drawContours(w_back,object_contour,c, (0,0,0),-1, lineType=8,hierarchy=obj_hierarchy)
      else:
        cv2.drawContours(w_back,object_contour,c, (255,255,255),-1, lineType=8,hierarchy=obj_hierarchy)
     
    kept=cv2.cvtColor(w_back, cv2.COLOR_RGB2GRAY )
    kept_obj= cv2.bitwise_not(kept)
    mask=np.copy(kept_obj)
    obj_area=cv2.countNonZero(kept_obj)
    kept_cnt,hierarchy=cv2.findContours(kept_obj,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(ori_img,kept_cnt,-1, (0,255,0),-1, lineType=8,hierarchy=hierarchy)
    cv2.drawContours(ori_img,roi_contour,-1, (255,0,0),5, lineType=8,hierarchy=roi_hierarchy)
  
  # Allows uer to cut objects to the ROI (all objects completely outside ROI will not be kept)
  elif roi_type=='cutto':
    cv2.drawContours(background1,object_contour,-1, (255,255,255),-1, lineType=8,hierarchy=obj_hierarchy)
    roi_points=np.vstack(roi_contour[0])
    cv2.fillPoly(background2,[roi_points], (255,255,255))
    obj_roi=cv2.multiply(background1,background2)
    kept_obj=cv2.cvtColor(obj_roi, cv2.COLOR_RGB2GRAY)
    mask=np.copy(kept_obj)
    obj_area=cv2.countNonZero(kept_obj)
    kept_cnt,hierarchy = cv2.findContours(kept_obj,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(w_back,kept_cnt,-1, (0,0,0),-1)
    cv2.drawContours(ori_img,kept_cnt,-1, (0,255,0),-1, lineType=8,hierarchy=hierarchy)
    cv2.drawContours(ori_img,roi_contour,-1, (255,0,0),5, lineType=8,hierarchy=roi_hierarchy)
         
  else:
    fatal_error('ROI Type' + roi_type + ' is not "cutto" or "partial"!')
  
  if debug:
    print_image(w_back, str(device) + '_roi_objects.png')
    print_image(ori_img, str(device) + '_obj_on_img.png')
    print_image(mask, str(device) + '_roi_mask.png')
    print ('Object Area=', obj_area)
  
  return device, kept_cnt, hierarchy, mask, obj_area

### Object composition
def object_composition(img, contours, hierarchy, device, debug=False):
  # Groups objects into a single object, usually done after object filtering
  # contours = object list
  # device = device number. Used to count steps in the pipeline
  # debug= True/False. If True, print image
  device += 1
  ori_img=np.copy(img)
  
  stack = np.zeros((len(contours), 1))
  r,g,b = cv2.split(ori_img)
  mask = np.zeros(g.shape,dtype=np.uint8)
  
  for c,cnt in enumerate(contours):
    #if hierarchy[0][c][3] == -1:
    if hierarchy[0][c][2] == -1 and hierarchy[0][c][3] > -1:
      stack[c] = 0
      #stack[c] = 1
      #cv2.drawContours(img, cnt, -1, color_palette(1)[0], 3)
      #np.append(group, np.vstack(cnt))
    else:
      stack[c] = 1
      #cv2.drawContours(img, contours, -1, color_palette(1)[0], -1, hierarchy=hierarchy)
      #stack[c] = 0
  ids = np.where(stack==1)[0]
  group = np.vstack(contours[i] for i in ids)
  cv2.drawContours(mask,contours, -1, (255), -1, hierarchy=hierarchy)
  
  if debug:
    #for cnt in contours:
    #  cv2.drawContours(img, cnt, -1, (255,0,0), 2)
    #cv2.drawContours(img, group, -1, (255,0,0), 2)
    print_image(ori_img, str(device) + '_objcomp.png')
    print_image(mask, str(device) + '_objcomp_mask.png')
  return device, group, mask

      
### Analyzes an object and outputs numeric properties
def analyze_object(img, obj, mask, device, debug=False):
  # Outputs numeric properties for an input object (contour or grouped contours)
  # Also color classification?
  # img = image object (most likely the original), color(RGB)
  # obj = single or grouped contour object
  # device = device number. Used to count steps in the pipeline
  # debug= True/False. If True, print image
  device += 1
  ori_img=np.copy(img)
  
  # Convex Hull
  hull = cv2.convexHull(obj)
  # Moments
#  m = cv2.moments(obj)
  m = cv2.moments(mask, binaryImage=True)
  ## Properties
  # Area
  area = m['m00']
  
  if area:
    # Convex Hull area
    hull_area = cv2.contourArea(hull)
    # Solidity
    solidity = area / hull_area
    # Perimeter
    perimeter = cv2.arcLength(obj, closed=True)
    # x and y position (bottom left?) and extent x (width) and extent y (height)
    x,y,width,height = cv2.boundingRect(obj)
    # Centroid (center of mass x, center of mass y)
    cmx,cmy = (m['m10']/m['m00'], m['m01']/m['m00'])
    # Ellipse
    center, axes, angle = cv2.fitEllipse(obj)
    major_axis = np.argmax(axes)
    minor_axis = 1 - major_axis
    major_axis_length = axes[major_axis]
    minor_axis_length = axes[minor_axis]
    eccentricity = np.sqrt(1 - (axes[minor_axis]/axes[major_axis]) ** 2)
  else:
    hull_area, solidity, perimeter, width, height, cmx, cmy = 'ND', 'ND', 'ND', 'ND', 'ND', 'ND', 'ND'
      
  data = {
    'area' : area,
    'hull_area' : hull_area,
    'solidity' : solidity,
    'perimeter' : perimeter,
    'width' : width,
    'height' : height,
    'center_mass_x' : cmx,
    'center_mass_y' : cmy
  }
      
  # Draw properties
  if debug and area:
    cv2.drawContours(ori_img, obj, -1, (255,0,0), 2)
    cv2.drawContours(ori_img, [hull], -1, (0,0,255), 3)
    cv2.line(ori_img, (x,y), (x+width,y), (0,0,255), 3)
    cv2.line(ori_img, (int(cmx),y), (int(cmx),y+height), (0,0,255), 3)
    cv2.circle(ori_img, (int(cmx),int(cmy)), 10, (0,0,255), 3)
      
  #if debug:
  #  print_image(img, str(device) + '_obj.png')

  return device, data

### Color palette returns an array of colors (rainbow)
def color_palette(num):
  # Returns array of colors length num
  # num = number of colors to return
  # If num = 1 a random color is returned
  # Otherwise evenly spaced colors are returned
  
  # Rainbow color scheme (red->red)
  rainbow = ((0,0,255),(0,6,255),(0,12,255),(0,18,255),(0,24,255),(0,30,255),(0,36,255),(0,42,255),(0,48,255),(0,54,255),(0,60,255),(0,66,255),(0,72,255),(0,78,255),(0,84,255),(0,90,255),(0,96,255),(0,102,255),(0,108,255),(0,114,255),(0,120,255),(0,126,255),(0,131,255),(0,137,255),(0,143,255),(0,149,255),(0,155,255),(0,161,255),(0,167,255),(0,173,255),(0,179,255),(0,185,255),(0,191,255),(0,197,255),(0,203,255),(0,209,255),(0,215,255),(0,221,255),(0,227,255),(0,233,255),(0,239,255),(0,245,255),(0,251,255),(0,255,253),(0,255,247),(0,255,241),(0,255,235),(0,255,229),(0,255,223),(0,255,217),(0,255,211),(0,255,205),(0,255,199),(0,255,193),(0,255,187),(0,255,181),(0,255,175),(0,255,169),(0,255,163),(0,255,157),(0,255,151),(0,255,145),(0,255,139),(0,255,133),(0,255,128),(0,255,122),(0,255,116),(0,255,110),(0,255,104),(0,255,98),(0,255,92),(0,255,86),(0,255,80),(0,255,74),(0,255,68),(0,255,62),(0,255,56),(0,255,50),(0,255,44),(0,255,38),(0,255,32),(0,255,26),(0,255,20),(0,255,14),(0,255,8),(0,255,2),(4,255,0),(10,255,0),(16,255,0),(22,255,0),(28,255,0),(34,255,0),(40,255,0),(46,255,0),(52,255,0),(58,255,0),(64,255,0),(70,255,0),(76,255,0),(82,255,0),(88,255,0),(94,255,0),(100,255,0),(106,255,0),(112,255,0),(118,255,0),(124,255,0),(129,255,0),(135,255,0),(141,255,0),(147,255,0),(153,255,0),(159,255,0),(165,255,0),(171,255,0),(177,255,0),(183,255,0),(189,255,0),(195,255,0),(201,255,0),(207,255,0),(213,255,0),(219,255,0),(225,255,0),(231,255,0),(237,255,0),(243,255,0),(249,255,0),(255,255,0),(255,249,0),(255,243,0),(255,237,0),(255,231,0),(255,225,0),(255,219,0),(255,213,0),(255,207,0),(255,201,0),(255,195,0),(255,189,0),(255,183,0),(255,177,0),(255,171,0),(255,165,0),(255,159,0),(255,153,0),(255,147,0),(255,141,0),(255,135,0),(255,129,0),(255,124,0),(255,118,0),(255,112,0),(255,106,0),(255,100,0),(255,94,0),(255,88,0),(255,82,0),(255,76,0),(255,70,0),(255,64,0),(255,58,0),(255,52,0),(255,46,0),(255,40,0),(255,34,0),(255,28,0),(255,22,0),(255,16,0),(255,10,0),(255,4,0),(255,0,2),(255,0,8),(255,0,14),(255,0,20),(255,0,26),(255,0,32),(255,0,38),(255,0,44),(255,0,50),(255,0,56),(255,0,62),(255,0,68),(255,0,74),(255,0,80),(255,0,86),(255,0,92),(255,0,98),(255,0,104),(255,0,110),(255,0,116),(255,0,122),(255,0,128),(255,0,133),(255,0,139),(255,0,145),(255,0,151),(255,0,157),(255,0,163),(255,0,169),(255,0,175),(255,0,181),(255,0,187),(255,0,193),(255,0,199),(255,0,205),(255,0,211),(255,0,217),(255,0,223),(255,0,229),(255,0,235),(255,0,241),(255,0,247),(255,0,253),(251,0,255),(245,0,255),(239,0,255),(233,0,255),(227,0,255),(221,0,255),(215,0,255),(209,0,255),(203,0,255),(197,0,255),(191,0,255),(185,0,255),(179,0,255),(173,0,255),(167,0,255),(161,0,255),(155,0,255),(149,0,255),(143,0,255),(137,0,255),(131,0,255),(126,0,255),(120,0,255),(114,0,255),(108,0,255),(102,0,255),(96,0,255),(90,0,255),(84,0,255),(78,0,255),(72,0,255),(66,0,255),(60,0,255),(54,0,255),(48,0,255),(42,0,255),(36,0,255),(30,0,255),(24,0,255),(18,0,255),(12,0,255),(6,0,255))
  
  if num == 1:
    color = rainbow[randrange(0,255)]
    return [color]
  else:
    dist = int(len(rainbow) / num)
    colors = []
    index = 0
    for i in range(1,num + 1):
      colors.append(rainbow[index])
      index += dist
    return colors
  
#################################################################################################################################################
   
"""ANAlYSIS FUNCTIONS BELOW"""

#################################################################################################################################################

    
### Analyze Color of Object
def analyze_color(img, mask,bins, device, debug=False,visualize=True,visualize_type='RGB',pseudocolor=True,pseudo_channel='v'):
  # img = image
  # mask = mask made from selected contours
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print data and histograms
  # visualize = True/False
  # visualize_type = 'RGB', 'HSV' or 'LAB'
  # pseudocolor= True/False. If True, create pseudocolored image
  # pseudo_channel= 'h','s', or 'v', creates pseduocolored image based on the specified channel
  
  device += 1
  
  masked=cv2.bitwise_and(img,img, mask=mask)
  b,g,r=cv2.split(masked)
  lab = cv2.cvtColor(masked, cv2.COLOR_BGR2LAB)
  l,m,y=cv2.split(lab)
  hsv = cv2.cvtColor(masked, cv2.COLOR_BGR2HSV)
  h,s,v=cv2.split(hsv)
  
  channel=(b,g,r,l,m,y,h,s,v)
  hist_data = {}
  graph_color=('blue','forestgreen','red','dimgray','magenta','yellow','blueviolet','cyan','orange' )
  label=('blue','green','red', 'lightness','green-magenta','blue-yellow','hue','saturation', 'value')

  # Color Histogram Stats
  for c,i in enumerate(channel):
    if c<=8: #0-2 for RGB ony, 3-5 for LAB ony, 6-8 for HSV only
      i_bin=i/(256/bins)
      hist = cv2.calcHist([i_bin],[0],mask,[bins], [0,(bins-1)])
      #max_bin= np.argmax(hist)
      #max_pixel=np.amax(hist)
      #non_zero=np.nonzero(hist)
      #non_zero_stack=np.vstack(non_zero)
      #last_non_zero=(len(non_zero_stack))-2
      hist_data[label[c]] = hist
      hist1 = cv2.calcHist([i_bin],[0],mask,[bins], [0,(bins-1)])    
      plt.plot(hist1,color=graph_color[c],label=label[c])
      plt.xlim([0,(bins-1)])
      plt.legend() 
      plt.savefig(str(device)+'color_hist.png')
  plt.clf()
      
      #hist_data[label[c]] = {
        #'bin with most pixels': max_bin,
        #'pixels in max bin': max_pixel,
        #'left_border':non_zero_stack[0][0],
        #'right_border':non_zero_stack[0][last_non_zero],
        #str(label[c]): hist
      #}
      
    #if debug:
      #print_image(masked, str(device) + '_masked_forcc.png')
      #if c<=8: #0-2 for RGB ony, 3-5 for LAB ony, 6-8 for HSV only
        #hist1 = cv2.calcHist([i_bin],[0],mask,[bins], [0,(bins-1)])    
        #plt.plot(hist1,color=graph_color[c],label=label[c])
        #plt.xlim([0,(bins-1)])
        #plt.legend() 
        #plt.savefig(str(device)+'color_hist.png')
  #plt.clf()

  # Generate Color Slice: Get Flattened Color Histogram for Visualization     
  if visualize==True:
    if visualize_type=='RGB':
      b_bin=b/(256/bins)
      g_bin=g/(256/bins)
      r_bin=r/(256/bins)
      b_hist = cv2.calcHist([b_bin],[0],mask,[bins], [0,(bins-1)])
      b_stack = np.vstack(b_hist)
      g_hist = cv2.calcHist([g_bin],[0],mask,[bins], [0,(bins-1)])
      g_stack= np.vstack(g_hist)
      r_hist = cv2.calcHist([r_bin],[0],mask,[bins], [0,(bins-1)])
      r_stack = np.vstack(r_hist)
    
      b_max=np.amax(b_stack)
      g_max=np.amax(g_stack)
      r_max=np.amax(r_stack)
      
      b_min=np.amin(b_stack)
      g_min=np.amin(g_stack)
      r_min=np.amin(r_stack)
      
      maximums=(b_max,g_max,r_max)
      minimums=(b_min,g_min,r_min)
      max_max=np.amax(maximums)
      min_min=np.amin(minimums)
      
      b_norm=((b_stack-min_min)/(max_max-min_min))*255
      g_norm=((g_stack-min_min)/(max_max-min_min))*255
      r_norm=((r_stack-min_min)/(max_max-min_min))*255
      
      #color_slice=np.dstack((b_stack,g_stack,r_stack))
      norm_slice=np.dstack((b_norm,g_norm,r_norm))
      #print_image(color_slice, str(device) + '_bgr_stack.png')
      #print_image(norm_slice, str(device) + '_bgr_norm.png')
    elif visualize_type=='HSV':
      h_bin=h/(256/bins)
      s_bin=s/(256/bins)
      v_bin=v/(256/bins)
      
      h_hist = cv2.calcHist([h_bin],[0],mask,[bins], [0,(bins-1)])
      h_stack = np.vstack(h_hist)
      s_hist = cv2.calcHist([s_bin],[0],mask,[bins], [0,(bins-1)])
      s_stack= np.vstack(s_hist)
      v_hist = cv2.calcHist([v_bin],[0],mask,[bins], [0,(bins-1)])
      v_stack = np.vstack(v_hist)
    
      h_max=np.amax(h_stack)
      s_max=np.amax(s_stack)
      v_max=np.amax(v_stack)
      
      h_min=np.amin(h_stack)
      s_min=np.amin(s_stack)
      v_min=np.amin(v_stack)
      
      maximums=(h_max,s_max,v_max)
      minimums=(h_min,s_min,v_min)
      max_max=np.amax(maximums)
      min_min=np.amin(minimums)
      
      h_norm=((h_stack-min_min)/(max_max-min_min))*255
      s_norm=((s_stack-min_min)/(max_max-min_min))*255
      v_norm=((v_stack-min_min)/(max_max-min_min))*255
      
      #color_slice=np.dstack((h_stack,s_stack,v_stack))
      norm_slice=np.dstack((h_norm,s_norm,v_norm))
      #print_image(color_slice, str(device) + '_hsv_stack.png')
      #print_image(norm_slice, str(device) + '_hsv_norm.png')
    elif visualize_type=='LAB':
      l_bin=l/(256/bins)
      m_bin=m/(256/bins)
      y_bin=y/(256/bins)
      
      l_hist = cv2.calcHist([l_bin],[0],mask,[bins], [0,(bins-1)])
      l_stack = np.vstack(l_hist)
      m_hist = cv2.calcHist([m_bin],[0],mask,[bins], [0,(bins-1)])
      m_stack= np.vstack(m_hist)
      y_hist = cv2.calcHist([y_bin],[0],mask,[bins], [0,(bins-1)])
      y_stack = np.vstack(y_hist)
    
      l_max=np.amax(l_stack)
      m_max=np.amax(m_stack)
      y_max=np.amax(y_stack)
      
      l_min=np.amin(l_stack)
      m_min=np.amin(m_stack)
      y_min=np.amin(y_stack)
      
      maximums=(l_max,m_max,y_max)
      minimums=(l_min,m_min,y_min)
      max_max=np.amax(maximums)
      min_min=np.amin(minimums)
      
      l_norm=((l_stack-min_min)/(max_max-min_min))*255
      m_norm=((m_stack-min_min)/(max_max-min_min))*255
      y_norm=((y_stack-min_min)/(max_max-min_min))*255
      
      #color_slice=np.dstack((c_stack,m_stack,y_stack))
      norm_slice=np.dstack((l_norm,m_norm,y_norm))
      #print_image(color_slice, str(device) + '_lab_stack.png')
      #print_image(norm_slice, str(device) + '_lab_norm.png')
    else:
      fatal_error('Visualize Type' + visualize_type + ' is not "RGB","HSV" or "LAB"!')
      
  # PseudoColor Image Based On h, s, or v Channel
  if pseudocolor==True:
    p_channel=pseudo_channel
    
    
    if p_channel=='v':
      size = 2056,2454
      background = np.zeros(size, dtype=np.uint8)
      w_back=background+255
      
      v_bin=v/(256/bins)
      
      v_img =plt.imshow(v_bin, vmin=0,vmax=(bins-1), cmap=cm.jet)
      plt.colorbar()
      
      mask_inv=cv2.bitwise_not(mask)
      img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      pot=cv2.bitwise_and(img_gray,img_gray,mask=mask_inv)
      pot_img=cv2.add(pot,mask)
      pot_rgba=np.dstack((pot_img,pot_img,pot_img,mask_inv))
      my_cmap = plt.get_cmap('binary_r')
      pot_img1 =plt.imshow(pot_rgba, cmap=my_cmap)
      plt.axis('off')
    
      plt.savefig(str(device)+'pseudocolor_on_ori.png')
      plt.clf()
      
      v_img =plt.imshow(v_bin, vmin=0,vmax=(bins-1), cmap=cm.jet)
      plt.colorbar()
      white_rgba=np.dstack((w_back,w_back,w_back,mask_inv))
      pot_img1 =plt.imshow(white_rgba, cmap=my_cmap)
      plt.axis('off')
      plt.savefig(str(device)+'pseudocolor_on_white.png')
      plt.clf()
      
    elif p_channel=='h':
      size = 2056,2454
      background = np.zeros(size, dtype=np.uint8)
      w_back=background+255
      
      h_bin=h/(256/bins)
      
      h_img =plt.imshow(h_bin, vmin=0,vmax=(bins-1), cmap=cm.jet)
      plt.colorbar()
      
      mask_inv=cv2.bitwise_not(mask)
      img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      pot=cv2.bitwise_and(img_gray,img_gray,mask=mask_inv)
      pot_img=cv2.add(pot,mask)
      pot_rgba=np.dstack((pot_img,pot_img,pot_img,mask_inv))
      my_cmap = plt.get_cmap('binary_r')
      pot_img1 =plt.imshow(pot_rgba, cmap=my_cmap)

      plt.axis('off')
      
      plt.savefig(str(device)+'pseudocolor_on_ori.png')
      plt.clf()
      
      h_img =plt.imshow(h_bin, vmin=0,vmax=(bins-1), cmap=cm.jet)
      plt.colorbar()
      white_rgba=np.dstack((w_back,w_back,w_back,mask_inv))
      pot_img1 =plt.imshow(white_rgba, cmap=my_cmap)
      plt.axis('off')
      plt.savefig(str(device)+'pseudocolor_on_white.png')
      plt.clf()
      
    elif p_channel=='s':
      size = 2056,2454
      background = np.zeros(size, dtype=np.uint8)
      w_back=background+255
      
      s_bin=s/(256/bins)
      
      s_img =plt.imshow(s_bin, vmin=0,vmax=(bins-1), cmap=cm.jet)
      plt.colorbar()
      
      mask_inv=cv2.bitwise_not(mask)
      img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      pot=cv2.bitwise_and(img_gray,img_gray,mask=mask_inv)
      pot_img=cv2.add(pot,mask)
      pot_rgba=np.dstack((pot_img,pot_img,pot_img,mask_inv))
      my_cmap = plt.get_cmap('binary_r')
      pot_img1 =plt.imshow(pot_rgba, cmap=my_cmap)

      plt.axis('off')
      
      plt.savefig(str(device)+'pseudocolor_on_ori.png')
      plt.clf()
      
      s_img =plt.imshow(s_bin, vmin=0,vmax=(bins-1), cmap=cm.jet)
      plt.colorbar()
      white_rgba=np.dstack((w_back,w_back,w_back,mask_inv))
      pot_img1 =plt.imshow(white_rgba, cmap=my_cmap)
      plt.axis('off')
      plt.savefig(str(device)+'pseudocolor_on_white.png')
      plt.clf()
    
    else:
      fatal_error('Pseudocolor Channel' + pseudo_channel + ' is not "h","s" or "v"!')

  return device, hist_data, norm_slice
