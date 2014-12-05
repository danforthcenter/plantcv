def _pseudocolored_image(histogram, bins, img, mask, background, channel, filename, resolution):
  # histogram = a normalized histogram of color values from one color channel
  # bins = number of color bins the channel is divided into
  # img = input image
  # mask = binary mask image
  # background = what background image?: channel image (img) or white
  # channel = color channel name
  # filename = input image filename
  # resolution = output image resolution
  
  # Get the image size
  if np.shape(img)[2] == 3:
    ix, iy, iz = np.shape(img)
  else:
    ix, iy = np.shape(img)
  size = ix, iy
  
  plt.imshow(histogram, vmin=0, vmax=(bins - 1), cmap=cm.jet)
  mask_inv = cv2.bitwise_not(mask)
  my_cmap = plt.get_cmap('binary_r')
  
  if background == 'img':
    # Plot pseudocolored plant on the channel image
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pot = cv2.bitwise_and(img_gray, img_gray, mask=mask_inv)
    pot_img = cv2.add(pot, mask)
    pot_rgba = np.dstack((pot_img, pot_img, pot_img, mask_inv))
    plt.imshow(pot_rgba, cmap=my_cmap)
  elif background == 'white':
    # Plot pseudocolored plant on a white background
    # Create white background
    w_back = np.zeros(size, dtype=np.uint8) + 255
    white_rgba = np.dstack((w_back, w_back, w_back, mask_inv))
    plt.imshow(white_rgba, cmap=my_cmap)
  else:
    fatal_error("Background type " + background + " is not a valid type!")

  plt.axis('off')
  
  # Name output file
  fig_name = str(filename[0:-4]) + '_' + str(channel) + '_pseudo_on_' + str(background) + '.png'
  
  # Save image
  plt.savefig(fig_name, dpi=resolution, bbox_inches='tight')
  print('\t'.join(map(str, ('IMAGE', 'pseudo', fig_name))))
  plt.clf()
