### Join images (OR)

import cv2
from . import print_image

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