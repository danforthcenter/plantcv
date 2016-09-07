import sys
import cv2
import numpy as np
from . import print_image
from . import plot_image
from . import fatal_error
from . import apply_mask


def cluster_contour(device,img, roi_objects, nrow=1,ncol=1 debug=None):

    """.
    Inputs:
    img - An RGB image array
    roi_objects - a list of object contours in an image that are needed to be clustered.
    nrow - number of rows to cluster (this should be the approximage number of desired rows in the entire image (even if there isn't a literal row of plants)
    ncol - number of columns to cluster (this should be the approximate number of desired rows in the entire image (even if there isn't a literal row of plants)

    :returns:
    device - pipeline step counter
    grouped_contours - contours grouped
    """
    device += 1


    if len(np.shape(img))==3:
        iy, ix, iz = np.shape(img)
    else:
        iy, ix, =np.shape(img)

    # get the break groups

    if nrow==1:
        rbreaks=iy
    else:
        rstep = np.rint(iy / nrow)
        rstep1 = np.int(rstep)
        rbreaks = range(0, iy, rstep1)
    if ncol==1:
        cbreaks=ix
    else:
        cstep = np.rint(ix / n)
        cstep1 = np.int(step)
        cbreaks = range(0, ix, cstep1)

    # categorize what bin the center of mass of each contour

    dtype = [('cx', int), ('cy', int), ('rowbin', int), ('colbin', int), ('index', int)]
    coord = []
    for i in range(0, len(roi_objects)):
        m = cv2.moments(roi_objects[i])
        if m['m00'] == 0:
            pass
        else:
            cx = int(m['m10'] / m['m00'])
            cy = int(m['m01'] / m['m00'])
            colbin = np.digitize(cx, cbreaks)
            rowbin = np.digitize(cy, rbreaks)
            a = (cx, cy, colbin, rowbin, i)
            coord.append(a)
    coord1 = np.array(coord, dtype=dtype)
    coord2 = np.sort(coord1, order=('colbin', 'rowbin'))

    groups = []
    for i, y in enumerate(coord2):
        col = y[3]
        row = y[2]
        location = str(row) + ',' + str(col)
        groups.append(location)

    unigroup = np.unique(groups)

    coordgroups = []

    for i, y in enumerate(unigroup):
        col = int(y[0])
        row = int(y[2])
        for a, b in enumerate(coord2):
            if b[2] == col and b[3] == row:
                grp = i
                contour = b[4]
                coordgroups.append((grp, contour))
            else:
                pass

    coordlist = [[y[1] for y in coordgroups if y[0] == x] for x in range(0, (len(unigroup)))]


    if debug == 'print':
            print_image(ori_img2, (str(device) + '_whitebalance_roi.png'))
            print_image(finalcorrected, (str(device) + '_whitebalance.png'))

        elif debug == 'plot':
            if len(np.shape(img)) == 3:
                ix, iy, iz = np.shape(ori_img2)
                plot_image(ori_img2)
                plot_image(finalcorrected)
            else:
                plot_image(ori_img2, cmap='gray')
                plot_image(finalcorrected, cmap='gray')

        return device,grouped_contours



