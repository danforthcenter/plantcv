### Erosion filter

import cv2
from . import print_image

def erode(img, kernel, i, device, debug):
  # Perform morphological 'erosion' filtering. Keeps pixel in center of the kernel if conditions set in kernel are true, otherwise removes pixel. 
  # img = input image
  # kernel = filtering window, you'll need to make your own using as such:  kernal = np.zeros((x,y), dtype=np.uint8), then fill the kernal with appropriate values
  # i = interations, i.e. number of consecutive filtering passes
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True; print output image
  er_img = cv2.erode(src = img, kernel = kernel, iterations = i)
  device += 1
  if debug:
    print_image(er_img, str(device) + '_er_image_' + 'itr_' + str(i) + '.png')
  return device, er_img