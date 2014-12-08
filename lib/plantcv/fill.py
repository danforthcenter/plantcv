### Object fill device

import numpy as np
import cv2
from . import print_image

def fill(img, mask, size, device, debug=False):
  # Identifies objects and fills objects that are less than size
  # img = image object, grayscale. img will be returned after filling
  # mask = image object, grayscale. This image will be used to identify contours
  # size = minimum object area size in pixels (integer)
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print image
  device += 1
  ix,iy= np.shape(img)
  size1=ix,iy
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