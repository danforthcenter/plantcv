### Shape Tiller Tool
def tiller_count (img,imgname, obj, mask, line_position, device , debug=False, filename=False):
  # img = image
  # imgname = name of input image
  # obj = single or grouped contour object
  # mask = mask made from selected contours
  # line_position = position of boundry line (a value of 0 would draw the line through the bottom of the image)
  # device = device number. Used to count steps in the pipeline
  # debug = True/False. If True, print data.
  # filename = False or image name. If defined print image.
  
  device +=1
  ori_img=np.copy(img)
  ori_mask=np.copy(mask)
  
  # Draw line horizontal line through bottom of image, that is adjusted to user input height
  if len(np.shape(ori_img))==3:
    iy,ix,iz=np.shape(ori_img)
  else:
    iy,ix=np.shape(ori_img)
  size=(iy,ix)
  size1=(iy,ix,3)
  background=np.zeros(size,dtype=np.uint8)
  wback=(np.zeros(size1,dtype=np.uint8))+255
  x_coor=int(ix)
  y_coor=int(iy)-int(line_position)
  line_point1=(1,y_coor-2)
  line_point2=(ix,y_coor-2)
  cv2.line(background,line_point1,line_point2,(255),1)
  
  # find intersection of line and mask image 
  tillers=cv2.bitwise_and(background, ori_mask)
  
  # find objects
  tiller_contour,tiller_hierarchy = cv2.findContours(tillers,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
  cv2.drawContours(ori_img, tiller_contour, -1 ,(0,0,255), -1)
 
  # find the width of each object
  tiller_len=[]
  for i,c in enumerate(tiller_contour):
      tiller_width1=len(c)
      tiller_len.append(tiller_width1)
  tiller_count=len(tiller_len)
  
  tiller_width=[l for l in tiller_len]
  # find the average width of each object and two standard deviations
  average_width=np.average(tiller_len)
  std=np.std(tiller_len)
  median=np.median(tiller_len)
  two_std=(2*std) 
  
  tillering_header=('HEADER_TILLERING' + str(line_position), 'raw_tillering_count', 'raw_tillering_widths','average_tillering_width','median_tillering_width','std_tillering_width')
  tillering_data = (
    'TILLERING_DATA',
    tiller_count,
    tiller_width,
    average_width,
    median,
    std
  )
  
  if filename:
    print_image(ori_img,(str(filename) + '_tiller.png'))
    print('\t'.join(map(str, ('IMAGE', 'tillers', str(filename) + '_tiller.png'))))
  else:
    pass
  
  if debug:
    print_image(background,(str(device) + '_tiller1.png'))
    print_image(ori_mask,(str(device) + '_tiller2.png'))
    print_image(tillers,(str(device) + '_tiller3.png'))
    print_image(ori_img,(str(device) + '_tiller4.png'))
    cv2.line(ori_img,line_point1,line_point2,(255,0,0),1)
    print_image(ori_img,(str(device) + '_tiller_line.png'))
  
  return device, tillering_header, tillering_data, ori_img