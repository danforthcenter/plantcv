### Sobel filtering
def sobel_filter(img, dx, dy, k, scale, device, debug):
  # This is a filtering method used to identify and highlight gradient edges/features using the 1st derivative
  # Typically used to identify gradients along the x-axis (dx = 1, dy = 0) and y-axis (dx = 0, dy = 1) independently
  # Performance is quite similar to Scharr filter
  # Used to detect edges / changes in pixel intensity 
  # img = image
  # dx = derivative of x to analyze (1-3)
  # dy = derivative of x to analyze (1-3)
  # k = specifies the size of the kernel (must be an odd integer: 1,3,5...)
  # scale = scaling factor applied (multiplied) to computed Sobel values (scale = 1 is unscaled)
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True; print output image
  # ddepth = -1 specifies that the dimensions of output image will be the same as the input image
  sb_img = cv2.Sobel(src = img, ddepth = -1, dx = dx, dy = dy, ksize = k)
  device += 1
  if debug:
    print_image(sb_img, str(device) + '_sb_img' + '_dx_' + str(dx) + '_dy_' + str(dy) + '_k_' + str(k) +'.png')
  return device, sb_img