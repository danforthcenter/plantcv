### Watershed boundry detection function

import cv2
from . import print_image

def watershed(img, marker, device, debug):
  # Uses the watershed algorithm to detect boundry of objects
  # Needs a marker file which specifies area which is object (white), background (grey), unknown area (black)
  # img = image to perform watershed on needs to be 3D (i.e. np.shape = x,y,z not np.shape = x,y)
  # marker = a 32-bit image file that specifies what areas are what (2D, np.shape = x,y)
  cv2.watershed(img, marker)
  device += 1
  if debug:
    print_image(marker, str(device) + 'watershed_img' + '.png')
  return device, marker