### Scharr filtering
def scharr_filter(img, dX, dY, scale, device, debug):
  # This is a filtering method used to identify and highlight gradient edges/features using the 1st derivative
  # Typically used to identify gradients along the x-axis (dx = 1, dy = 0) and y-axis (dx = 0, dy = 1) independently
  # Performance is quite similar to Sobel filter
  # Used to detect edges / changes in pixel intensity 
  # img = image
  # dx = derivative of x to analyze (1-3)
  # dy = derivative of x to analyze (1-3)
  # scale = scaling factor applied (multiplied) to computed Scharr values (scale = 1 is unscaled)
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True; print output image
  # ddepth = -1 specifies that the dimensions of output image will be the same as the input image
  sr_img = cv2.Scharr(src = img, ddepth = -1, dx = dX, dy = dY, scale = scale)
  device += 1
  if debug:
    print_image(sr_img, str(device) + '_sr_img' + '_dx_' + str(dX) + '_dy_' + str(dY) + '_scale_' + str(scale) + '.png')
  return device, sr_img