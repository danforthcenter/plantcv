### Mask border of image
def border_mask(img, p1, p2, device, debug, color="black"):
  # by using rectangle_mask to mask the edge of plotting regions you end up missing the border of the images by 1 pixel
  # This function fills this region in
  # note that p1 = (0,0) is the top left hand corner bottom right hand corner is p2 = (max-value(x), max-value(y))
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True; print output image
  if color=="black":
    ix, iy = np.shape(img)
    size = ix,iy
    bnk = np.zeros(size, dtype=np.uint8)
    cv2.rectangle(img = bnk, pt1 = p1, pt2 = p2, color = (255,255,255))
    ret, bnk = cv2.threshold(bnk,127,255,0)
    contour,hierarchy = cv2.findContours(bnk,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(bnk, contour, -1 ,(255,255,255), 5)
    device +=1
  if color=="gray":
    ix, iy = np.shape(img)
    size = ix,iy
    bnk = np.zeros(size, dtype=np.uint8)
    cv2.rectangle(img = bnk, pt1 = p1, pt2 = p2, color = (192,192,192))
    ret, bnk = cv2.threshold(bnk,127,255,0)
    contour,hierarchy = cv2.findContours(bnk,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(bnk, contour, -1 ,(192,192,192), 5)
    device +=1
  if debug:
    print_image(bnk, (str(device) + '_brd_mskd_' + '.png'))
  return device, bnk, contour, hierarchy