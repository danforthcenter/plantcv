import sys
import cv2
import numpy as np
from datetime import datetime
from . import print_image
from . import plot_image
from . import fatal_error
from . import apply_mask


def cluster_contour(device,img, roi_objects, nrow=1,ncol=1,debug=None):

    """
    This function take a image with multiple contours and clusters them based on user input of rows and columns

    Inputs:
    img - An RGB image array
    roi_objects - object contours in an image that are needed to be clustered.
    nrow - number of rows to cluster (this should be the approximate  number of desired rows in the entire image (even if there isn't a literal row of plants)
    ncol - number of columns to cluster (this should be the approximate number of desired columns in the entire image (even if there isn't a literal row of plants)
    file -  output of filename from read_image function
    filenames - input txt file with list of filenames in order from top to bottom left to right
    debug - print debugging images

    :returns:
    device - pipeline step counter
    grouped_contour_indexes - contours grouped
    contours - All inputed contours
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

    # get the list of unique coordinates and group the contours with the same bin coordinates

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

    contours=roi_objects  # Debug image is rainbow printed contours

    if debug == 'print':
        if len(np.shape(img1) == 3:
            img_copy = np.copy(img1)
        else:
            iy, ix = np.shape(img1)
            img_copy = np.zeros((iy, ix, 3), dtype=np.uint8)

        rand_color = color_palette(len(coordlist))
        for i, x in enumerate(coordlist):
            for a in x:
                cv2.drawContours(img_copy, roi_objects, a, rand_color[i], -1, lineType=8)
        print_image(img_copy, (str(device) + '_clusters.png'))

    elif debug == 'plot':
        if len(np.shape(img1) == 3:
            img_copy = np.copy(img1)
        else:
            iy, ix = np.shape(img1)
            img_copy = np.zeros((iy, ix, 3), dtype=np.uint8)

        rand_color = color_palette(len(coordlist))
        for i, x in enumerate(coordlist):
            for a in x:
                cv2.drawContours(img_copy, roi_objects, a, rand_color[i], -1, lineType=8)
        plot_image(img_copy)

    return device, grouped_contour_indexes, contours


def cluster_contour_splitimg(device,img,grouped_contour_indexes,contours,outdir,file=None, filenames=None,debug=None):

    """
    This function takes clustered contours and splits them into multiple images, also does a check to make sure that
    the number of inputted filenames matches the number of clustered contours.

    Inputs:
    img - ideally a masked RGB image.
    grouped_contour_indexes - output of cluster_contours, indexes of clusters of contours
    contours - contours to cluster, output of cluster_contours
    file -  the name of the input image to use as a base name , output of filename from read_image function
    filenames - input txt file with list of filenames in order from top to bottom left to right (likely list of genotypes)
    debug - print debugging images

    :returns:
    device - pipeline step counter
    output_path - array of paths to output images
    """

    # get names to split also to check the target number of objects

    i = datetime.now()
    timenow = i.strftime('%m-%d-%Y_%H:%M:%S')

    if file==None:
        filebase = timenow
    else:
        filebase = file[:-4]

    if filenames==None:
        l=len(coordlist)
        namelist=[]
        for x in range(0,l):
            namelist.append(x)
    else:
        with open(filenames, 'r') as n:
            namelist = n.read().splitlines()
        n.close()

    # make sure the number of objects matches the namelist, and if not, remove the smallest grouped countor
    # removing contours is not ideal but the lists don't match there is a warning to check output

    if len(namelist) == len(grouped_contour_indexes):
        corrected_contour_indexes = grouped_contour_indexes
    elif len(namelist) < len(grouped_contour_indexes):
        print("Warning number of names is less than number of grouped contours, attempting to fix, to double check output")
        diff = len(grouped_contour_indexes) - len(namelist)
        size = []
        for i, x in enumerate(grouped_contour_indexes):
            totallen = []
            for a in x:
                g = unigroup[i]
                la = len(roi_contours[a])
                totallen.append(la)
            sumlen = np.sum(totallen)
            size.append((sumlen, g, i))

        dtype = [('len', int), ('group', list), ('index', int)]
        lencontour = np.array(size, dtype=dtype)
        lencontour = np.sort(lencontour, order='len')

        rm_contour = lencontour[diff:]
        rm_contour = np.sort(rm_contour, order='group')
        corrected_contour_indexes = []

        for x in rm_contour:
            index = x[2]
            grouped_contours_indexes.append(grouped_contour_indexes[index])

    elif len(namelist) > len(coordlist):
        print("Warning number of names is more than number of  grouped contours, double check output")
        diff = len(namelist) - len(coordlist)
        namelist=namelist[0:-diff]
        corrected_contour_indexes = grouped_contour_indexes

    # create filenames

    group_names = []
    for i, x in enumerate(namelist):
        plantname = str(filebase) + '_' + str(x) + '_p' + str(i) + '.jpg'
        group_names.append(plantname)

    # split image

    output_path=[]

    for y, x in enumerate(corrected_contour_indexes):
        savename = str(outdir)+'/'+group_names[y]
        iy, ix, iz = np.shape(img)
        mask = np.zeros((iy, ix, 3), dtype=np.uint8)
        masked_img = np.copy(img)
        for a in x:
            cv2.drawContours(mask, contours, a, (255, 255, 255), -1, lineType=8)

        mask_binary = mask[:, :, 0]

        if np.sum(mask_binary) == 0:
            pass
        else:
            retval, mask_binary = cv2.threshold(mask_binary, 254, 255, cv2.THRESH_BINARY)
            device, masked1 = apply_mask(masked_img, mask_binary, 'white', device, debug)
            print_image(masked1,savename)
            output_path.append(savename)

            if debug == 'print':
                print_image(masked1, (str(device) + '_clusters.png'))
            elif debug == 'plot':
                if len(np.shape(masked1)) == 3:
                    plot_image(masked1)
                else:
                    plot_image(masked1, cmap='gray')
                    plot_image(masked1)

    return device, output_path


