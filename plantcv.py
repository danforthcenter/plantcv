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
from Bio.Statistics.lowess import lowess

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

### Read image
def readimage(filename):
  # Reads image into numpy ndarray and splits the path and image filename
  # filename = user inputed filename (possibly including a path)
  try:
    img = cv2.imread(filename)
  except:
    fatal_error("Cannot open " + filename);
  
  # Split path from filename
  path, img_name = os.path.split(filename)
  
  return img, path, img_name
    
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
      print_image(h, (str(device) + '_hsv_hue.png'))
    return device, h
  elif channel == 's':
    if debug:
      print_image(s, (str(device) + '_hsv_saturation.png'))
    return device, s
  elif channel == 'v':
    if debug:
      print_image(v, (str(device) + '_hsv_value.png'))
    return device, v
  else:
    fatal_error('Channel ' + (str(channel) + ' is not h, s or v!'))

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
      print_image(l, (str(device) + '_lab_lightness.png'))
    return device, l
  elif channel == 'a':
    if debug:
      print_image(a, (str(device) + '_lab_green-magenta.png'))
    return device, a
  elif channel == 'b':
    if debug:
      print_image(b, (str(device) + '_lab_blue-yellow.png'))
    return device, b
  else:
    fatal_error('Channel ' + str(channel) + ' is not l, a or b!')
    
### RGB -> Gray
def rgb2gray(img, device, debug=False):
  # Convert image from RGB colorspace to Gray
  # img = image object, RGB colorspace
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print image
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  device += 1
  if debug:
    print_image(gray, (str(device) + '_gray.png'))
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
      print_image(t_img, (str(device) + '_binary_threshold' + str(threshold) + '.png'))
    return device, t_img
  elif object_type == 'dark':
    ret,t_img = cv2.threshold(img, threshold, maxValue, cv2.THRESH_BINARY_INV)
    if debug:
      print_image(t_img, (str(device) + '_binary_threshold' + str(threshold) + '_inv.png'))
    return device, t_img
  else:
    fatal_error('Object type ' + str(object_type) + ' is not "light" or "dark"!')

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
    print_image(img_mblur, (str(device) + '_median_blur' + str(ksize) + '.png'))
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
  ix,iy= np.shape(img)
  size1=ix,iy,3
  background=np.zeros(size1, dtype=np.uint8)
  
  # Find contours
  contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
  #cv2.drawContours(background,contours,-1, (255,0,0),5, lineType=8,hierarchy=hierarchy)
  #print_image(background, str(device) + '_fillcheck'+ '.png')
  
  # Loop through contours, fill contours less than or equal to size in area
  for c,cnt in enumerate(contours):
    #if hierarchy[0][c][0]==-1:
      m = cv2.moments(cnt)
      area = m['m00']
      if area<=size:
        #cv2.fillPoly(img, pts = cnt, color=(0,0,0))
        cv2.drawContours(img,contours,c, (0,0,0),-1, lineType=8,hierarchy=hierarchy)
  if debug:
    print_image(img, (str(device) + '_fill' + str(size) + '.png'))

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
    print_image(img_inv, (str(device) + '_invert.png'))
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
    print_image(merged, (str(device) + '_and_joined.png'))
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
    print_image(merged, (str(device) + '_or_joined.png'))
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
    print_image(merged, (str(device) + '_xor_joined.png'))
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
      print_image(white_masked, (str(device) + '_wmasked.png'))
    return device, white_masked
  elif mask_color=='black':
    masked_img= cv2.bitwise_and(img,img, mask = mask)
    if debug:
      print_image(masked_img, (str(device) + '_bmasked.png'))
    return device, masked_img
  else:
      fatal_error('Mask Color' + str(mask_color) + ' is not "white" or "black"!')

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
  for i,cnt in enumerate(objects):
     cv2.drawContours(img,objects,i, color_palette(1)[0],-1, lineType=8,hierarchy=hierarchy)
  if debug:
    print_image(img, (str(device) + '_id_objects.png'))
  
  return device, objects, hierarchy

### View and Adjust ROI
def define_roi(img, shape, device, roi=None, roi_input='default', debug=False, adjust=False, x_adj=0, y_adj=0, w_adj=0, h_adj=0, ):
  # img = img to overlay roi 
  # roi =default (None) or user input ROI image, object area should be white and background should be black, has not been optimized for more than one ROI
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
  ix,iy,iz=np.shape(img)
  
  #Allows user to use the default ROI or input their own RGB or binary image (made with imagej or some other program) as a base ROI (that can be adjusted below)
  if roi_input== 'rgb':
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    ret,v_img = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY)
    roi_contour,hierarchy = cv2.findContours(v_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
  elif roi_input== 'binary':
    roi_contour,hierarchy = cv2.findContours(rois,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)  
  elif roi_input=='default':
    size = ix,iy
    roi_background = np.zeros(size, dtype=np.uint8)
    roi_size=(ix-5),(iy-5)
    roi=np.zeros(roi_size, dtype=np.uint8)
    roi1=roi+1
    roi_contour,roi_heirarchy=cv2.findContours(roi1,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(roi_background,roi_contour[0],-1, (255,0,0),5)
    if adjust==True:
      if x_adj>0 and w_adj>=0:
        fatal_error('Adjusted ROI position is out of frame, this will cause problems in detecting objects')
      elif y_adj>0 and h_adj>=0:
        fatal_error('Adjusted ROI position is out of frame, this will cause problems in detecting objects')
      elif x_adj<0 or y_adj<0:
        fatal_error('Adjusted ROI position is out of frame, this will cause problems in detecting objects')
  else:
    fatal_error('ROI Input' + str(roi_input) + ' is not "binary", "rgb" or "default roi"!')
    
  #If the ROI is exactly in the 'correct' position 
  if adjust==False:    
    for cnt in roi_contour:
      size = ix,iy,3
      background = np.zeros(size, dtype=np.uint8)
      if shape=='rectangle':
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(background,(x,y),(x+w,y+h),(0,255,0),5)
        rect = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
        rect_contour,hierarchy = cv2.findContours(rect,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(ori_img,rect_contour[0],-1, (255,0,0),5)
        if debug:
          print_image(ori_img, (str(device) + '_roi.png'))
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
            print_image(ori_img, (str(device) + '_roi.png'))
          return device, circle_contour, hierarchy
        else:
          radius = int(h/2)
          cv2.circle(background,center,radius,(255,255,255),-1)
          circle = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
          circle_contour,hierarchy = cv2.findContours(circle,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
          cv2.drawContours(ori_img,circle_contour[0],-1, (255,0,0),5)
          if debug:
            print_image(ori_img, (str(device) + '_roi.png'))
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
            print_image(ori_img, (str(device) + '_roi.png'))
          return device, ellipse_contour, hierarchy
        else:
          cv2.ellipse(ori_img,center,(h/2,w/2),0,0,360, (0,255,0), 2)
          cv2.ellipse(background,center,(h/2,w/2),0,0,360, (0,255,0), 2)
          ellipse = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
          ellipse_contour,hierarchy = cv2.findContours(ellipse,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
          cv2.drawContours(ori_img,ellipse_contour[0],-1, (255,0,0),5)
          if debug:
            print_image(ori_img, (str(device) + '_roi.png'))
          return device, ellipse_contour, hierarchy
      else:
          fatal_error('Shape' + str(shape) + ' is not "rectangle", "circle", or "ellipse"!')
          
   #If the user wants to change the size of the ROI or adjust ROI position   
  if adjust==True:
    sys.stderr.write('WARNING: Make sure ROI is COMPLETELY in frame or object detection will not perform properly\n')
    if x_adj==0 and y_adj==0 and w_adj==0 and h_adj==0:
      fatal_error( 'If adjust is true then x_adj, y_adj, w_adj or h_adj must have a non-zero value')
    else:
      for cnt in roi_contour:
        size = ix,iy, 3
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
            print_image(ori_img, (str(device) + '_roi.png'))
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
              print_image(ori_img, (str(device) + '_roi.png'))
            return device, circle_contour, hierarchy
          else:
            radius = int(h1/2)
            cv2.circle(background,center,radius,(255,255,255),-1)
            circle = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
            circle_contour,hierarchy = cv2.findContours(circle,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(ori_img,circle_contour[0],-1, (255,0,0),5)
            if debug:
              print_image(ori_img, (str(device) + '_roi.png'))
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
              print_image(ori_img, (str(device) + '_roi.png'))
            return device, ellipse_contour, hierarchy
          else:
            cv2.ellipse(background,center,(h1/2,w1/2),0,0,360, (0,255,0), 2)
            ellipse = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
            ellipse_contour,hierarchy = cv2.findContours(ellipse,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(ori_img,ellipse_contour[0],-1, (255,0,0),5)
            if debug:
              print_image(ori_img, (str(device) + '_roi.png'))
            return device, ellipse_contour, hierarchy
        else:
            fatal_error('Shape' + str(shape) + ' is not "rectangle", "circle", or "ellipse"!')
        
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
  ix,iy,iz=np.shape(img)
  size = ix,iy,3
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
    fatal_error('ROI Type' + str(roi_type) + ' is not "cutto" or "partial"!')
  
  if debug:
    print_image(w_back, (str(device) + '_roi_objects.png'))
    print_image(ori_img, (str(device) + '_obj_on_img.png'))
    print_image(mask, (str(device) + '_roi_mask.png'))
    #print ('Object Area=', obj_area)
  
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
    for cnt in contours:
      cv2.drawContours(ori_img, cnt, -1, (255,0,0), 4)
      cv2.drawContours(ori_img, group, -1, (255,0,0), 4)
    print_image(ori_img, (str(device) + '_objcomp.png'))
    print_image(ori_img, (str(device) + '_objcomp_mask.png'))
  return device, group, mask


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
      
### Analyzes an object and outputs numeric properties
def analyze_object(img,imgname,obj, mask, device, debug=False,filename=False):
  # Outputs numeric properties for an input object (contour or grouped contours)
  # Also color classification?
  # img = image object (most likely the original), color(RGB)
  # imgname= name of image
  # obj = single or grouped contour object
  # device = device number. Used to count steps in the pipeline
  # debug= True/False. If True, print image
  # filename= False or image name. If defined print image
  device += 1
  ori_img=np.copy(img)
  ix,iy,iz=np.shape(img)
  size = ix,iy,3
  size1 = ix,iy
  background = np.zeros(size, dtype=np.uint8)
  background1 = np.zeros(size1, dtype=np.uint8)
  background2 = np.zeros(size1, dtype=np.uint8)
  
  # Check is object is touching image boundaries (QC)
  frame_background = np.zeros(size1, dtype=np.uint8)
  frame=frame_background+1
  frame_contour,frame_heirarchy=cv2.findContours(frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
  ptest=[]
  vobj=np.vstack(obj)
  for i,c in enumerate(vobj):
      xy=tuple(c)
      pptest=cv2.pointPolygonTest(frame_contour[0],xy, measureDist=False)
      ptest.append(pptest)
  in_bounds=all(c==1 for c in ptest)
    
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
    
    #Longest Axis: line through center of mass and point on the convex hull that is furthest away
    cv2.circle(background, (int(cmx),int(cmy)), 4, (255,255,255),-1)
    center_p = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    ret,centerp_binary = cv2.threshold(center_p, 0, 255, cv2.THRESH_BINARY)
    centerpoint,cpoint_h = cv2.findContours(centerp_binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    
    dist=[]
    vhull=np.vstack(hull)
    
    for i,c in enumerate(vhull):
      xy=tuple(c)
      pptest=cv2.pointPolygonTest(centerpoint[0],xy, measureDist=True)
      dist.append(pptest)
    
    abs_dist=np.absolute(dist)
    max_i=np.argmax(abs_dist)
    
    caliper_max=list(tuple(vhull[max_i]))
    caliper_mid=[int(cmx),int(cmy)]
    
    caliper_points=np.array([caliper_max, caliper_mid])
    
    [vx,vy,x1,y1] = cv2.fitLine(caliper_points,cv2.cv.CV_DIST_L2,0,0.01,0.01)
    lefty = int((-x1*vy/vx) + y1)
    righty = int(((mask.shape[1]-x1)*vy/vx)+y1)
    cv2.line(background1,(mask.shape[1]-1,righty),(0,lefty),(255),5)
    ret1,line_binary = cv2.threshold(background1, 0, 255, cv2.THRESH_BINARY)
    #print_image(line_binary,(str(device)+'_caliperfit.png'))
    
    cv2.drawContours(background2, [hull], -1, (255), -1)
    ret2,hullp_binary = cv2.threshold(background2, 0, 255, cv2.THRESH_BINARY)
    #print_image(hullp_binary,(str(device)+'_hull.png'))
    
    caliper=cv2.multiply(line_binary,hullp_binary)    
    #print_image(caliper,(str(device)+'_caliperlength.png'))
    
    caliper_y,caliper_x=np.array(caliper.nonzero())
    caliper_matrix=np.vstack((caliper_x,caliper_y))
    caliper_transpose=np.transpose(caliper_matrix)
    caliper_length=len(caliper_transpose)
    
    
  else:
    hull_area, solidity, perimeter, width, height, cmx, cmy = 'ND', 'ND', 'ND', 'ND', 'ND', 'ND', 'ND'
      
  #Store Shape Data
  shape_header=('area','hull-area','solidity','perimeter','width','height','longest_axis','center-of-mass-x', 'center-of-mass-y', 'in_bounds')
  data = {
    'area' : area,
    'hull_area' : hull_area,
    'solidity' : solidity,
    'perimeter' : perimeter,
    'width' : width,
    'height' : height,
    'longest_axis': caliper_length,
    'center_mass_x' : cmx,
    'center_mass_y' : cmy,
    'in_bounds': in_bounds
  }
  
  shape_data = (
    data['area'],
    data['hull_area'],
    data['solidity'],
    data['perimeter'],
    data['width'],
    data['height'],
    data['longest_axis'],
    data['center_mass_x'],
    data['center_mass_y'],
    data['in_bounds']
    )
      
  # Draw properties
  if area and filename:
    cv2.drawContours(ori_img, obj, -1, (255,0,0), 2)
    cv2.drawContours(ori_img, [hull], -1, (0,0,255), 3)
    cv2.line(ori_img, (x,y), (x+width,y), (0,0,255), 3)
    cv2.line(ori_img, (int(cmx),y), (int(cmx),y+height), (0,0,255), 3)
    cv2.line(ori_img,(tuple(caliper_transpose[caliper_length-1])),(tuple(caliper_transpose[0])),(0,0,255),3)
    cv2.circle(ori_img, (int(cmx),int(cmy)), 10, (0,0,255), 3)
    print_image(ori_img,(filename + '_shapes.png'))
  else:
    pass
  
  if debug:
    cv2.drawContours(ori_img, obj, -1, (255,0,0), 2)
    cv2.drawContours(ori_img, [hull], -1, (0,0,255), 3)
    cv2.line(ori_img, (x,y), (x+width,y), (0,0,255), 3)
    cv2.line(ori_img, (int(cmx),y), (int(cmx),y+height), (0,0,255), 3)
    cv2.line(ori_img,(tuple(caliper_transpose[caliper_length-1])),(tuple(caliper_transpose[0])),(0,0,255),3)
    cv2.circle(ori_img, (int(cmx),int(cmy)), 10, (0,0,255), 3)
    print_image(ori_img,(str(device)+'_shapes.png'))
 
  return device, shape_header, shape_data, ori_img
    
### Analyze Color of Object
def analyze_color(img, imgname, mask,bins,device,debug=False,hist_plot_type='all',cslice_type='rgb',pseudo_channel='v',filename=False):
  # img = image
  # imgname = name of input image
  # mask = mask made from selected contours
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print data and histograms
  # hist_plot_type= 'None', 'all', 'rgb','lab' or 'hsv'
  # color_slice_type = 'None', 'rgb', 'hsv' or 'lab'
  # pseudo_channel= 'None', 'l', 'm' (green-magenta), 'y' (blue-yellow), h','s', or 'v', creates pseduocolored image based on the specified channel
  # filename= False or image name. If defined print image
  
  device += 1
  ix,iy,iz=np.shape(img)
  size = ix,iy
  background = np.zeros(size, dtype=np.uint8)
  w_back=background+255
  ori_img=np.copy(img)
  
  masked=cv2.bitwise_and(img,img, mask=mask)
  b,g,r=cv2.split(masked)
  lab = cv2.cvtColor(masked, cv2.COLOR_BGR2LAB)
  l,m,y=cv2.split(lab)
  hsv = cv2.cvtColor(masked, cv2.COLOR_BGR2HSV)
  h,s,v=cv2.split(hsv)
  
  channel=(b,g,r,l,m,y,h,s,v)
  graph_color=('blue','forestgreen','red','dimgray','magenta','yellow','blueviolet','cyan','orange' )
  label=('blue','green','red', 'lightness','green-magenta','blue-yellow','hue','saturation', 'value')

  # Create Color Histogram Data
  b_bin=b/(256/bins)
  g_bin=g/(256/bins)
  r_bin=r/(256/bins)
  l_bin=l/(256/bins)
  m_bin=m/(256/bins)
  y_bin=y/(256/bins)
  h_bin=h/(256/bins)
  s_bin=s/(256/bins)
  v_bin=v/(256/bins)
  
  hist_b= cv2.calcHist([b_bin],[0],mask,[bins], [0,(bins-1)])
  hist_g= cv2.calcHist([g_bin],[0],mask,[bins], [0,(bins-1)])
  hist_r= cv2.calcHist([r_bin],[0],mask,[bins], [0,(bins-1)])
  hist_l= cv2.calcHist([l_bin],[0],mask,[bins], [0,(bins-1)])
  hist_m= cv2.calcHist([m_bin],[0],mask,[bins], [0,(bins-1)])
  hist_y= cv2.calcHist([y_bin],[0],mask,[bins], [0,(bins-1)])
  hist_h= cv2.calcHist([h_bin],[0],mask,[bins], [0,(bins-1)])
  hist_s= cv2.calcHist([s_bin],[0],mask,[bins], [0,(bins-1)])
  hist_v= cv2.calcHist([v_bin],[0],mask,[bins], [0,(bins-1)])

  hist_data_b=[l[0] for l in hist_b]
  hist_data_g=[l[0] for l in hist_g]
  hist_data_r=[l[0] for l in hist_r]
  hist_data_l=[l[0] for l in hist_l]
  hist_data_m=[l[0] for l in hist_m]
  hist_data_y=[l[0] for l in hist_y]
  hist_data_h=[l[0] for l in hist_h]
  hist_data_s=[l[0] for l in hist_s]
  hist_data_v=[l[0] for l in hist_v]
    
  
  #Store Color Histogram Data
  hist_header=('bin-number','blue','green','red', 'lightness','green-magenta','blue-yellow','hue','saturation', 'value')
  data={
    'bin-number': bins,
    'blue': hist_data_b,
    'green':hist_data_g,
    'red':hist_data_r,
    'lightness':hist_data_l,
    'green-magenta':hist_data_m,
    'blue-yellow':hist_data_y,
    'hue': hist_data_h,
    'saturation':hist_data_s,
    'value':hist_data_v  
    }
  
  hist_data= (
    data['bin-number'],
    data['blue'],
    data['green'],
    data['red'],
    data['lightness'],
    data['green-magenta'],
    data['blue-yellow'],
    data['hue'],
    data['saturation'],
    data['value']
    )
  
  
  # Create Histogram Plot
  if filename:
    if hist_plot_type=='all':
      hist_plotb=plt.plot(hist_b,color=graph_color[0],label=label[0])
      hist_plotg=plt.plot(hist_g,color=graph_color[1],label=label[1])
      hist_plotr= plt.plot(hist_r,color=graph_color[2],label=label[2])
      hist_plotl=plt.plot(hist_l,color=graph_color[3],label=label[3])
      hist_plotm= plt.plot(hist_m,color=graph_color[4],label=label[4])
      hist_ploty=plt.plot(hist_y,color=graph_color[5],label=label[5])
      hist_ploth=plt.plot(hist_h,color=graph_color[6],label=label[6])
      hist_plots= plt.plot(hist_s,color=graph_color[7],label=label[7])
      hist_plotv=plt.plot(hist_v,color=graph_color[8],label=label[8])
      xaxis=plt.xlim([0,(bins-1)])
      legend=plt.legend()
      fig_name=(filename +'_' + str(hist_plot_type) + '_hist.png')
      plt.savefig(fig_name)
      if debug:
        fig_name=(str(device) +'_' + str(hist_plot_type) + '_hist.png')
        plt.savefig(fig_name)
      plt.clf()
    elif hist_plot_type=='rgb':
      hist_plotb=plt.plot(hist_b,color=graph_color[0],label=label[0])
      hist_plotg=plt.plot(hist_g,color=graph_color[1],label=label[1])
      hist_plotr= plt.plot(hist_r,color=graph_color[2],label=label[2])
      xaxis=plt.xlim([0,(bins-1)])
      legend=plt.legend()
      fig_name=(filename +'_' + str(hist_plot_type) + '_hist.png')
      plt.savefig(fig_name)
      plt.clf()
    elif hist_plot_type=='lab':
      hist_plotl=plt.plot(hist_l,color=graph_color[3],label=label[3])
      hist_plotm= plt.plot(hist_m,color=graph_color[4],label=label[4])
      hist_ploty=plt.plot(hist_y,color=graph_color[5],label=label[5])
      xaxis=plt.xlim([0,(bins-1)])
      legend=plt.legend()
      fig_name=(filename +'_' + str(hist_plot_type) + '_hist.png')
      plt.savefig(fig_name)
      if debug:
        fig_name=(str(device) +'_' + str(hist_plot_type) + '_hist.png')
        plt.savefig(fig_name)
      plt.clf()
    elif hist_plot_type=='hsv':
      hist_ploth=plt.plot(hist_h,color=graph_color[6],label=label[6])
      hist_plots= plt.plot(hist_s,color=graph_color[7],label=label[7])
      hist_plotv=plt.plot(hist_v,color=graph_color[8],label=label[8])
      xaxis=plt.xlim([0,(bins-1)])
      legend=plt.legend()
      fig_name=(filename +'_' + str(hist_plot_type) + '_hist.png')
      plt.savefig(fig_name)
      if debug:
        fig_name=(str(device) +'_' + str(hist_plot_type) + '_hist.png')
        plt.savefig(fig_name)
      plt.clf()
    elif hist_plot_type==None:
      pass
    else:
      fatal_error('Histogram Plot Type' + str(hist_plot_type) + ' is not "none", "all","rgb", "lab" or "hsv"!')
    
  # Generate Color Slice: Get Flattened RGB, LAB or HSV Histogram for Visualization     
  if cslice_type==None:
    pass
  elif cslice_type=='rgb':
    b_stack = np.vstack(hist_b)
    g_stack= np.vstack(hist_g)
    r_stack = np.vstack(hist_r)
  
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
    
    norm_slice=np.dstack((b_norm,g_norm,r_norm))

  elif cslice_type=='hsv':
    h_stack = np.vstack(hist_h)
    s_stack= np.vstack(hist_s)
    v_stack = np.vstack(hist_v)
  
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
    
    norm_slice=np.dstack((h_norm,s_norm,v_norm))

  elif cslice_type=='lab':
    l_stack = np.vstack(hist_l)
    m_stack= np.vstack(hist_m)
    y_stack = np.vstack(hist_y)
  
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
    
    norm_slice=np.dstack((l_norm,m_norm,y_norm))
    
  else:
    fatal_error('Visualize Type' + str(visualize_type) + ' is not "None", "rgb","hsv" or "lab"!')
  
  if filename:
    print_image(norm_slice, (filename + '_'+ str(cslice_type)+ '_norm_slice.png'))
  else:
    pass
  
  if debug:
    print_image(norm_slice, (str(device)+ '_'+ str(cslice_type)+ '_norm_slice.png'))

  # PseudoColor Image Based On l,A,B, H, S, or V Channel
  
  p_channel=pseudo_channel
  pseudocolor_img=1
  
  if pseudo_channel==None:
    pass
  
  elif p_channel=='h':
        
    h_img =plt.imshow(h_bin, vmin=0,vmax=(bins-1), cmap=cm.jet)
    bar=plt.colorbar(orientation='horizontal')
    mask_inv=cv2.bitwise_not(mask)
    img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pot=cv2.bitwise_and(img_gray,img_gray,mask=mask_inv)
    pot_img=cv2.add(pot,mask)
    pot_rgba=np.dstack((pot_img,pot_img,pot_img,mask_inv))
    my_cmap = plt.get_cmap('binary_r')
    pot_img1 =plt.imshow(pot_rgba, cmap=my_cmap)
    plt.axis('off')
    fig_name=(filename +'_' + str(pseudo_channel) + '_pseduo_on_img.png')
    plt.savefig(fig_name)
    if debug:
      fig_name=(str(device) +'_' + str(pseudo_channel) + '_pseduo_on_img.png')
      plt.savefig(fig_name)
    plt.clf()
    
    h_img =plt.imshow(h_bin, vmin=0,vmax=(bins-1), cmap=cm.jet)
    bar=plt.colorbar(orientation='horizontal')
    white_rgba=np.dstack((w_back,w_back,w_back,mask_inv))
    pot_img1 =plt.imshow(white_rgba, cmap=my_cmap)
    plt.axis('off')
    fig_name=(filename +'_' + str(pseudo_channel) + '_pseduo_on_white.png')
    plt.savefig(fig_name)
    if debug:
      fig_name=(str(device) +'_' + str(pseudo_channel) + '_pseduo_on_white.png')
      plt.savefig(fig_name)
    plt.clf()
    
  elif p_channel=='s':
    
    s_img =plt.imshow(s_bin, vmin=0,vmax=(bins-1), cmap=cm.jet)
    bar=plt.colorbar(orientation='horizontal')
    mask_inv=cv2.bitwise_not(mask)
    img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pot=cv2.bitwise_and(img_gray,img_gray,mask=mask_inv)
    pot_img=cv2.add(pot,mask)
    pot_rgba=np.dstack((pot_img,pot_img,pot_img,mask_inv))
    my_cmap = plt.get_cmap('binary_r')
    pot_img1 =plt.imshow(pot_rgba, cmap=my_cmap)
    plt.axis('off')
    fig_name=(filename +'_' + str(pseudo_channel) + '_pseduo_on_img.png')
    plt.savefig(fig_name)
    if debug:
      fig_name=(str(device) +'_' + str(pseudo_channel) + '_pseduo_on_img.png')
      plt.savefig(fig_name)
    plt.clf()
    
    s_img =plt.imshow(s_bin, vmin=0,vmax=(bins-1), cmap=cm.jet)
    bar=plt.colorbar(orientation='horizontal')
    white_rgba=np.dstack((w_back,w_back,w_back,mask_inv))
    pot_img1 =plt.imshow(white_rgba, cmap=my_cmap)
    plt.axis('off')
    fig_name=(filename +'_' + str(pseudo_channel) + '_pseduo_on_white.png')
    plt.savefig(fig_name)
    if debug:
      fig_name=(str(device) +'_' + str(pseudo_channel) + '_pseduo_on_white.png')
      plt.savefig(fig_name)
    plt.clf()
    
  elif p_channel=='v':
    
    v_img =plt.imshow(v_bin, vmin=0,vmax=(bins-1), cmap=cm.jet)
    bar=plt.colorbar(orientation='horizontal')
    mask_inv=cv2.bitwise_not(mask)
    img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pot=cv2.bitwise_and(img_gray,img_gray,mask=mask_inv)
    pot_img=cv2.add(pot,mask)
    pot_rgba=np.dstack((pot_img,pot_img,pot_img,mask_inv))
    my_cmap = plt.get_cmap('binary_r')
    pot_img1 =plt.imshow(pot_rgba, cmap=my_cmap)
    plt.axis('off')
    fig_name=(filename +'_' + str(pseudo_channel) + '_pseduo_on_img.png')
    plt.savefig(fig_name)
    if debug:
      fig_name=(str(device) +'_' + str(pseudo_channel) + '_pseduo_on_img.png')
      plt.savefig(fig_name)
    plt.clf()
    
    v_img =plt.imshow(v_bin, vmin=0,vmax=(bins-1), cmap=cm.jet)
    bar=plt.colorbar(orientation='horizontal')
    white_rgba=np.dstack((w_back,w_back,w_back,mask_inv))
    pot_img1 =plt.imshow(white_rgba, cmap=my_cmap)
    plt.axis('off')
    fig_name=(filename +'_' + str(pseudo_channel) + '_pseduo_on_white.png')
    plt.savefig(fig_name)
    if debug:
      fig_name=(str(device) +'_' + str(pseudo_channel) + '_pseduo_on_white.png')
      plt.savefig(fig_name)
    plt.clf()
    
  elif p_channel=='l':
    
    l_img =plt.imshow(l_bin, vmin=0,vmax=(bins-1), cmap=cm.jet)
    bar=plt.colorbar(orientation='horizontal')
    mask_inv=cv2.bitwise_not(mask)
    img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pot=cv2.bitwise_and(img_gray,img_gray,mask=mask_inv)
    pot_img=cv2.add(pot,mask)
    pot_rgba=np.dstack((pot_img,pot_img,pot_img,mask_inv))
    my_cmap = plt.get_cmap('binary_r')
    pot_img1 =plt.imshow(pot_rgba, cmap=my_cmap)
    plt.axis('off')
    fig_name=(filename +'_' + str(pseudo_channel) + '_pseduo_on_img.png')
    plt.savefig(fig_name)
    if debug:
      fig_name=(str(device) +'_' + str(pseudo_channel) + '_pseduo_on_img.png')
      plt.savefig(fig_name)
    plt.clf()
    
    l_img =plt.imshow(l_bin, vmin=0,vmax=(bins-1), cmap=cm.jet)
    bar=plt.colorbar(orientation='horizontal')
    white_rgba=np.dstack((w_back,w_back,w_back,mask_inv))
    pot_img1 =plt.imshow(white_rgba, cmap=my_cmap)
    plt.axis('off')
    fig_name=(filename +'_' + str(pseudo_channel) + '_pseduo_on_white.png')
    plt.savefig(fig_name)
    if debug:
      fig_name=(str(device) +'_' + str(pseudo_channel) + '_pseduo_on_white.png')
      plt.savefig(fig_name)
    plt.clf()
    
  elif p_channel=='m':
    
    m_img =plt.imshow(m_bin, vmin=0,vmax=(bins-1), cmap=cm.jet)
    bar=plt.colorbar(orientation='horizontal')
    mask_inv=cv2.bitwise_not(mask)
    img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pot=cv2.bitwise_and(img_gray,img_gray,mask=mask_inv)
    pot_img=cv2.add(pot,mask)
    pot_rgba=np.dstack((pot_img,pot_img,pot_img,mask_inv))
    my_cmap = plt.get_cmap('binary_r')
    pot_img1 =plt.imshow(pot_rgba, cmap=my_cmap)
    plt.axis('off')
    fig_name=(filename +'_' + str(pseudo_channel) + '_pseduo_on_img.png')
    plt.savefig(fig_name)
    if debug:
      fig_name=(str(device) +'_' + str(pseudo_channel) + '_pseduo_on_img.png')
      plt.savefig(fig_name)
    plt.clf()
    
    m_img =plt.imshow(m_bin, vmin=0,vmax=(bins-1), cmap=cm.jet)
    bar=plt.colorbar(orientation='horizontal')
    white_rgba=np.dstack((w_back,w_back,w_back,mask_inv))
    pot_img1 =plt.imshow(white_rgba, cmap=my_cmap)
    plt.axis('off')
    fig_name=(filename +'_' + str(pseudo_channel) + '_pseduo_on_white.png')
    plt.savefig(fig_name)
    if debug:
      fig_name=(str(device) +'_' + str(pseudo_channel) + '_pseduo_on_white.png')
      plt.savefig(fig_name)
    plt.clf()
    
  elif p_channel=='y':
    
    y_img =plt.imshow(y_bin, vmin=0,vmax=(bins-1), cmap=cm.jet)
    bar=plt.colorbar(orientation='horizontal')
    mask_inv=cv2.bitwise_not(mask)
    img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pot=cv2.bitwise_and(img_gray,img_gray,mask=mask_inv)
    pot_img=cv2.add(pot,mask)
    pot_rgba=np.dstack((pot_img,pot_img,pot_img,mask_inv))
    my_cmap = plt.get_cmap('binary_r')
    pot_img1 =plt.imshow(pot_rgba, cmap=my_cmap)
    plt.axis('off')
    fig_name=(filename +'_' + str(pseudo_channel) + '_pseduo_on_img.png')
    plt.savefig(fig_name)
    if debug:
      fig_name=(str(device) +'_' + str(pseudo_channel) + '_pseduo_on_img.png')
      plt.savefig(fig_name)
    plt.clf()
    
    y_img =plt.imshow(y_bin, vmin=0,vmax=(bins-1), cmap=cm.jet)
    bar=plt.colorbar(orientation='horizontal')
    white_rgba=np.dstack((w_back,w_back,w_back,mask_inv))
    pot_img1 =plt.imshow(white_rgba, cmap=my_cmap)
    plt.axis('off')
    fig_name=(filename +'_' + str(pseudo_channel) + '_pseduo_on_white.png')
    plt.savefig(fig_name)
    if debug:
      fig_name=(str(device) +'_' + str(pseudo_channel) + '_pseduo_on_white.png')
      plt.savefig(fig_name)
    plt.clf()
  
  else:
    fatal_error('Pseudocolor Channel' + str(pseudo_channel) + ' is not "None", "l","m", "y", "h","s" or "v"!')
  
  return device, hist_header, hist_data, norm_slice

### Print Numerical Data 
def print_results(filename, header, data):
  print '\t'.join(map(str, header))
  print '\t'.join(map(str, data))
    
    
###



