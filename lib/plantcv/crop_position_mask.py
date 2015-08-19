import cv2
import numpy as np
from . import print_image
from . import fatal_error


def crop_position_mask(img,mask,device,x,y,v_pos,h_pos="right",debug=False):
# img = image to mask
# mask = mask to use (must be correct size, if, not use make_resize_mask function)
# x = x position
# y = y position
# v_pos = push from "top" or "bottom"
# h_pos = push to "right" or "left"
# device = device counter
# debug = if true prints image
  ori_mask=np.copy(mask)
  
  device += 1
  
  if x<0 or y<0:
    fatal_error("x and y cannot be negative numbers or non-integers")
  
  #subtract 1 from x and y since python counts start from 0
  if y!=0:
    y=y-1
  if x!=0:
    x=x-1

  if len(np.shape(img))==3:
    ix,iy,iz=np.shape(img)
    ori_img=np.copy(img)
  else:
    ix,iy=np.shape(img)
    ori_img=np.dstack((img,img,img))
    
  if len(np.shape(mask))==3:
    mx,my,mz=np.shape(mask)
  else:
    mx,my=np.shape(mask)
    
  npimg=np.zeros((ix,iy), dtype=np.uint8)
  
  if v_pos=="top" and h_pos=="right":
    top=np.zeros((x,my),dtype=np.uint8)
    maskv=np.vstack((top,mask))
    
    r=((x+mx),y)
    right=np.zeros(r,dtype=np.uint8)
    maskh=np.hstack((right,maskv))
    ni,ny=np.shape(maskh)
    
    if ni>=ix and ny>=iy:
      newmask=np.array(maskh[0:ix,0:iy])
    if ni<ix or ny<iy:
      r=((ix-ni),ny)
      xadd=np.zeros(r,dtype=np.uint8)
      maskh1=np.hstack((maskh,xadd))
      h1x,h1y=np.shape(maskh1)
      
      c=(h1x,(iy-ni))
      yadd=np.zeros(c,dtype=np.uint8)
      maskv1=np.vstack((maskh1,yadd))

      newmask=np.array(maskv1[0:ix,0:iy])


  if v_pos=="top" and h_pos=="left":
    top=np.zeros((x,my),dtype=np.uint8)
    maskv=np.vstack((top,mask))
    
    l=((x+mx),y)
    left=np.zeros(l,dtype=np.uint8)
    maskv1=maskv[:,y:]
    maskh=np.hstack((maskv1,left))
    ni,ny=np.shape(maskh)
    
    if ni>=ix and ny>=iy:
      newmask=np.array(maskh[0:ix,0:iy])
    if ni<ix or ny<iy:
      r=((ix-ni),ny)
      xadd=np.zeros(r,dtype=np.uint8)
      maskh1=np.hstack((xadd,maskh))
      h1x,h1y=np.shape(maskh1)
      
      c=(h1x,(iy-ni))
      yadd=np.zeros(c,dtype=np.uint8)
      maskv1=np.vstack((maskh1,yadd))

      newmask=np.array(maskv1[0:ix,0:iy])

  if v_pos=="bottom" and h_pos=="right":
    bottom=np.zeros((x,my),dtype=np.uint8)
    maskv=np.vstack((mask,bottom))
    
    r=((x+mx),y)
    right=np.zeros(r,dtype=np.uint8)
    maskh=np.hstack((right,maskv))
    ni,ny=np.shape(maskh)
    
    if ni>=ix and ny>=iy:
      newmask=np.array(maskh[0:ix,0:iy])
    if ni<ix or ny<iy:
      r=((ix-ni),ny)
      xadd=np.zeros(r,dtype=np.uint8)
      maskh1=np.hstack((maskh,xadd))
      h1x,h1y=np.shape(maskh1)
      
      c=(h1x,(iy-ni))
      yadd=np.zeros(c,dtype=np.uint8)
      maskv1=np.vstack((yadd,maskh1))

      newmask=np.array(maskv1[0:ix,0:iy])
    
  if v_pos=="bottom" and h_pos=="left":
    bottom=np.zeros((x,my),dtype=np.uint8)
    maskv=np.vstack((mask,bottom))
    
    l=((x+mx),y)
    left=np.zeros(l,dtype=np.uint8)
    maskv1=maskv[:,y:]
    maskh=np.hstack((maskv1,left))
    ni,ny=np.shape(maskh)
    
    if ni>=ix and ny>=iy:
      newmask=np.array(maskh[0:ix,0:iy])
    if ni<ix or ny<iy:
      r=((ix-ni),ny)
      xadd=np.zeros(r,dtype=np.uint8)
      maskh1=np.hstack((xadd,maskh))
      h1x,h1y=np.shape(maskh1)
      
      c=(h1x,(iy-ni))
      yadd=np.zeros(c,dtype=np.uint8)
      maskv1=np.vstack((yadd,maskh1))

      newmask=np.array(maskv1[0:ix,0:iy])
  if debug:
    print_image(newmask,(str(device)+"_newmask.png"))
    
    objects,hierarchy = cv2.findContours(newmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for i,cnt in enumerate(objects):
        cv2.drawContours(ori_img,objects,i, (255,102,255),-1, lineType=8,hierarchy=hierarchy)
    print_image(ori_img, (str(device) + '_mask_overlay.png'))
  
  return device, newmask