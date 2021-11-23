import os
import cv2
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import color_palette
from plantcv.plantcv import params


def cluster_contours(img, roi_objects, roi_obj_hierarchy, nrow=1, ncol=1, show_grid=False):
    """
    This function take a image with multiple contours and clusters them based on user input of rows and columns

    Inputs:
    img                     = RGB or grayscale image data for plotting
    roi_objects             = object contours in an image that are needed to be clustered.
    roi_obj_hierarchy       = object hierarchy
    nrow                    = number of rows to cluster (this should be the approximate  number of desired rows
                              in the entire image (even if there isn't a literal row of plants)
    ncol                    = number of columns to cluster (this should be the approximate number of desired columns
                              in the entire image (even if there isn't a literal row of plants)
    show_grid               = if True then the grid will get plot to show how plants are being clustered

    Returns:
    grouped_contour_indexes = contours grouped
    contours                = All inputed contours

    :param img: numpy.ndarray
    :param roi_objects: list
    :param roi_obj_hierarchy: numpy.ndarray
    :param nrow: int
    :param ncol: int
    :param show_grid: bool
    :return grouped_contour_indexes: list
    :return contours: list
    :return roi_obj_hierarchy: list
    """

    if len(np.shape(img)) == 3:
        iy, ix, iz = np.shape(img)
    else:
        iy, ix, = np.shape(img)

    # get the break groups
    if nrow == 1:
        rbreaks = [0, iy]
    else:
        rstep = np.rint(iy / nrow)
        rstep1 = int(rstep)
        rbreaks = range(0, iy, rstep1)
    if ncol == 1:
        cbreaks = [0, ix]
    else:
        cstep = np.rint(ix / ncol)
        cstep1 = int(cstep)
        cbreaks = range(0, ix, cstep1)

    # categorize what bin the center of mass of each contour
    def digitize(a, step):
        # The way cbreaks and rbreaks are calculated, step will never be an integer
        # if isinstance(step, int):
        #     i = step
        # else:
        num_bins = len(step)
        for x in range(0, num_bins):
            if x == 0:
                if a >= 0 and a < step[1]:
                    return 1
            else:
                if a >= step[x - 1] and a < step[x]:
                    return x
                elif a >= np.max(step):
                    return num_bins

    dtype = [('cx', int), ('cy', int), ('rowbin', int), ('colbin', int), ('index', int)]
    coord = []
    for i in range(0, len(roi_objects)):
        m = cv2.moments(roi_objects[i])
        if m['m00'] == 0:
            pass
        else:
            cx = int(m['m10'] / m['m00'])
            cy = int(m['m01'] / m['m00'])
            colbin = digitize(cx, cbreaks)
            rowbin = digitize(cy, rbreaks)
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
        col_row = y.split(',')
        col = int(col_row[0])
        row = int(col_row[1])
        for a, b in enumerate(coord2):
            if b[2] == col and b[3] == row:
                grp = i
                contour = b[4]
                coordgroups.append((grp, contour))
            else:
                pass

    coordlist = [[y[1] for y in coordgroups if y[0] == x] for x in range(0, (len(unigroup)))]

    contours = roi_objects
    grouped_contour_indexes = coordlist

    # Debug image is rainbow printed contours

    if params.debug is not None:
        if len(np.shape(img)) == 3:
            img_copy = np.copy(img)
        else:
            iy, ix = np.shape(img)
            img_copy = np.zeros((iy, ix, 3), dtype=np.uint8)

        rand_color = color_palette(len(coordlist))
        for i, x in enumerate(coordlist):
            for a in x:
                if roi_obj_hierarchy[0][a][3] > -1:
                    pass
                else:
                    cv2.drawContours(img_copy, roi_objects, a, rand_color[i], -1, hierarchy=roi_obj_hierarchy)
        if show_grid:
            for y in rbreaks:
                cv2.line(img_copy, (0, y), (ix, y), (255, 0, 0), params.line_thickness)
            for x in cbreaks:
                cv2.line(img_copy, (x, 0), (x, iy), (255, 0, 0), params.line_thickness)
    else:
        img_copy = img  # for _debug

    _debug(visual=img_copy,  # keep this outside if statement to avoid additional test
           filename=os.path.join(params.debug_outdir, str(params.device) + '_clusters.png'))

    return grouped_contour_indexes, contours, roi_obj_hierarchy
