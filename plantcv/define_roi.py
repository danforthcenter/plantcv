# View and Adjust ROI

import sys
import cv2
import numpy as np
from . import print_image
from . import plot_image
from . import fatal_error


def define_roi(img, shape, device, roi=None, roi_input='default', debug=None, adjust=False, x_adj=0, y_adj=0,
               w_adj=0, h_adj=0):
    """Define a region of interest.

    Inputs:
    img       = img to overlay roi
    roi       = default (None) or user input ROI image, object area should be white and background should be black,
                has not been optimized for more than one ROI
    roi_input = type of file roi_base is, either 'binary', 'rgb', or 'default' (no ROI inputted)
    shape     = desired shape of final roi, either 'rectangle' or 'circle', if  user inputs rectangular roi but chooses
                'circle' for shape then a circle is fitted around rectangular roi (and vice versa)
    device    = device number.  Used to count steps in the pipeline
    debug     = None, print, or plot. Print = save to file, Plot = print to screen.
    adjust    = either 'True' or 'False', if 'True' allows user to adjust ROI
    x_adj     = adjust center along x axis
    y_adj     = adjust center along y axis
    w_adj     = adjust width
    h_adj     = adjust height

    Returns:
    device    = device number
    contour   = object contour list
    hierarchy = contour hierarchy list

    :param img: numpy array
    :param shape: str
    :param device: int
    :param roi: numpy array
    :param roi_input: str
    :param debug: str
    :param adjust: bool
    :param x_adj: int
    :param y_adj: int
    :param w_adj: int
    :param h_adj: int
    :return device: int
    :return contour: list
    :return hierarchy: list
    """

    device += 1
    ori_img = np.copy(img)
    if len(np.shape(img)) == 3:
        ix, iy, iz = np.shape(img)
    else:
        ix, iy = np.shape(img)

    # Allows user to use the default ROI or input their own RGB or binary image (made with imagej or some other program)
    #  as a base ROI (that can be adjusted below)
    if roi_input == 'rgb':
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        ret, v_img = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY)
        roi_contour, hierarchy = cv2.findContours(v_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    elif roi_input == 'binary':
        roi_contour, hierarchy = cv2.findContours(roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    elif roi_input == 'default':
        size = ix, iy
        roi_background = np.zeros(size, dtype=np.uint8)
        roi_size = (ix - 5), (iy - 5)
        roi = np.zeros(roi_size, dtype=np.uint8)
        roi1 = roi + 1
        roi_contour, roi_heirarchy = cv2.findContours(roi1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
        cv2.drawContours(roi_background, roi_contour[0], -1, (255, 0, 0), 5)
        if adjust == True:
            if (x_adj > 0 and w_adj > 0) or (y_adj > 0 and h_adj > 0) or (x_adj < 0 or y_adj < 0):
                fatal_error('Adjusted ROI position is out of frame, this will cause problems in detecting objects')
    else:
        fatal_error('ROI Input' + str(roi_input) + ' is not "binary", "rgb" or "default roi"!')

    # If the ROI is exactly in the 'correct' position
    if adjust == False:
        for cnt in roi_contour:
            size = ix, iy, 3
            background = np.zeros(size, dtype=np.uint8)
            if shape == 'rectangle':
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(background, (x, y), (x + w, y + h), (0, 255, 0), 5)
                rect = cv2.cvtColor(background, cv2.COLOR_RGB2GRAY)
                rect_contour, hierarchy = cv2.findContours(rect, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
                cv2.drawContours(ori_img, rect_contour[0], -1, (255, 0, 0), 5)
                if debug == 'print':
                    print_image(ori_img, (str(device) + '_roi.png'))
                elif debug == 'plot':
                    plot_image(ori_img)
                return device, rect_contour, hierarchy
            elif shape == 'circle':
                x, y, w, h = cv2.boundingRect(cnt)
                center = (int(w / 2), int(h / 2))
                if h > w:
                    radius = int(w / 2)
                    cv2.circle(background, center, radius, (255, 255, 255), -1)
                    circle = cv2.cvtColor(background, cv2.COLOR_RGB2GRAY)
                    circle_contour, hierarchy = cv2.findContours(circle, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
                    cv2.drawContours(ori_img, circle_contour[0], -1, (255, 0, 0), 5)
                    if debug == 'print':
                        print_image(ori_img, (str(device) + '_roi.png'))
                    elif debug == 'plot':
                        plot_image(ori_img)
                    return device, circle_contour, hierarchy
                else:
                    radius = int(h / 2)
                    cv2.circle(background, center, radius, (255, 255, 255), -1)
                    circle = cv2.cvtColor(background, cv2.COLOR_RGB2GRAY)
                    circle_contour, hierarchy = cv2.findContours(circle, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
                    cv2.drawContours(ori_img, circle_contour[0], -1, (255, 0, 0), 5)
                    if debug == 'print':
                        print_image(ori_img, (str(device) + '_roi.png'))
                    elif debug == 'plot':
                        plot_image(ori_img)
                    return device, circle_contour, hierarchy
            elif shape == 'ellipse':
                x, y, w, h = cv2.boundingRect(cnt)
                center = (int(w / 2), int(h / 2))
                if w > h:
                    cv2.ellipse(background, center, (w / 2, h / 2), 0, 0, 360, (0, 255, 0), 2)
                    ellipse = cv2.cvtColor(background, cv2.COLOR_RGB2GRAY)
                    ellipse_contour, hierarchy = cv2.findContours(ellipse, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
                    cv2.drawContours(ori_img, ellipse_contour[0], -1, (255, 0, 0), 5)
                    if debug == 'print':
                        print_image(ori_img, (str(device) + '_roi.png'))
                    elif debug == 'plot':
                        plot_image(ori_img)
                    return device, ellipse_contour, hierarchy
                else:
                    cv2.ellipse(ori_img, center, (h / 2, w / 2), 0, 0, 360, (0, 255, 0), 2)
                    cv2.ellipse(background, center, (h / 2, w / 2), 0, 0, 360, (0, 255, 0), 2)
                    ellipse = cv2.cvtColor(background, cv2.COLOR_RGB2GRAY)
                    ellipse_contour, hierarchy = cv2.findContours(ellipse, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
                    cv2.drawContours(ori_img, ellipse_contour[0], -1, (255, 0, 0), 5)
                    if debug == 'print':
                        print_image(ori_img, (str(device) + '_roi.png'))
                    elif debug == 'plot':
                        plot_image(ori_img)
                    return device, ellipse_contour, hierarchy
            else:
                fatal_error('Shape' + str(shape) + ' is not "rectangle", "circle", or "ellipse"!')

                # If the user wants to change the size of the ROI or adjust ROI position
    if adjust == True:
        if debug is not None:
            sys.stderr.write(
                'WARNING: Make sure ROI is COMPLETELY in frame or object detection will not perform properly\n')
        if x_adj == 0 and y_adj == 0 and w_adj == 0 and h_adj == 0:
            fatal_error('If adjust is true then x_adj, y_adj, w_adj or h_adj must have a non-zero value')
        else:
            for cnt in roi_contour:
                size = ix, iy, 3
                background = np.zeros(size, dtype=np.uint8)
                if shape == 'rectangle':
                    x, y, w, h = cv2.boundingRect(cnt)
                    x1 = x + x_adj
                    y1 = y + y_adj
                    w1 = w + w_adj
                    h1 = h + h_adj
                    cv2.rectangle(background, (x1, y1), (x + w1, y + h1), (0, 255, 0), 1)
                    rect = cv2.cvtColor(background, cv2.COLOR_RGB2GRAY)
                    rect_contour, hierarchy = cv2.findContours(rect, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
                    cv2.drawContours(ori_img, rect_contour[0], -1, (255, 0, 0), 5)
                    if debug == 'print':
                        print_image(ori_img, (str(device) + '_roi.png'))
                    elif debug == 'plot':
                        plot_image(ori_img)
                    return device, rect_contour, hierarchy
                elif shape == 'circle':
                    x, y, w, h = cv2.boundingRect(cnt)
                    x1 = x + x_adj
                    y1 = y + y_adj
                    w1 = w + w_adj
                    h1 = h + h_adj
                    center = (int((w + x1) / 2), int((h + y1) / 2))
                    if h > w:
                        radius = int(w1 / 2)
                        cv2.circle(background, center, radius, (255, 255, 255), -1)
                        circle = cv2.cvtColor(background, cv2.COLOR_RGB2GRAY)
                        circle_contour, hierarchy = cv2.findContours(circle, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
                        cv2.drawContours(ori_img, circle_contour[0], -1, (255, 0, 0), 5)
                        if debug == 'print':
                            print_image(ori_img, (str(device) + '_roi.png'))
                        elif debug == 'plot':
                            plot_image(ori_img)
                        return device, circle_contour, hierarchy
                    else:
                        radius = int(h1 / 2)
                        cv2.circle(background, center, radius, (255, 255, 255), -1)
                        circle = cv2.cvtColor(background, cv2.COLOR_RGB2GRAY)
                        circle_contour, hierarchy = cv2.findContours(circle, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
                        cv2.drawContours(ori_img, circle_contour[0], -1, (255, 0, 0), 5)
                        if debug == 'print':
                            print_image(ori_img, (str(device) + '_roi.png'))
                        elif debug == 'plot':
                            plot_image(ori_img)
                        return device, circle_contour, hierarchy
                elif shape == 'ellipse':
                    x, y, w, h = cv2.boundingRect(cnt)
                    x1 = x + x_adj
                    y1 = y + y_adj
                    w1 = w + w_adj
                    h1 = h + h_adj
                    center = (int((w + x1) / 2), int((h + y1) / 2))
                    if w > h:
                        cv2.ellipse(background, center, (w1 / 2, h1 / 2), 0, 0, 360, (0, 255, 0), 2)
                        ellipse = cv2.cvtColor(background, cv2.COLOR_RGB2GRAY)
                        ellipse_contour, hierarchy = cv2.findContours(ellipse, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
                        cv2.drawContours(ori_img, ellipse_contour[0], -1, (255, 0, 0), 5)
                        if debug == 'print':
                            print_image(ori_img, (str(device) + '_roi.png'))
                        elif debug == 'plot':
                            plot_image(ori_img)
                        return device, ellipse_contour, hierarchy
                    else:
                        cv2.ellipse(background, center, (h1 / 2, w1 / 2), 0, 0, 360, (0, 255, 0), 2)
                        ellipse = cv2.cvtColor(background, cv2.COLOR_RGB2GRAY)
                        ellipse_contour, hierarchy = cv2.findContours(ellipse, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                        cv2.drawContours(ori_img, ellipse_contour[0], -1, (255, 0, 0), 5)
                        if debug == 'print':
                            print_image(ori_img, (str(device) + '_roi.png'))
                        elif debug == 'plot':
                            plot_image(ori_img)
                        return device, ellipse_contour, hierarchy
                else:
                    fatal_error('Shape' + str(shape) + ' is not "rectangle", "circle", or "ellipse"!')
