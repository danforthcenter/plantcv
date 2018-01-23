# Analyzes an object and outputs numeric properties

import cv2
import numpy as np
from . import print_image
from . import plot_image


def analyze_object(img, imgname, obj, mask, device, debug=None, filename=False):
    """Outputs numeric properties for an input object (contour or grouped contours).

    Inputs:
    img             = image object (most likely the original), color(RGB)
    imgname         = name of image file.  (No longer used; kept for compatibility)
    obj             = single or grouped contour object
    mask            = binary image to use as mask for moments analysis
    device          = device number. Used to count steps in the pipeline
    debug           = None, print, or plot. Print = save to file, Plot = print to screen.
    filename        = False or image name. If defined print image

    Returns:
    device          = device number
    shape_header    = shape data table headers
    shape_data      = shape data table values
    analysis_images = list of output images

    :param img: numpy array
    :param imgname: str
    :param obj: list
    :param mask: numpy array
    :param device: int
    :param debug: str
    :param filename: str
    :return:
    """

    device += 1

    # Valid objects can only be analyzed if they have >= 5 vertices
    if len(obj) < 5:
        return device, None, None, None

    ori_img = np.copy(img)
    if len(np.shape(img)) == 3:
        ix, iy, iz = np.shape(img)
    else:
        ix, iy = np.shape(img)
    size = ix, iy, 3
    size1 = ix, iy
    background = np.zeros(size, dtype=np.uint8)
    background1 = np.zeros(size1, dtype=np.uint8)
    background2 = np.zeros(size1, dtype=np.uint8)

    # Check is object is touching image boundaries (QC)
    frame_background = np.zeros(size1, dtype=np.uint8)
    frame = frame_background + 1
    frame_contour, frame_heirarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    ptest = []
    vobj = np.vstack(obj)
    for i, c in enumerate(vobj):
        xy = tuple(c)
        pptest = cv2.pointPolygonTest(frame_contour[0], xy, measureDist=False)
        ptest.append(pptest)
    in_bounds = all(c == 1 for c in ptest)

    # Convex Hull
    hull = cv2.convexHull(obj)
    hull_vertices = len(hull)
    # Moments
    #  m = cv2.moments(obj)
    m = cv2.moments(mask, binaryImage=True)
    # Properties
    # Area
    area = m['m00']

    if area:
        # Convex Hull area
        hull_area = cv2.contourArea(hull)
        # Solidity
        solidity = 1
        if int(hull_area) != 0:
            solidity = area / hull_area
        # Perimeter
        perimeter = cv2.arcLength(obj, closed=True)
        # x and y position (bottom left?) and extent x (width) and extent y (height)
        x, y, width, height = cv2.boundingRect(obj)
        # Centroid (center of mass x, center of mass y)
        cmx, cmy = (m['m10'] / m['m00'], m['m01'] / m['m00'])
        # Ellipse
        center, axes, angle = cv2.fitEllipse(obj)
        major_axis = np.argmax(axes)
        minor_axis = 1 - major_axis
        major_axis_length = axes[major_axis]
        minor_axis_length = axes[minor_axis]
        eccentricity = np.sqrt(1 - (axes[minor_axis] / axes[major_axis]) ** 2)

        # Longest Axis: line through center of mass and point on the convex hull that is furthest away
        cv2.circle(background, (int(cmx), int(cmy)), 4, (255, 255, 255), -1)
        center_p = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
        ret, centerp_binary = cv2.threshold(center_p, 0, 255, cv2.THRESH_BINARY)
        centerpoint, cpoint_h = cv2.findContours(centerp_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

        dist = []
        vhull = np.vstack(hull)

        for i, c in enumerate(vhull):
            xy = tuple(c)
            pptest = cv2.pointPolygonTest(centerpoint[0], xy, measureDist=True)
            dist.append(pptest)

        abs_dist = np.absolute(dist)
        max_i = np.argmax(abs_dist)

        caliper_max_x, caliper_max_y = list(tuple(vhull[max_i]))
        caliper_mid_x, caliper_mid_y = [int(cmx), int(cmy)]

        xdiff = float(caliper_max_x - caliper_mid_x)
        ydiff = float(caliper_max_y - caliper_mid_y)

        if xdiff != 0:
            slope = (float(ydiff / xdiff))
        if xdiff == 0:
            slope = 1
        b_line = caliper_mid_y - (slope * caliper_mid_x)

        if slope == 0:
            xintercept = 0
            xintercept1 = 0
            yintercept = 'none'
            yintercept1 = 'none'
            cv2.line(background1, (iy, caliper_mid_y), (0, caliper_mid_y), (255), 1)
        else:
            xintercept = int(-b_line / slope)
            xintercept1 = int((ix - b_line) / slope)
            yintercept = 'none'
            yintercept1 = 'none'
            if 0 <= xintercept <= iy and 0 <= xintercept1 <= iy:
                cv2.line(background1, (xintercept1, ix), (xintercept, 0), (255), 1)
            elif xintercept < 0 or xintercept > iy or xintercept1 < 0 or xintercept1 > iy:
                if xintercept < 0 and 0 <= xintercept1 <= iy:
                    yintercept = int(b_line)
                    cv2.line(background1, (0, yintercept), (xintercept1, ix), (255), 1)
                elif xintercept > iy and 0 <= xintercept1 <= iy:
                    yintercept1 = int((slope * iy) + b_line)
                    cv2.line(background1, (iy, yintercept1), (xintercept1, ix), (255), 1)
                elif 0 <= xintercept <= iy and xintercept1 < 0:
                    yintercept = int(b_line)
                    cv2.line(background1, (0, yintercept), (xintercept, 0), (255), 1)
                elif 0 <= xintercept <= iy and xintercept1 > iy:
                    yintercept1 = int((slope * iy) + b_line)
                    cv2.line(background1, (iy, yintercept1), (xintercept, 0), (255), 1)
                else:
                    yintercept = int(b_line)
                    yintercept1 = int((slope * iy) + b_line)
                    cv2.line(background1, (0, yintercept), (iy, yintercept1), (255), 1)

        ret1, line_binary = cv2.threshold(background1, 0, 255, cv2.THRESH_BINARY)
        # print_image(line_binary,(str(device)+'_caliperfit.png'))

        cv2.drawContours(background2, [hull], -1, (255), -1)
        ret2, hullp_binary = cv2.threshold(background2, 0, 255, cv2.THRESH_BINARY)
        # print_image(hullp_binary,(str(device)+'_hull.png'))

        caliper = cv2.multiply(line_binary, hullp_binary)
        # print_image(caliper,(str(device)+'_caliperlength.png'))

        caliper_y, caliper_x = np.array(caliper.nonzero())
        caliper_matrix = np.vstack((caliper_x, caliper_y))
        caliper_transpose = np.transpose(caliper_matrix)
        caliper_length = len(caliper_transpose)

        caliper_transpose1 = np.lexsort((caliper_y, caliper_x))
        caliper_transpose2 = [(caliper_x[i], caliper_y[i]) for i in caliper_transpose1]
        caliper_transpose = np.array(caliper_transpose2)

    # else:
    #  hull_area, solidity, perimeter, width, height, cmx, cmy = 'ND', 'ND', 'ND', 'ND', 'ND', 'ND', 'ND'

    # Store Shape Data
    shape_header = [
        'HEADER_SHAPES',
        'area',
        'hull-area',
        'solidity',
        'perimeter',
        'width',
        'height',
        'longest_axis',
        'center-of-mass-x',
        'center-of-mass-y',
        'hull_vertices',
        'in_bounds',
        'ellipse_center_x',
        'ellipse_center_y',
        'ellipse_major_axis',
        'ellipse_minor_axis',
        'ellipse_angle',
        'ellipse_eccentricity'
    ]

    shape_data = [
        'SHAPES_DATA',
        area,
        hull_area,
        solidity,
        perimeter,
        width,
        height,
        caliper_length,
        cmx,
        cmy,
        hull_vertices,
        in_bounds,
        center[0],
        center[1],
        major_axis_length,
        minor_axis_length,
        angle,
        eccentricity
    ]

    analysis_images = []

    # Draw properties
    if area and filename:
        cv2.drawContours(ori_img, obj, -1, (255, 0, 0), 3)
        cv2.drawContours(ori_img, [hull], -1, (0, 0, 255), 3)
        cv2.line(ori_img, (x, y), (x + width, y), (0, 0, 255), 3)
        cv2.line(ori_img, (int(cmx), y), (int(cmx), y + height), (0, 0, 255), 3)
        cv2.line(ori_img, (tuple(caliper_transpose[caliper_length - 1])), (tuple(caliper_transpose[0])), (0, 0, 255), 3)
        cv2.circle(ori_img, (int(cmx), int(cmy)), 10, (0, 0, 255), 3)
        # Output images with convex hull, extent x and y
        extention = filename.split('.')[-1]
        # out_file = str(filename[0:-4]) + '_shapes.' + extention
        out_file = str(filename[0:-4]) + '_shapes.jpg'
        out_file1 = str(filename[0:-4]) + '_mask.jpg'

        if debug == 'print':
            print_image(ori_img, out_file)
        analysis_images.append(['IMAGE', 'shapes', out_file])

        if debug == 'print':
            print_image(mask, out_file1)
        analysis_images.append(['IMAGE', 'mask', out_file1])

    else:
        pass

    if debug is not None:
        cv2.drawContours(ori_img, obj, -1, (255, 0, 0), 3)
        cv2.drawContours(ori_img, [hull], -1, (0, 0, 255), 3)
        cv2.line(ori_img, (x, y), (x + width, y), (0, 0, 255), 3)
        cv2.line(ori_img, (int(cmx), y), (int(cmx), y + height), (0, 0, 255), 3)
        cv2.circle(ori_img, (int(cmx), int(cmy)), 10, (0, 0, 255), 3)
        cv2.line(ori_img, (tuple(caliper_transpose[caliper_length - 1])), (tuple(caliper_transpose[0])), (0, 0, 255), 3)
        if debug == 'print':
            print_image(ori_img, (str(device) + '_shapes.jpg'))
        elif debug == 'plot':
            if len(np.shape(img)) == 3:
                plot_image(ori_img)
            else:
                plot_image(ori_img, cmap='gray')

    return device, shape_header, shape_data, analysis_images
