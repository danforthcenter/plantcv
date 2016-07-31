### Convert image to 32-bit integer from 8-bit floating point
def image_to_32(img, device, debug):
  # Converts image to a 32-bit integer format from an 8-bit floating point image
  # img = image to convert
  img32 = np.int32(img)
  device += 1
  if debug:
    print_image(img32, str(device) + '_img32' + '.png')
  return device, img32