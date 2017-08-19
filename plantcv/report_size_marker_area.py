# Analyzes an object and outputs numeric properties

import cv2
import numpy as np
from . import fatal_error
from . import print_image
from . import plot_image
from . import rgb2gray_hsv
from . import find_objects
from . import binary_threshold
from . import define_roi
from . import roi_objects
from . import object_composition


def report_size_marker_area(img, shape, device, debug, marker='define', x_adj=0, y_adj=0, w_adj=0, h_adj=0,
                            base='white', objcolor='dark', thresh_channel=None, thresh=None, filename=False):
    """Outputs numeric properties for an input object (contour or grouped contours).

    Inputs:
    img             = image object (most likely the original), color(RGB)
    shape           = 'rectangle', 'circle', 'ellipse'
    device          = device number. Used to count steps in the pipeline
    debug           = None, print, or plot. Print = save to file, Plot = print to screen.
    marker          = define or detect, if define it means you set an area, if detect it means you want to
                      detect within an area
    x_adj           = x position of shape, integer
    y_adj           = y position of shape, integer
    w_adj           = width
    h_adj           = height
    base            = background color 'white' is default
    objcolor        = object color is 'dark' or 'light'
    thresh_channel  = 'h', 's','v'
    thresh          = integer value
    filename        = name of file

    Returns:
    device          = device number
    marker_header    = shape data table headers
    marker_data      = shape data table values
    analysis_images = list of output images

    :param img: numpy array
    :param shape: str
    :param device: int
    :param debug: str
    :param marker: str
    :param x_adj:int
    :param y_adj:int
    :param w_adj:int
    :param h_adj:int
    :param h_adj:int
    :param base:str
    :param objcolor: str
    :param thresh_channel:str
    :param thresh:int
    :param filename: str
    :return: device: int
    :return: marker_header: str
    :return: marker_data: int
    :return: analysis_images: list
    """

    device += 1
    ori_img = np.copy(img)
    if len(np.shape(img)) == 3:
        ix, iy, iz = np.shape(img)
    else:
        ix, iy = np.shape(img)

    size = ix, iy
    roi_background = np.zeros(size, dtype=np.uint8)
    roi_size = (ix - 5), (iy - 5)
    roi = np.zeros(roi_size, dtype=np.uint8)
    roi1 = roi + 1
    roi_contour, roi_heirarchy = cv2.findContours(roi1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    cv2.drawContours(roi_background, roi_contour[0], -1, (255, 0, 0), 5)

    if (x_adj > 0 and w_adj > 0) or (y_adj > 0 and h_adj > 0):
        fatal_error('Adjusted ROI position is out of frame, this will cause problems in detecting objects')

    for cnt in roi_contour:
        size1 = ix, iy, 3
        background = np.zeros(size1, dtype=np.uint8)
        if shape == 'rectangle' and (x_adj >= 0 and y_adj >= 0):
            x, y, w, h = cv2.boundingRect(cnt)
            x1 = x + x_adj
            y1 = y + y_adj
            w1 = w + w_adj
            h1 = h + h_adj
            cv2.rectangle(background, (x1, y1), (x + w1, y + h1), (1, 1, 1), -1)
        elif shape == 'circle':
            x, y, w, h = cv2.boundingRect(cnt)
            x1 = x + x_adj
            y1 = y + y_adj
            w1 = w + w_adj
            h1 = h + h_adj
            center = (int((w + x1) / 2), int((h + y1) / 2))
            if h > w:
                radius = int(w1 / 2)
                cv2.circle(background, center, radius, (1, 1, 1), -1)
            else:
                radius = int(h1 / 2)
                cv2.circle(background, center, radius, (1, 1, 1), -1)
        elif shape == 'ellipse':
            x, y, w, h = cv2.boundingRect(cnt)
            x1 = x + x_adj
            y1 = y + y_adj
            w1 = w + w_adj
            h1 = h + h_adj
            center = (int((w + x1) / 2), int((h + y1) / 2))
            if w > h:
                cv2.ellipse(background, center, (w1 / 2, h1 / 2), 0, 0, 360, (1, 1, 1), -1)
            else:
                cv2.ellipse(background, center, (h1 / 2, w1 / 2), 0, 0, 360, (1, 1, 1), -1)
        else:
            fatal_error('Shape' + str(shape) + ' is not "rectangle", "circle", or "ellipse"!')

    markerback = cv2.cvtColor(background, cv2.COLOR_RGB2GRAY)
    shape_contour, hierarchy = cv2.findContours(markerback, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    cv2.drawContours(ori_img, shape_contour, -1, (255, 255, 0), 5)
    
    if debug is 'print':
        print_image(ori_img, (str(device) + '_marker_roi.png'))
    elif debug is 'plot':
        plot_image(ori_img)

    if marker == 'define':
        m = cv2.moments(markerback, binaryImage=True)
        area = m['m00']
        device, id_objects, obj_hierarchy = find_objects(img, markerback, device, debug)
        device, obj, mask = object_composition(img, id_objects, obj_hierarchy, device, debug)
        center, axes, angle = cv2.fitEllipse(obj)
        major_axis = np.argmax(axes)
        minor_axis = 1 - major_axis
        major_axis_length = axes[major_axis]
        minor_axis_length = axes[minor_axis]
        eccentricity = np.sqrt(1 - (axes[minor_axis] / axes[major_axis]) ** 2)

    elif marker == 'detect':
        if thresh_channel is not None and thresh is not None:
            if base == 'white':
                masked = cv2.multiply(img, background)
                marker1 = markerback * 255
                mask1 = cv2.bitwise_not(marker1)
                markstack = np.dstack((mask1, mask1, mask1))
                added = cv2.add(masked, markstack)
            else:
                added = cv2.multiply(img, background)
            device, maskedhsv = rgb2gray_hsv(added, thresh_channel, device, debug)
            device, masked2a_thresh = binary_threshold(maskedhsv, thresh, 255, objcolor, device, debug)
            device, id_objects, obj_hierarchy = find_objects(added, masked2a_thresh, device, debug)
            device, roi1, roi_hierarchy = define_roi(added, shape, device, None, 'default', debug, True, x_adj, y_adj,
                                                     w_adj, h_adj)
            device, roi_o, hierarchy3, kept_mask, obj_area = roi_objects(img, 'partial', roi1, roi_hierarchy,
                                                                         id_objects, obj_hierarchy, device, debug)
            device, obj, mask = object_composition(img, roi_o, hierarchy3, device, debug)

            cv2.drawContours(ori_img, roi_o, -1, (0, 255, 0), -1, lineType=8, hierarchy=hierarchy3)
            m = cv2.moments(mask, binaryImage=True)
            area = m['m00']

            center, axes, angle = cv2.fitEllipse(obj)
            major_axis = np.argmax(axes)
            minor_axis = 1 - major_axis
            major_axis_length = axes[major_axis]
            minor_axis_length = axes[minor_axis]
            eccentricity = np.sqrt(1 - (axes[minor_axis] / axes[major_axis]) ** 2)

        else:
            fatal_error('thresh_channel and thresh must be defined in detect mode')
    else:
        fatal_error("marker must be either in 'detect' or 'define' mode")
    
    analysis_images = []
    if filename:
        out_file = str(filename[0:-4]) + '_sizemarker.jpg'
        print_image(ori_img, out_file)
        analysis_images.append(['IMAGE', 'marker', out_file])
    if debug is 'print':
        print_image(ori_img, (str(device) + '_marker_shape.png'))
    elif debug is 'plot':
        plot_image(ori_img)

    marker_header = (
        'HEADER_MARKER',
        'marker_area',
        'marker_major_axis_length',
        'marker_minor_axis_length',
        'marker_eccentricity'
    )

    marker_data = (
        'MARKER_DATA',
        area,
        major_axis_length,
        minor_axis_length,
        eccentricity
    )

    return device, marker_header, marker_data, analysis_images
