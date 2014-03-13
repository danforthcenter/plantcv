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
      size = 2056,2456, 3
      background = np.zeros(size, dtype=np.uint8)
      if shape=='rectangle':
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(background,(x,y),(x+w,y+h),(0,255,0),5)
        rect = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
        rect_contour,hierarchy = cv2.findContours(rect,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(img,rect_contour[0],-1, (255,0,0),5)
        if debug:
          print_image(img, str(device) + '_roi.png')
        return device, rect_contour, hierarchy
      elif shape== 'circle':
        x,y,w,h = cv2.boundingRect(cnt)
        center = (int(w/2),int(h/2))
        if h>w:
          radius = int(w/2)
          cv2.circle(background,center,radius,(255,255,255),-1)
          circle = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
          circle_contour,hierarchy = cv2.findContours(circle,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
          cv2.drawContours(img,circle_contour[0],-1, (255,0,0),5)
          if debug:
            print_image(img, str(device) + '_roi.png')
          return device, circle_contour, hierarchy
        else:
          radius = int(h/2)
          cv2.circle(background,center,radius,(255,255,255),-1)
          circle = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
          circle_contour,hierarchy = cv2.findContours(circle,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
          cv2.drawContours(img,circle_contour[0],-1, (255,0,0),5)
          if debug:
            print_image(img, str(device) + '_roi.png')
          return device, circle_contour, hierarchy
      elif shape== 'ellipse': 
        x,y,w,h = cv2.boundingRect(cnt)
        center = (int(w/2),int(h/2))
        if w>h:
          cv2.ellipse(background,center,(w/2,h/2),0,0,360, (0,255,0), 2)
          ellipse = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
          ellipse_contour,hierarchy = cv2.findContours(ellipse,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
          cv2.drawContours(img,ellipse_contour[0],-1, (255,0,0),5)
          if debug:
            print_image(img, str(device) + '_roi.png')
          return device, ellipse_contour, hierarchy
        else:
          cv2.ellipse(img,center,(h/2,w/2),0,0,360, (0,255,0), 2)
          cv2.ellipse(background,center,(h/2,w/2),0,0,360, (0,255,0), 2)
          ellipse = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
          ellipse_contour,hierarchy = cv2.findContours(ellipse,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
          cv2.drawContours(img,ellipse_contour[0],-1, (255,0,0),5)
          if debug:
            print_image(img, str(device) + '_roi.png')
          return device, ellipse_contour, hierarchy
      else:
          fatal_error('Shape' + shape + ' is not "rectangle", "circle", or "ellipse"!')
          
  # If the user wants to change the shape of the ROI or adjust ROI size or position   
  if adjust==True:
    if x_adj==0 and y_adj==0 and w_adj==0 and h_adj==0:
      fatal_error( 'If Adjust is True then x_adj, y_adj, w_adj or h_adj must have a non-zero value')
    else:
      for cnt in roi_contour:
        size = 2056,2456, 3
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
          cv2.drawContours(img,rect_contour[0],-1, (255,0,0),5)
          if debug:
            print_image(img, str(device) + '_roi.png')
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
            cv2.drawContours(img,circle_contour[0],-1, (255,0,0),5)
            if debug:
              print_image(img, str(device) + '_roi.png')
            return device, circle_contour, hierarchy
          else:
            radius = int(h1/2)
            cv2.circle(background,center,radius,(255,255,255),-1)
            circle = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
            circle_contour,hierarchy = cv2.findContours(circle,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(img,circle_contour[0],-1, (255,0,0),5)
            if debug:
              print_image(img, str(device) + '_roi.png')
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
            cv2.drawContours(img,ellipse_contour[0],-1, (255,0,0),5)
            if debug:
              print_image(img, str(device) + '_roi.png')
            return device, ellipse_contour, hierarchy
          else:
            cv2.ellipse(background,center,(h1/2,w1/2),0,0,360, (0,255,0), 2)
            ellipse = cv2.cvtColor( background, cv2.COLOR_RGB2GRAY )
            ellipse_contour,hierarchy = cv2.findContours(ellipse,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(img,ellipse_contour[0],-1, (255,0,0),5)
            if debug:
              print_image(img, str(device) + '_roi.png')
            return device, ellipse_contour, hierarchy
        else:
            fatal_error('Shape' + shape + ' is not "rectangle", "circle", or "ellipse"!')
        
  
### Find Objects in Region of Interest and Fill Them
def obj_roi(mask,roi,roi_type,device, debug=False, overlay='no', img=[] ):
  # mask = what is used for object detection
  # roi= region of interest
  # roi_type= region of interest type either 'cut' or 'partial'
  # overlay = either 'yes' or 'no'
  # img = image that the objects will be overlayed (if overlay=no then it will be on white background), if no you must put [] as a place holder.
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print image
  device += 1
  
  size = 2056,2456, 3
  background = np.zeros(size, dtype=np.uint8)
  w_back=background+255
  
  if overlay=='no':
    if roi_type=='cut':
      obj_roi=cv2.multiply(mask,roi)
      obj_roi_contour,hierarchy = cv2.findContours(obj_roi,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
      cv2.drawContours(w_back,obj_roi_contour,-1, (255,0,0),-1)
      if debug:
        print_image(w_back, str(device) + '_roi_objects.png')
      return device, w_back
    else:
      fatal_error('ROI Type' + roi_type + ' is not "cut" or "partial"!')
  elif overlay=='yes':
    if roi_type=='cut':
      obj_roi=cv2.multiply(mask,roi)
      obj_roi_contour,hierarchy = cv2.findContours(obj_roi,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
      cv2.drawContours(img,obj_roi_contour,-1, (255,0,0),-1)
      if debug:
        print_image(img, str(device) + '_roi_objects.png')
      return device, img
    else:
      fatal_error('ROI Type' + roi_type + ' is not "cut" or "partial"!')
  else:
   fatal_error('Overlay' + overlay + ' is not "no" or "yes"!')
   
### Find contours
# Temp method
def find_contours(img, device, debug=False):
  # img = binary image object
  # device = device number. Used to count steps in the pipeline
  # debug= True/False. If True, print image
  device += 1
  
  # Find contours
  contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
 
  return device, contours

### Object composition
def object_composition(img, contours, device, debug=False):
  # Groups objects into a single object, usually done after object filtering
  # contours = object list
  # device = device number. Used to count steps in the pipeline
  # debug= True/False. If True, print image
  device += 1
  
  group = np.vstack(contours)
  if debug:
    #for cnt in contours:
    #  cv2.drawContours(img, cnt, -1, (255,0,0), 2)
    cv2.drawContours(img, [group], -1, (0,0,255), -1)
    print_image(img, str(device) + '_objcomp.png')
  return device, group

      
### Analyzes an object and outputs numeric properties
def analyze_object(img, obj, device, debug=False):
  # Outputs numeric properties for an input object (contour or grouped contours)
  # Also color classification?
  # img = image object (most likely the original), color(RGB)
  # obj = single or grouped contour object
  # device = device number. Used to count steps in the pipeline
  # debug= True/False. If True, print image
  device += 1
  
  # Convex Hull
  hull = cv2.convexHull(obj)
  # Moments
  m = cv2.moments(obj)
  ## Properties
  # Area
  area = m['m00']
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
  if debug:
    cv2.drawContours(img, [hull], -1, (0,255,0), 3)
    cv2.line(img, (x,y), (x+width,y), (255,0,0), 3)
    cv2.line(img, (int(cmx),y), (int(cmx),y+height), (255,0,0), 3)
    cv2.circle(img, (int(cmx),int(cmy)), 10, (0,255,0), 3)
      
  if debug:
    print_image(img, str(device) + '_obj.png')

  return device, data