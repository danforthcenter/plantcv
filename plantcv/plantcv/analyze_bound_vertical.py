# User-Input Boundary Line

import os
import cv2
import numpy as np
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


def analyze_bound_vertical(img, obj, mask, line_position):
    """User-input boundary line tool

    Inputs:
    img             = RGB or grayscale image data for plotting
    obj             = single or grouped contour object
    mask            = Binary mask made from selected contours
    shape_header    = pass shape header data to function
    shape_data      = pass shape data so that analyze_bound data can be appended to it
    line_position   = position of boundary line (a value of 0 would draw the line through the left side of the image)

    Returns:
    bound_header    = data table column headers
    bound_data      = boundary data table
    analysis_images = output images

    :param img: numpy.ndarray
    :param obj: list
    :param mask: numpy.ndarray
    :param line_position: int
    :return bound_header: tuple
    :return bound_data: tuple
    :return analysis_images: list
    """

    params.device += 1
    ori_img = np.copy(img)

    # Draw line horizontal line through bottom of image, that is adjusted to user input height
    if len(np.shape(ori_img)) == 2:
        ori_img = cv2.cvtColor(ori_img, cv2.COLOR_GRAY2BGR)
    iy, ix, iz = np.shape(ori_img)
    size = (iy, ix)
    size1 = (iy, ix, 3)
    background = np.zeros(size, dtype=np.uint8)
    wback = (np.zeros(size1, dtype=np.uint8)) + 255
    x_coor = 0 + int(line_position)
    y_coor = int(iy)
    rec_point1 = (0, 0)
    rec_point2 = (x_coor, y_coor - 2)
    cv2.rectangle(background, rec_point1, rec_point2, (255), -1)
    right_contour, right_hierarchy = cv2.findContours(background, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

    x, y, width, height = cv2.boundingRect(obj)

    if x_coor - x <= 0:
        width_left_bound = 0
        width_right_bound = width
    elif x_coor - x > 0:
        width_1 = x_coor - x
        if width - width_1 <= 0:
            width_left_bound = width
            width_right_bound = 0
        else:
            width_left_bound = x_coor - x
            width_right_bound = width - width_left_bound

    right = []
    left = []
    mask_nonzerox, mask_nonzeroy = np.nonzero(mask)
    obj_points = np.vstack((mask_nonzeroy, mask_nonzerox))
    obj_points1 = np.transpose(obj_points)

    for i, c in enumerate(obj_points1):
        xy = tuple(c)
        pptest = cv2.pointPolygonTest(right_contour[0], xy, measureDist=False)
        if pptest == 1:
            left.append(xy)
            cv2.circle(ori_img, xy, 1, (0, 0, 255))
            cv2.circle(wback, xy, 1, (0, 0, 255))
        else:
            right.append(xy)
            cv2.circle(ori_img, xy, 1, (0, 255, 0))
            cv2.circle(wback, xy, 1, (0, 255, 0))
    right_bound_area = len(right)
    left_bound_area = len(left)
    percent_bound_area_right = ((float(right_bound_area)) / (float(left_bound_area + right_bound_area))) * 100
    percent_bound_area_left = ((float(left_bound_area)) / (float(right_bound_area + left_bound_area))) * 100

    bound_header = [
        'HEADER_BOUNDARY' + str(line_position),
        'width_left_bound',
        'width_right_bound',
        'left_bound_area',
        'percent_left_bound_area',
        'right_bound_area',
        'percent_right_bound_area'
    ]

    bound_data = [
        'BOUNDARY_DATA',
        width_left_bound,
        width_right_bound,
        left_bound_area,
        percent_bound_area_left,
        right_bound_area,
        percent_bound_area_right
    ]

    analysis_images = []

    if left_bound_area or right_bound_area:
        point3 = (x_coor+2, 0)
        point4 = (x_coor+2, y_coor)
        cv2.line(ori_img, point3, point4, (255, 0, 255), 5)
        cv2.line(wback, point3, point4, (255, 0, 255), 5)
        m = cv2.moments(mask, binaryImage=True)
        cmx, cmy = (m['m10'] / m['m00'], m['m01'] / m['m00'])
        if x_coor - x <= 0:
            cv2.line(ori_img, (x, int(cmy)), (x + width, int(cmy)), (0, 255, 0), 3)
            cv2.line(wback, (x, int(cmy)), (x + width, int(cmy)), (0, 255, 0), 3)
        elif x_coor - x > 0:
            width_1 = x_coor - x
            if width - width_1 <= 0:
                cv2.line(ori_img, (x, int(cmy)), (x + width, int(cmy)), (255, 0, 0), 3)
                cv2.line(wback, (x, int(cmy)), (x + width, int(cmy)), (255, 0, 0), 3)
            else:
                cv2.line(ori_img, (x_coor + 2, int(cmy)), (x_coor + width_left_bound, int(cmy)), (255, 0, 0), 3)
                cv2.line(ori_img, (x_coor + 2, int(cmy)), (x_coor - width_right_bound, int(cmy)), (0, 255, 0), 3)
                cv2.line(wback, (x_coor + 2, int(cmy)), (x_coor + width_left_bound, int(cmy)), (255, 0, 0), 3)
                cv2.line(wback, (x_coor + 2, int(cmy)), (x_coor - width_right_bound, int(cmy)), (0, 255, 0), 3)
        # Output images with boundary line
        analysis_images.append(wback)
        analysis_images.append(ori_img)

    if params.debug is not None:
        point3 = (x_coor+2, 0)
        point4 = (x_coor+2, y_coor)
        cv2.line(ori_img, point3, point4, (255, 0, 255), 5)
        cv2.line(wback, point3, point4, (255, 0, 255), 5)
        m = cv2.moments(mask, binaryImage=True)
        cmx, cmy = (m['m10'] / m['m00'], m['m01'] / m['m00'])
        if x_coor - x <= 0:
            cv2.line(ori_img, (x, int(cmy)), (x + width, int(cmy)), (0, 255, 0), 3)
            cv2.line(wback, (x, int(cmy)), (x + width, int(cmy)), (0, 255, 0), 3)
        elif x_coor - x > 0:
            width_1 = x_coor - x
            if width - width_1 <= 0:
                cv2.line(ori_img, (x, int(cmy)), (x + width, int(cmy)), (255, 0, 0), 3)
                cv2.line(wback, (x, int(cmy)), (x + width, int(cmy)), (255, 0, 0), 3)
            else:
                cv2.line(ori_img, (x_coor + 2, int(cmy)), (x_coor + width_left_bound, int(cmy)), (255, 0, 0), 3)
                cv2.line(ori_img, (x_coor + 2, int(cmy)), (x_coor - width_right_bound, int(cmy)), (0, 255, 0), 3)
                cv2.line(wback, (x_coor + 2, int(cmy)), (x_coor + width_left_bound, int(cmy)), (255, 0, 0), 3)
                cv2.line(wback, (x_coor + 2, int(cmy)), (x_coor - width_right_bound, int(cmy)), (0, 255, 0), 3)
        if params.debug == 'print':
            print_image(wback, os.path.join(params.debug_outdir, str(params.device) + '_boundary_on_white.jpg'))
            print_image(ori_img, os.path.join(params.debug_outdir, str(params.device) + '_boundary_on_img.jpg'))
        if params.debug == 'plot':
            plot_image(wback)
            plot_image(ori_img)

    return bound_header, bound_data, analysis_images
