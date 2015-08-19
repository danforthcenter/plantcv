### Dilation filter

import cv2
import numpy as np
from . import print_image

def dilate(img, kernel, i, device, debug):
  # Performs morphological 'dilation' filtering. Adds pixel to center of kernel if conditions set in kernel are true.
  # img = input image
  # kernel = filtering window, you'll need to make your own using as such:  kernal = np.zeros((x,y), dtype=np.uint8), then fill the kernal with appropriate values
  # i = interations, i.e. number of consecutive filtering passes
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True; print output image
    kernel1=int(kernel)
    kernel2 = np.ones((kernel1,kernel1),np.uint8)
    dil_img = cv2.dilate(src = img, kernel = kernel2, iterations = i)
    device += 1
    if debug:
        print_image(dil_img, str(device) + '_dil_image_' + 'itr_' + str(i) + '.png')
    return device, dil_img