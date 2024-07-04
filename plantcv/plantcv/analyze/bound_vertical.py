"""Analyze the horizontal distribution of the plant relative to a vertical reference line."""
import os
import cv2
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _iterate_analysis, _cv2_findcontours, _object_composition, _grayscale_to_rgb
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def bound_vertical(img, labeled_mask, line_position, n_labels=1, label=None):
    """User-input boundary line analysis for individual objects.

    Inputs:
    img           = RGB or grayscale image data for plotting
    labeled_mask  = Labeled mask of objects (32-bit).
    n_labels      = Total number expected individual objects (default = 1).
    line_position = position of boundary line in pixels from top to bottom
                    (a value of 0 would draw the line through the top of the image)
    label         = Optional label parameter, modifies the variable name of
                    observations recorded (default = pcv.params.sample_label).

    Returns:
    analysis_image = Diagnostic image showing measurements.

    :param img: numpy.ndarray
    :param labeled_mask: numpy.ndarray
    :param n_labels: int
    :param line_position: int
    :param label: str
    :return analysis_image: numpy.ndarray
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    img = _iterate_analysis(img=img, labeled_mask=labeled_mask, n_labels=n_labels,
                            label=label, function=_analyze_bound_vertical,
                            **{"line_position": line_position})
    # Debugging
    _debug(visual=img, filename=os.path.join(params.debug_outdir, str(params.device) + '_boundary_on_img.png'))
    return img


def _analyze_bound_vertical(img, mask, line_position, label):
    """
    User-input boundary line tool

    Inputs:
    img             = RGB or grayscale image data for plotting
    mask            = Binary mask made from selected contours
    line_position   = position of boundary line (a value of 0 would draw the line through the left side of the image)
    label           = optional label parameter, modifies the variable name of observations recorded

    Returns:
    analysis_images = output images

    :param img: numpy.ndarray
    :param mask: numpy.ndarray
    :param line_position: int
    :param label: str
    :return analysis_images: list
    """
    # Initialize output measurements
    width_left_bound = 0
    width_right_bound = 0
    left_bound_area = 0
    percent_bound_area_left = 0
    right_bound_area = 0
    percent_bound_area_right = 0

    ori_img = np.copy(img)
    # Skip empty masks
    if np.count_nonzero(mask) != 0:
        # Draw line horizontal line through bottom of image, that is adjusted to user input height
        ori_img = _grayscale_to_rgb(img)
        iy, ix, _ = np.shape(ori_img)
        size = (iy, ix)
        size1 = (iy, ix, 3)
        background = np.zeros(size, dtype=np.uint8)
        wback = (np.zeros(size1, dtype=np.uint8)) + 255
        x_coor = 0 + int(line_position)
        y_coor = int(iy)
        rec_point1 = (0, 0)
        rec_point2 = (x_coor, y_coor - 2)
        cv2.rectangle(background, rec_point1, rec_point2, (255), -1)
        right_contour, _ = _cv2_findcontours(bin_img=background)

        # Find contours
        cnt, cnt_str = _cv2_findcontours(bin_img=mask)

        # Consolidate contours
        obj = _object_composition(contours=cnt, hierarchy=cnt_str)

        x, _, width, _ = cv2.boundingRect(obj)

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

        for c in obj_points1:
            xy = tuple(int(ci) for ci in c)
            pptest = cv2.pointPolygonTest(right_contour[0], xy, measureDist=False)
            if pptest == 1:
                left.append(xy)
                cv2.circle(ori_img, xy, 1, (155, 0, 255))
                cv2.circle(wback, xy, 1, (155, 0, 255))
            else:
                right.append(xy)
                cv2.circle(ori_img, xy, 1, (0, 255, 0))
                cv2.circle(wback, xy, 1, (0, 255, 0))
        right_bound_area = len(right)
        left_bound_area = len(left)
        percent_bound_area_right = ((float(right_bound_area)) / (float(left_bound_area + right_bound_area))) * 100
        percent_bound_area_left = ((float(left_bound_area)) / (float(right_bound_area + left_bound_area))) * 100

        analysis_images = []

        if left_bound_area or right_bound_area:
            point3 = (x_coor+2, 0)
            point4 = (x_coor+2, y_coor)
            cv2.line(ori_img, point3, point4, (255, 0, 255), params.line_thickness)
            cv2.line(wback, point3, point4, (255, 0, 255), params.line_thickness)
            m = cv2.moments(mask, binaryImage=True)
            _, cmy = (m['m10'] / m['m00'], m['m01'] / m['m00'])
            if x_coor - x <= 0:
                cv2.line(ori_img, (x, int(cmy)), (x + width, int(cmy)), (0, 255, 0), params.line_thickness)
                cv2.line(wback, (x, int(cmy)), (x + width, int(cmy)), (0, 255, 0), params.line_thickness)
            elif x_coor - x > 0:
                width_1 = x_coor - x
                if width - width_1 <= 0:
                    cv2.line(ori_img, (x, int(cmy)), (x + width, int(cmy)), (255, 0, 0), params.line_thickness)
                    cv2.line(wback, (x, int(cmy)), (x + width, int(cmy)), (255, 0, 0), params.line_thickness)
                else:
                    cv2.line(ori_img, (x_coor + 2, int(cmy)), (x_coor + width_left_bound, int(cmy)), (255, 0, 0),
                             params.line_thickness)
                    cv2.line(ori_img, (x_coor + 2, int(cmy)), (x_coor - width_right_bound, int(cmy)), (0, 255, 0),
                             params.line_thickness)
                    cv2.line(wback, (x_coor + 2, int(cmy)), (x_coor + width_left_bound, int(cmy)), (255, 0, 0),
                             params.line_thickness)
                    cv2.line(wback, (x_coor + 2, int(cmy)), (x_coor - width_right_bound, int(cmy)), (0, 255, 0),
                             params.line_thickness)
            # Output images with boundary line
            analysis_images.append(wback)
            analysis_images.append(ori_img)

        point3 = (x_coor+2, 0)
        point4 = (x_coor+2, y_coor)
        cv2.line(ori_img, point3, point4, (255, 0, 255), params.line_thickness)
        cv2.line(wback, point3, point4, (255, 0, 255), params.line_thickness)
        m = cv2.moments(mask, binaryImage=True)
        _, cmy = (m['m10'] / m['m00'], m['m01'] / m['m00'])
        if x_coor - x <= 0:
            cv2.line(ori_img, (x, int(cmy)), (x + width, int(cmy)), (0, 255, 0), params.line_thickness)
            cv2.line(wback, (x, int(cmy)), (x + width, int(cmy)), (0, 255, 0), params.line_thickness)
        elif x_coor - x > 0:
            width_1 = x_coor - x
            if width - width_1 <= 0:
                cv2.line(ori_img, (x, int(cmy)), (x + width, int(cmy)), (255, 0, 0), params.line_thickness)
                cv2.line(wback, (x, int(cmy)), (x + width, int(cmy)), (255, 0, 0), params.line_thickness)
            else:
                cv2.line(ori_img, (x_coor + 2, int(cmy)), (x_coor + width_left_bound, int(cmy)), (255, 0, 0),
                         params.line_thickness)
                cv2.line(ori_img, (x_coor + 2, int(cmy)), (x_coor - width_right_bound, int(cmy)), (0, 255, 0),
                         params.line_thickness)
                cv2.line(wback, (x_coor + 2, int(cmy)), (x_coor + width_left_bound, int(cmy)), (255, 0, 0),
                         params.line_thickness)
                cv2.line(wback, (x_coor + 2, int(cmy)), (x_coor - width_right_bound, int(cmy)), (0, 255, 0),
                         params.line_thickness)

    outputs.add_observation(sample=label, variable='vertical_reference_position', trait='vertical reference position',
                            method='plantcv.plantcv.analyze.bound_vertical', scale='none', datatype=int,
                            value=line_position, label='none')
    outputs.add_observation(sample=label, variable='width_left_reference', trait='width left of reference',
                            method='plantcv.plantcv.analyze.bound_vertical', scale='pixels', datatype=int,
                            value=width_left_bound, label='pixels')
    outputs.add_observation(sample=label, variable='width_right_reference', trait='width right of reference',
                            method='plantcv.plantcv.analyze.bound_vertical', scale='pixels', datatype=int,
                            value=width_right_bound, label='pixels')
    outputs.add_observation(sample=label, variable='area_left_reference', trait='area left of reference',
                            method='plantcv.plantcv.analyze.bound_vertical', scale='pixels', datatype=int,
                            value=left_bound_area, label='pixels')
    outputs.add_observation(sample=label, variable='percent_area_left_reference',
                            trait='percent area left of reference', method='plantcv.plantcv.analyze.bound_vertical',
                            scale='none', datatype=float,
                            value=percent_bound_area_left, label='none')
    outputs.add_observation(sample=label, variable='area_right_reference', trait='area right of reference',
                            method='plantcv.plantcv.analyze.bound_vertical', scale='pixels', datatype=int,
                            value=right_bound_area, label='pixels')
    outputs.add_observation(sample=label, variable='percent_area_right_reference',
                            trait='percent area right of reference', method='plantcv.plantcv.analyze.bound_vertical',
                            scale='none', datatype=float, value=percent_bound_area_right, label='none')

    # Store images
    outputs.images.append(analysis_images)

    return ori_img
