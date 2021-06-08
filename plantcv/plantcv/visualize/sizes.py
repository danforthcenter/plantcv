# Visualize an annotated image with object sizes

import os
import cv2
import random
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import find_objects
from plantcv.plantcv import color_palette


def sizes(img, mask, num_objects=100):
    """ Visualize an RGB image in all potential colorspaces

    Inputs:
    img          = RGB or grayscale image data
    mask         = Binary mask made from selected contours
    num_objects  = Optional parameter to limit the number of objects that will get annotated.

    Returns:
    plotting_img = Plotting image containing the original image and L,A,B,H,S, and V colorspaces

    :param img: numpy.ndarray
    :param mask: numpy.ndarray
    :param num_objects: int
    :return plotting_img: numpy.ndarray
    """


    plotting_img = np.copy(img)

    # Store debug
    debug = params.debug
    params.debug = None

    id_objects, obj_hierarchy = find_objects(img=img, mask=mask)
    rand_color = color_palette(num=len(id_objects), saved=False)
    random.shuffle(rand_color)

    label_coord_x = []
    label_coord_y = []
    area_vals = []

    for i, cnt in enumerate(id_objects):
        # Calculate geodesic distance, divide by two since cv2 seems to be taking the perimeter of the contour
        area_vals.append(cv2.contourArea(cnt))
        cv2.drawContours(plotting_img, id_objects, i, rand_color[i], thickness=-1)
        # Store coordinates for labels
        label_coord_x.append(id_objects[i][0][0][0])
        label_coord_y.append(id_objects[i][0][0][1])

    segment_ids = []
    # Put labels of length
    for c, value in enumerate(area_vals):
        text = "{:.0f}".format(value)
        w = label_coord_x[c]
        h = label_coord_y[c]
        if c < int(num_objects):
            cv2.putText(img=plotting_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=params.text_size, color=(150, 150, 150), thickness=params.text_thickness)
        else:
            print("There were " + str(len(area_vals)-num_objects) + " objects not annotated.")
            break

    # Auto-increment device
    params.device += 1
    # Reset debug mode
    params.debug = debug

    if params.debug == 'print':
        print_image(plotting_img, os.path.join(params.debug_outdir, str(params.device) + '_object_sizes.png'))
    elif params.debug == 'plot':
        plot_image(plotting_img)

    return plotting_img
