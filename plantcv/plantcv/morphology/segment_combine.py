# Plot segment ID numbers after combining segments

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import fatal_error
from plantcv.plantcv import color_palette
from plantcv.plantcv._debug import _debug


def segment_combine(segment_list, objects, mask):
    """Combine user specified segments together.

    Inputs:
    segment_list  = List of segment indices to get combined
    objects       = List of contours
    mask          = Binary mask for debugging image

    Returns:
    segmented_img = Segmented image
    objects       = Updated list of contours

    :param segment_list: list
    :param objects: list
    :param mask: numpy.ndarray
    :return labeled_img: numpy.ndarray
    :return objects: list
    """
    label_coord_x = []
    label_coord_y = []
    all_objects = objects[:]
    if type(segment_list[0]) is not int:
        fatal_error("segment_list must be a list of object ID's")
    segment_list_copy = sorted(segment_list, reverse=True)

    # If user provides a single list of objects to combine
    num_contours = len(segment_list)
    count = 1

    # Store the first object into the new object array
    combined_object = objects[segment_list_copy[0]]
    # Remove the objects getting combined from the list of all objects
    all_objects.pop(segment_list_copy[0])

    while count < num_contours:
        # Combine segments into a single object
        combined_object = np.append(combined_object, objects[segment_list_copy[count]], 0)
        # Remove the segment that was combined from the list of all objects
        all_objects.pop(segment_list_copy[count])
        count += 1
    # Replace with the combined object
    all_objects.append(combined_object)

    labeled_img = mask.copy()
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_GRAY2RGB)

    # Color each segment a different color, use a previously saved scale if available
    rand_color = color_palette(num=len(all_objects), saved=True)
    # Plot all segment contours
    for i, _ in enumerate(all_objects):
        cv2.drawContours(labeled_img, all_objects[i], -1, rand_color[i], params.line_thickness, lineType=8)
        # Store coordinates for labels
        label_coord_x.append(all_objects[i][0][0][0])
        label_coord_y.append(all_objects[i][0][0][1])

    # Label segments
    for i, _ in enumerate(all_objects):
        w = label_coord_x[i]
        h = label_coord_y[i]
        text = f"ID:{i}"
        cv2.putText(img=labeled_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=params.text_size, color=rand_color[i], thickness=2)

    _debug(visual=labeled_img, filename=os.path.join(params.debug_outdir, f"{params.device}_combined_segment_ids.png"))

    return labeled_img, all_objects
