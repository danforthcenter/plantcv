### RGB -> LAB -> Gray

import cv2
from . import print_image
from . import fatal_error

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
    