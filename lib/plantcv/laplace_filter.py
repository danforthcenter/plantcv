### Laplace filtering
def laplace_filter(img, k, scale, device, debug):
  # This is a filtering method used to identify and highlight fine edges based on the 2nd derivative
  # A very sensetive method to highlight edges but will also amplify background noise
  # img = input image
  # k = apertures size used to calculate 2nd derivative filter, specifies the size of the kernel (must be an odd integer: 1,3,5...)
  # scale = scaling factor applied (multiplied) to computed Laplacian values (scale = 1 is unscaled)
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True; print output image
  # ddepth = -1 specifies that the dimensions of output image will be the same as the input image
  lp_filtered = cv2.Laplacian(src = img, ddepth = -1, ksize = k, scale = scale)
  device += 1
  if debug:
    print_image(lp_filtered, str(device) + '_lp_out' + '_k_' + str(k) + '_scale_' + str(scale) + '_.png')
  return device, lp_filtered
