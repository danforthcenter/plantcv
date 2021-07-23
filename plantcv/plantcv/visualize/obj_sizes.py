# Visualize an annotated image with object sizes

import os
import cv2
import random
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import color_palette
from plantcv.plantcv._debug import _debug


def obj_sizes(img, mask, num_objects=100):
    """
    Label the size of objects in an image.

    Inputs:
    img          = RGB or grayscale image data
    mask         = Binary mask made from selected contours
    num_objects  = Optional parameter to limit the number of objects that will get annotated.

    Returns:
    plotting_img = Plotting image with objects labeled by area

    :param img: numpy.ndarray
    :param mask: numpy.ndarray
    :param num_objects: int
    :return plotting_img: numpy.ndarray
    """
    plotting_img = np.copy(img)
    # Convert grayscale images to color
    if len(np.shape(plotting_img)) == 2:
        plotting_img = cv2.cvtColor(plotting_img, cv2.COLOR_GRAY2BGR)

    # Store debug
    debug = params.debug
    params.debug = None

    # ID contours and sort them from largest to smallest
    id_objects, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    sorted_objects = sorted(id_objects, key=lambda x: cv2.contourArea(x))
    # Function sorts smallest to largest so keep the last X objects listed
    # sorted_objects = sorted_objects[len(sorted_objects) - num_objects: len(sorted_objects)]
    # Reverse the sorted list to order contours from largest to smallest
    sorted_objects.reverse()

    rand_color = color_palette(num=num_objects, saved=False)
    random.shuffle(rand_color)

    label_coord_x = []
    label_coord_y = []
    area_vals = []

    for i, contour in enumerate(sorted_objects):
        # Break out of the for loop once the number of objects have been plotted
        if i >= num_objects:
            break
        # ID and store area values and centers of mass for labeling them
        m = cv2.moments(contour)
        # Skip iteration if contour area is zero
        # This is needed because cv2.contourArea can be > 0 while moments area is 0.
        if m['m00'] == 0:
            continue
        area_vals.append(m['m00'])
        label_coord_x.append(int(m["m10"] / m["m00"]))
        label_coord_y.append(int(m["m01"] / m["m00"]))
        # Fill in objects with color
        cv2.drawContours(plotting_img, sorted_objects, i, rand_color[i], thickness=-1)

    # Label with area values
    for c, value in enumerate(area_vals):
        text = "{:.0f}".format(value)
        w = label_coord_x[c]
        h = label_coord_y[c]
        cv2.putText(img=plotting_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=params.text_size, color=(150, 150, 150), thickness=params.text_thickness)
    print(f"There were {max(0, len(id_objects) - num_objects)} objects not annotated.")

    params.debug = debug

    _debug(visual=plotting_img, filename=os.path.join(params.debug_outdir, str(params.device) + '_object_sizes.png'))

    return plotting_img
