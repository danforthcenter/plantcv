#### Binary image adaptive threshold

import cv2
from . import print_image
from . import fatal_error

	# Creates a binary image from a grayscaled image using adaptive thresholding
	# img = img object, grayscale
	# maxValue = value to apply above threshold (usually 255 = white)
	# thres_type is the type for thresholding (gaussian or mean)
  	# object_type = light or dark
  	# If object is light then standard thresholding is done
  	# If object is dark then inverse thresholding is done
  	# device = device number. Used to count steps in the pipeline
  	# debug = True/False. If True, print image
def adaptive_threshold(img,maxValue,thres_type,object_type,device,debug=False):
	device += 1

	thres = 0
	#check to see which type of adaptive threshold to use
	if thres_type == 'mean':
		thres = cv2.ADAPTIVE_THRESH_MEAN_C
	elif thres_type == 'gaussian':
		thres = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
	else:
		fatal_error('threshold type ' + str(thres_type) + ' is not "mean" or "gaussian"!')

	# check whether to invert the image or not and make an ending extension
	obj = 0
	ext = ''
	if object_type == 'light':
		ext = '.png'
		obj = cv2.THRESH_BINARY
	elif object_type == 'dark':
		ext = '_inv.png'
		obj = cv2.THRESH_BINARY_INV 
	else:
		fatal_error('Object type ' + str(object_type) + ' is not "light" or "dark"!')

	# threshold the image based on the thres_type and object_type
	t_img = cv2.adaptiveThreshold(img,maxValue,thres,obj,11,2)

	# print out the image if the debug is true
	if debug:
		name = str(device) + '_adaptive_threshold' + thres_type + ext
		print_image(t_img, name)

	return device,t_img

