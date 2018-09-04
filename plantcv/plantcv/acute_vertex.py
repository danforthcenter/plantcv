# Script to identify corners/acute angles of an object

import os
import cv2
import numpy as np
import math
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


def acute_vertex(obj, win, thresh, sep, img):
    """acute_vertex: identify corners/acute angles of an object

    For each point in contour, get a point before (pre) and after (post) the point of interest,
    calculate the angle between the pre and post point.

    Inputs:
    obj    = a contour of the plant object (this should be output from the object_composition.py fxn)
    win    = win argument specifies the pre and post point distances (a value of 30 worked well for a sample image)
    thresh = an threshold to set for acuteness; keep points with an angle more acute than the threshold (a value of 15
             worked well for sample image)
    sep    = the number of contour points to search within for the most acute value
    img    = the original image

    :param obj: ndarray
    :param win: int
    :param thresh: int
    :param sep: int
    :param img: ndarray
    :return acute: ndarray
    """
    params.device += 1
    chain = []
    if not np.any(obj):
        acute = ('NA', 'NA')
        return acute
    for i in range(len(obj) - win):
        x, y = obj[i].ravel()
        pre_x, pre_y = obj[i - win].ravel()
        post_x, post_y = obj[i + win].ravel()
        # print "The iterator i is currently " + str(i)
        # print "Here are the values: " + str(x) + " " + str(y)
        # print "Here are the pre values: " + str(pre_x) + " " + str(pre_y)
        # print "Here are the post values: " + str(post_x) + " " + str(post_y)
        # Angle in radians derived from Law of Cosines, converted to degrees
        P12 = np.sqrt((x-pre_x)*(x-pre_x)+(y-pre_y)*(y-pre_y))
        P13 = np.sqrt((x-post_x)*(x-post_x)+(y-post_y)*(y-post_y))
        P23 = np.sqrt((pre_x-post_x)*(pre_x-post_x)+(pre_y-post_y)*(pre_y-post_y))
        if (2*P12*P13) > 0.001:
            dot = (P12*P12 + P13*P13 - P23*P23)/(2*P12*P13)
        if (2*P12*P13) < 0.001:
            dot = (P12*P12 + P13*P13 - P23*P23)/0.001
        if dot > 1:                            # If float excedes 1 prevent arcos error and force to equal 1
            dot = 1
        elif dot < -1:                     # If float excedes -1 prevent arcos error and force to equal -1
            dot = -1            
        ang = math.degrees(math.acos(dot))
        # print "Here is the angle: " + str(ang)
        chain.append(ang)
        
    # Select points in contour that have an angle more acute than thresh
    index = []
    for c in range(len(chain)):         
        if float(chain[c]) <= thresh:
            index.append(c)
    # There oftentimes several points around tips with acute angles
    # Here we try to pick the most acute angle given a set of contiguous point
    # Sep is the number of points to evaluate the number of verticies
    out = []
    tester = []
    for i in range(len(index)-1):
        # print str(index[i])
        if index[i+1] - index[i] < sep:
            tester.append(index[i])
        if index[i+1] - index[i] >= sep:
            tester.append(index[i])
            # print(tester)
            angles = ([chain[d] for d in tester])
            keeper = angles.index(min(angles))
            t = tester[keeper]
            # print str(t)
            out.append(t)
            tester = []
        
    # Store the points in the variable acute
    flag = 0
    acute = obj[[out]]
    # If no points found as acute get the largest point
    if len(acute) == 0:
        acute = max(obj, key=cv2.contourArea)
        flag = 1
    # img2 = np.copy(img)
    # cv2.circle(img2,(int(cmx),int(cmy)),30,(0,215,255),-1)
    # cv2.circle(img2,(int(cmx),int(bly)),30,(255,0,0),-1)
    # Plot each of these tip points on the image
    # for i in acute:
    #        x,y = i.ravel()
    #        cv2.circle(img2,(x,y),15,(153,0,153),-1)
    # cv2.imwrite('tip_points_centroid_and_base.png', img2)
    if params.debug == 'print':
        # Lets make a plot of these values on the
        img2 = np.copy(img)
        # Plot each of these tip points on the image
        for i in acute:
            x, y = i.ravel()
            cv2.circle(img2, (x, y), 15, (255, 204, 255), -1)
        print_image(img2, os.path.join(params.debug_outdir, str(params.device) + '_acute_vertices.png'))
    elif params.debug == 'plot':
        # Lets make a plot of these values on the
        img2 = np.copy(img)
        # Plot each of these tip points on the image
        for i in acute:
            x, y = i.ravel()
            # cv2.circle(img2,(x,y),15,(255,204,255),-1)
            cv2.circle(img2, (x, y), 15, (0, 0, 255), -1)
        plot_image(img2)
    # If flag was true (no points found as acute) reformat output appropriate type
    if flag == 1:
        acute = np.asarray(acute)
        acute = acute.reshape(1, 1, 2)
    return acute
# End of function
