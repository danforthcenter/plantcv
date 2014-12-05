### RGB -> HSV -> Gray
def rgb2gray_hsv(img, channel, device, debug=False):
  # Convert image from RGB colorspace to HSV colorspace
  # Returns the specified subchannel as a gray image
  # img = image object, RGB colorspace
  # channel = color subchannel (h = hue, s = saturation, v = value/intensity/brightness)
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print image
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  # Split HSV channels
  h,s,v = cv2.split(hsv)
  device += 1
  if channel == 'h':
    if debug:
      print_image(h, (str(device) + '_hsv_hue.png'))
    return device, h
  elif channel == 's':
    if debug:
      print_image(s, (str(device) + '_hsv_saturation.png'))
    return device, s
  elif channel == 'v':
    if debug:
      print_image(v, (str(device) + '_hsv_value.png'))
    return device, v
  else:
    fatal_error('Channel ' + (str(channel) + ' is not h, s or v!'))