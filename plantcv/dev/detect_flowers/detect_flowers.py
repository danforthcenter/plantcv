### Analyzes an object and outputs numeric properties

from __future__ import print_function
import cv2
import numpy as np
#from . import print_image
#from . import fatal_error

def detect_flowers(img, imgname, threshold, device, debug=False,filename=False):
  # Outputs numeric properties for an input object (contour or grouped contours)
  # img = image object (most likely the original), color(RGB)
  # imgname = name of image
  # threshold = flower detection threshold
  # device = device number. Used to count steps in the pipeline
  # debug= True/False. If True, print image
  # filename= False or image name. If defined print image
  
  # Code incorporated from: https://github.com/rjcmarkelz/ASPB_Hackathon
  #########
  # Cody Markelz
  # July 28th, 2015
  # markelz@gmail.com
  # github, twitter, bitbucket: rjcmarkelz
  #########
  device += 1

  # Convert original image to the L*a*b* color space for flower detection
  lab_image = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
  l_channel,a_channel,b_channel = cv2.split(lab_image)

  # take a look at the a channel histogram for pot detection, uncomment when finding correct threshold
  hist = cv2.calcHist([b_channel], [0], None, [256], [0, 256])

  blur2 = cv2.bilateralFilter(b_channel, 5, 50, 100)

  (bT, b_thresh_image) = cv2.threshold(blur2, threshold, 256, cv2.THRESH_BINARY)

  # canny edge detection on the thresholded image
  canny_image2 = cv2.Canny(b_thresh_image, 100, 199, apertureSize = 3)

  plants = img.copy()
  (cnts2, _) = cv2.findContours(b_thresh_image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

  cnts2 = sorted(cnts2, key = cv2.contourArea, reverse = True)[:20]

  if len(cnts2) > 2:
    flowers = 'Flowering'
  else:
    flowers = 'Not Flowering' 

  if debug:
    print("I count %d flowers" % (len(cnts2)))
    
    # Loop over each contour and draw a line around it
    for x in range(0, len(cnts2)):
      cv2.drawContours(plants, cnts2, x, (255, 255, 0), 4)
    
    # Output an image with the flower contours labeled and whether or not we think the plant is flowering
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(plants, flowers, (10,150), font, 5,(0,0,255),5)
    cv2.imwrite(str(device) + '_flowering.png', plants)

  flower_header = ('HEADER_FLOWER', 'flowering')
  flower_data = ('FLOWER_DATA', flowers)
  
  return device, flower_header, flower_data
  ######
  # END SCRIPT
  ######