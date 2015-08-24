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
    
  if v_pos=="top":
    # Add rows to the top
    top=np.zeros((x,my),dtype=np.uint8)
    maskv=np.vstack((top,mask))
    
    if len(np.shape(maskv))==3:
      mx,my,mz=np.shape(maskv)
    else:
      mx,my=np.shape(maskv)
        
    if mx>=ix:
      maskv=maskv[0:ix,0:my]
            
    if mx<ix:
      r=ix-mx
      rows=np.zeros((r,my),dtype=np.uint8)
      maskv=np.vstack((maskv,rows))
    if debug:
      print_image(maskv,(str(device)+"_push-top_.png"))
    
    print np.shape(img)
    print np.shape(maskv)
    
  if v_pos=="bottom":
    # Add rows to the top
    bottom=np.zeros((x,my),dtype=np.uint8)
    maskv=np.vstack((mask,bottom))
    
    if len(np.shape(maskv))==3:
      mx,my,mz=np.shape(maskv)
    else:
      mx,my=np.shape(maskv)
        
    if mx>=ix:
      maskv=maskv[0:ix,0:my]
            
    if mx<ix:
      r=ix-mx
      rows=np.zeros((r,my),dtype=np.uint8)
      maskv=np.vstack((rows,maskv))
    if debug:
      print_image(maskv,(str(device)+"_push-bottom.png"))
    
  if h_pos=="left":
    if len(np.shape(maskv))==3:
      mx,my,mz=np.shape(maskv)
    else:
      mx,my=np.shape(maskv)
      
    # Add rows to the left
    left=np.zeros((mx,y),dtype=np.uint8)
    maskv=np.hstack((left,maskv))
    
    if len(np.shape(maskv))==3:
      mx,my,mz=np.shape(maskv)
    else:
      mx,my=np.shape(maskv)
        
    if my>=iy:
      maskv=maskv[0:mx,0:iy]
            
    if my<iy:
      c=iy-my
      col=np.zeros((mx,c),dtype=np.uint8)
      maskv=np.hstack((maskv,col))
    if debug:
      print_image(maskv,(str(device)+"_push-left.png"))
      
    print np.shape(img)
    print np.shape(maskv)
    
  if h_pos=="right":
    if len(np.shape(maskv))==3:
      mx,my,mz=np.shape(maskv)
    else:
      mx,my=np.shape(maskv)
      
    # Add rows to the left
    right=np.zeros((mx,y),dtype=np.uint8)
    maskv=np.hstack((maskv,right))
    
    if len(np.shape(maskv))==3:
      mx,my,mz=np.shape(maskv)
    else:
      mx,my=np.shape(maskv)
        
    if my>=iy:
      ex=my-iy
      maskv=maskv[0:mx,ex:my]
            
    if my<iy:
      c=iy-my
      col=np.zeros((mx,c),dtype=np.uint8)
      maskv=np.hstack((col,maskv))
    if debug:
      print_image(maskv,(str(device)+"_push-right.png"))  
    
    
  newmask=1
    
    ##Add rows to the left
    #l=((x+mx),y)
    #left=np.zeros(l,dtype=np.uint8)
    #maskv1=maskv[:,y:]
    #maskh=np.hstack((maskv1,left))
    #nx,ny=np.shape(maskh)
    #
    
    #if ni<ix or ny<iy:
    #  r=((ni-ix),ny)
    #  print r
    #  print np.shape(img)
    #  print np.shape(maskh)
    #  xadd=np.zeros(r,dtype=np.uint8)
    #  maskh1=np.hstack((xadd,maskh))
    #  h1x,h1y=np.shape(maskh1)
    #  
    #  c=(h1x,(ny-ni))
    #  yadd=np.zeros(c,dtype=np.uint8)
    #  maskv1=np.vstack((maskh1,yadd))
    #
    #  newmask=np.array(maskv1[0:ix,0:iy])
  #  
  #if v_pos=="top" and h_pos=="right":
  #  top=np.zeros((x,my),dtype=np.uint8)
  #  maskv=np.vstack((top,mask))
  #  
  #  r=((x+mx),y)
  #  right=np.zeros(r,dtype=np.uint8)
  #  maskh=np.hstack((right,maskv))
  #  ni,ny=np.shape(maskh)
  #  
  #  if ni>=ix and ny>=iy:
  #    newmask=np.array(maskh[0:ix,0:iy])
  #  if ni<ix or ny<iy:
  #    r=((ni-ix),ny)
  #    xadd=np.zeros(r,dtype=np.uint8)
  #    maskh1=np.hstack((maskh,xadd))
  #    h1x,h1y=np.shape(maskh1)
  #    
  #    c=(h1x,(ny-iy))
  #    yadd=np.zeros(c,dtype=np.uint8)
  #    maskv1=np.vstack((maskh1,yadd))
  #
  #    newmask=np.array(maskv1[0:ix,0:iy])
  #
  #if v_pos=="bottom" and h_pos=="right":
  #  bottom=np.zeros((x,my),dtype=np.uint8)
  #  maskv=np.vstack((mask,bottom))
  #  
  #  r=((x+mx),y)
  #  right=np.zeros(r,dtype=np.uint8)
  #  maskh=np.hstack((right,maskv))
  #  ni,ny=np.shape(maskh)
  #  
  #  if ni>=ix and ny>=iy:
  #    newmask=np.array(maskh[0:ix,0:iy])
  #  if ni<ix or ny<iy:
  #    r=((ni-ix),ny)
  #    xadd=np.zeros(r,dtype=np.uint8)
  #    maskh1=np.hstack((maskh,xadd))
  #    h1x,h1y=np.shape(maskh1)
  #    
  #    c=(h1x,(ny-iy))
  #    yadd=np.zeros(c,dtype=np.uint8)
  #    maskv1=np.vstack((yadd,maskh1))
  #
  #    newmask=np.array(maskv1[0:ix,0:iy])
  #  
  #if v_pos=="bottom" and h_pos=="left":
  #  bottom=np.zeros((x,my),dtype=np.uint8)
  #  maskv=np.vstack((mask,bottom))
  #  
  #  l=((x+mx),y)
  #  left=np.zeros(l,dtype=np.uint8)
  #  maskv1=maskv[:,y:]
  #  maskh=np.hstack((maskv1,left))
  #  ni,ny=np.shape(maskh)
  #  
  #  if ni>=ix and ny>=iy:
  #    newmask=np.array(maskh[0:ix,0:iy])
  #  if ni<ix or ny<iy:
  #    r=((nyi-ix),ny)
  #    xadd=np.zeros(r,dtype=np.uint8)
  #    maskh1=np.hstack((xadd,maskh))
  #    h1x,h1y=np.shape(maskh1)
  #    
  #    c=(h1x,(ny-iy))
  #    yadd=np.zeros(c,dtype=np.uint8)
  #    maskv1=np.vstack((yadd,maskh1))
  #
  #    newmask=np.array(maskv1[0:ix,0:iy])
  #if debug:
  #  print_image(newmask,(str(device)+"_newmask.png"))
  #  
  #  objects,hierarchy = cv2.findContours(newmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
  #  for i,cnt in enumerate(objects):
  #      cv2.drawContours(ori_img,objects,i, (255,102,255),-1, lineType=8,hierarchy=hierarchy)
  #  print_image(ori_img, (str(device) + '_mask_overlay.png'))
  
  return device, newmask