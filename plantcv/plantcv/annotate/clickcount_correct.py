"""Detect dics."""
import os
import numpy as np
from plantcv.plantcv.floodfill import floodfill
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def _recover_circ(bin_img, c):
    # Generates a binary image of a disc based on the coordinates c
    # and the surrounding white pixels in bin_img
    
    # make bin_img 1-0
    bin_img = 1*(bin_img != 0)
    h,w = bin_img.shape
    # coordinates of pixels in the shape of the bin_image
    X,Y = np.meshgrid(np.linspace(0,w-1,w),np.linspace(0,h-1,h))

    
    # Alternate two steps: 
    # 1 - growing the disc centered in c until it overlaps with black pixels in bin_img.
    # 2 - move c a step of at least one pixel towards the center of mass (mean of coordinate values) 
    # of the white pixels of bin_img that overlap with the disc.
    # It terminates when the direction of the step in both axis has changed once.
    
    # radius
    r = 0
    
    # sum of previous directions
    dir_x_hist = 0
    dir_y_hist = 0
    
    # flags indicate if there has been a change in direction in each axis
    chg_dir_x = False
    chg_dir_y = False
    
    while (chg_dir_x and chg_dir_y) == False:
        # image of concentric circles centered in c
        circ = np.sqrt((X-c[1])**2+(Y-c[0])**2)
        
        # growing radius until it reaches black pixels 
        inside = True
        while inside == True:
            circ_mask = 1*(circ < r)
            circ_mask_area = np.sum(circ_mask)
            masked_circ = bin_img*circ_mask
            # if masked_circ has a smaller count it means the circle is 
            # overlapping black pixels -> no longer inside the white part
            if np.abs(np.sum(masked_circ) - circ_mask_area) > 100:
                inside = False
            else:
                r += 1
                
        # moving center towards the center of mass 
        Cx = np.mean(X[masked_circ==1])
        Cy = np.mean(Y[masked_circ==1])
        #dist = np.sqrt( (Cx-c[1])**2 + (Cy-c[0])**2 )
        
        dir_x = np.sign(Cx - c[1])
        dir_y = np.sign(Cy - c[0])
        
        stepx = dir_x*np.ceil(np.abs(Cx - c[1]))
        stepy = dir_y*np.ceil(np.abs(Cy - c[0]))
        
        dir_x_hist += dir_x 
        dir_y_hist += dir_y 
        
        # register that a change in direction has occurred to terminate when
        # is has happened in both directions
        if np.sign(dir_x_hist) != dir_x or dir_x==0:
            chg_dir_x = True
            
        if np.sign(dir_y_hist) != dir_y or dir_y==0:
            chg_dir_y = True
        
        # if there is no step to take, terminate loop
        #if (dir_x==0) and (dir_y==0):
        #    chg_dir_x = True
        #    
        #    chg_dir_y = True
        
        c[1] += stepx.astype(np.int32)
        c[0] += stepy.astype(np.int32)
    
    circ_mask = 1*(circ < r)
    masked_circ = (bin_img*circ_mask).astype(np.uint8)
    masked_circ[c[0],c[1]] = 1 # center of mass always part of the mask
    
    return masked_circ, c

def _clickcount_labels(counter):
    labels = [key for key in counter.count]
    
    return labels

def _remove_points(autolist,confirmedlist):
    # internal function to remove to remove points specified by a user
    removecoor=[]

    for element in autolist:
        if element not in confirmedlist:
            removecoor.append(element)
            
    return removecoor

def clickcount_correct(bin_img, bin_img_recover, counter, coor):
    # bin_img - binary image, image with selected objects
    # bin_img_recover - binary image, image with all potential objects
    # counter - ClickCount object
    # coor - coordinates of 'auto' detected points (coordinate output of detect_discs)

    debug = params.debug
    params.debug = None
    
    labelnames=_clickcount_labels(counter)
            
    completed_mask = np.copy(bin_img)
    
    totalcoor=[]
    
    for names in labelnames:
        for i, (x,y) in enumerate(counter.points[names]):
            x = int(x)
            y = int(y)
            totalcoor.append((y,x))
    
    
    removecoor= _remove_points(coor,totalcoor)
    removecoor= list(map(lambda sub: (sub[1], sub[0]), removecoor)) 
    completed_mask=floodfill(completed_mask, removecoor,0)
    
    # points in class used for recovering and labeling
    for names in labelnames:
        for i, (x,y) in enumerate(counter.points[names]):
            x = int(x)
            y = int(y)
            counter.points[names][i] = (x,y) # corrected coordinates 
            # if the coordinates point to 0 in the binary image, recover the grain and coordinates of center
            if completed_mask[y,x] == 1 or completed_mask[y,x]==0:
                print(f"Recovering grain at coordinates: x = {x}, y = {y}")
                masked_circ, [a,b] = _recover_circ(bin_img_recover, [y,x])
                completed_mask = completed_mask + masked_circ
                counter.points[names][i] = (b,a)
    
    completed_mask1 = 1*((completed_mask + 1*(completed_mask==255)) != 0).astype(np.uint8)
    
    params.debug = debug

    _debug(visual=completed_mask1, filename=os.path.join(params.debug_outdir, f"{params.device}_clickcount-corrected.png"))
     
    return completed_mask, counter