import cv2
import numpy as np
from . import print_image
from . import fatal_error


def flip(img,direction,device,debug=False):
# img = image to be flipped
# direction = "horizontal" or "vertical"
# device = device counter
# debug = if true prints image
  if direction=="vertical":
    vh_img=cv2.flip(img,1)
  elif direction=="horizontal":
    vh_img=cv2.flip(img,0)
  else:
    fatal_error(str(direction)+" is not a valid direction, must be horizontal or vertical")
 
  if debug:
    print_image(vh_img,(str(device)+"_flipped.png"))
  
  return device,vh_img