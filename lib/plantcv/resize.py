import cv2
import numpy as np
from . import print_image
from . import fatal_error

def resize(img, resize_x, resize_y, device,debug=False):
# img = image to resize
# resize_x = scaling factor
# resize_y = scaling factor
# device = device counter
# debug = if true prints images
  device += 1
    
  reimg=cv2.resize(img,(0,0),fx=resize_x,fy=resize_y)
  
  if resize_x<=0 and resize_y<=0:
    fatal_error("Resize values both cannot be 0 or negative values!")

  if debug:
    print_image(reimg,(str(device)+"_resize.png"))
  
  return device, reimg