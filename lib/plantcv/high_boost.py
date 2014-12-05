### Highboost filtering
def high_boost(img, img_mblur, c, device, debug):
  # High-boost filtering is a method used to sharpen images
  # This method will sharpen regions of high contrast while keeping blurred regions intact
  # See Digital Image Processsing by Gonzalez and Woods
  # img = image for filtering
  # img_mblur = an image subjected to lowpass filtering (median, gaussian, etc.). I like median.
  # c = scaling factor to multiply output array by
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True; print output image
  
  # Get difference between original and smoothed image
  img_sub = np.sub(img, img_blur)
  # Enhance the difference by an appropriate scaling factor (c)
  img_mult = np.multiply(img_sub, c)
  # Sharpen the original image
  img_hb = np.add(img, img_mult)
  device += 1
  if debug:
    print_image(img_hb, str(device) + '_hb_image_' + 'scale_' + str(c) + '.png')
  return device, img_hb