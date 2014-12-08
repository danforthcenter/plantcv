### Make masking rectangle

import cv2
import numpy as np
from . import print_image

def rectangle_mask(img, p1, p2, device, debug, color="black"):
  # takes an input image and returns a binary image masked by a rectangular area denoted by p1 and p2
  # note that p1 = (0,0) is the top left hand corner bottom right hand corner is p2 = (max-value(x), max-value(y))
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True; print output image
  # get the dimensions of the input image
  ix, iy = np.shape(img)
  size = ix,iy
  # create a blank image of same size
  bnk = np.zeros(size, dtype=np.uint8)
  # draw a rectangle denoted by pt1 and pt2 on the blank image
  
  if color=="black":
    cv2.rectangle(img = bnk, pt1 = p1, pt2 = p2, color = (255,255,255))
    ret, bnk = cv2.threshold(bnk,127,255,0)
    contour,hierarchy = cv2.findContours(bnk,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    # make sure entire rectangle is within (visable within) plotting region or else it will not fill with thickness = -1
    # note that you should only print the first contour (contour[0]) if you want to fill with thickness = -1
    # otherwise two rectangles will be drawn and the space between them will get filled
    cv2.drawContours(bnk, contour, 0 ,(255,255,255), -1)
    device +=1
  if color=="gray":
    cv2.rectangle(img = bnk, pt1 = p1, pt2 = p2, color = (192,192,192))
    ret, bnk = cv2.threshold(bnk,127,255,0)
    contour,hierarchy = cv2.findContours(bnk,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    # make sure entire rectangle is within (visable within) plotting region or else it will not fill with thickness = -1
    # note that you should only print the first contour (contour[0]) if you want to fill with thickness = -1
    # otherwise two rectangles will be drawn and the space between them will get filled
    cv2.drawContours(bnk, contour, 0 ,(192,192,192), -1)
  if debug:
    print_image(bnk, (str(device) + '_roi.png'))
  return device, bnk, contour, hierarchy