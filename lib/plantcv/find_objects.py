### Find Objects
def find_objects(img, mask, device, debug=False):
  # find all objects and color them blue
  # img = image that the objects will be overlayed
  # mask = what is used for object detection
  # device = device number.  Used to count steps in the pipeline
  # debug = True/False. If True, print image
  device += 1
  mask1=np.copy(mask)
  ori_img=np.copy(img)
  objects,hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
  for i,cnt in enumerate(objects):
     cv2.drawContours(ori_img,objects,i, color_palette(1)[0],-1, lineType=8,hierarchy=hierarchy)
  if debug:
    print_image(ori_img, (str(device) + '_id_objects.png'))
  
  return device, objects, hierarchy