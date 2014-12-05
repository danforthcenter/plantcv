### Convert image to 8-bit
def convertScaleAbs(img, device, debug):
  # Scales, calculates absolute values and converts result to an 8-bit image
  # img = image to convert
  img8 = cv2.convertScaleAbs(img)
  device += 1
  if debug:
    print_image(img8, str(device) + '_img8' + '.png')
  return device, img8