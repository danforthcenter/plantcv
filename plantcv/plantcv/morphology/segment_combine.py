# Plot segment ID numbers after combining segments

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import color_palette


def segment_combine(segment_list, objects, mask):
    """ Combine user specified segments together

            Inputs:
            segment_list  = List of segments to get combined, or list of lists of segments to get combined
            objects       = List of contours
            hierarchy     = Contour hierarchy NumPy array
            mask          = Binary mask for debugging image

            Returns:
            segmented_img = Segmented image
            objects       = Updated list of contours
            hierarchy     = Updated contour hierarchy NumPy array

            :param segment_list: list
            :param objects: list
            :param mask: numpy.ndarray
            :return labeled_img: numpy.ndarray
            :return objects: list
            """
    label_coord_x = []
    label_coord_y = []
    all_objects = objects[:]

    # If user provides a single list of objects to combine
    if type(segment_list[0]) is int:
        num_contours = len(segment_list)
        count = 1

        # Store the first object into the new object array
        new_objects = all_objects[segment_list[0]]
        # Remove the objects getting combined from the list of all objects
        all_objects.remove(objects[segment_list[0]])

        while count < num_contours:
            # Combine objects into a single array
            new_objects = np.append(new_objects, objects[segment_list[count]], 0)
            # Remove the objects getting combined from the list of all objects
            all_objects.remove(objects[segment_list[count]])
            count += 1
        # Replace with the combined object
        all_objects.append(new_objects)

    # If user provides a list of lists of objects to combine
    elif type(segment_list[0]) is list:
        # For each list provided
        for lists in segment_list:
            num_contours = len(lists)
            count = 1
            # Store the first object into the new object array
            new_objects = all_objects[lists[0]]
            # Remove the objects getting combined from the list of all objects
            all_objects.remove(objects[lists[0]])

            while count < num_contours:
                # Combine objects into a single array
                new_objects = np.append(new_objects, objects[lists[count]], 0)
                # Remove the objects getting combined from the list of all objects
                all_objects.remove(objects[lists[count]])
                count += 1
            # Add combined contour to list of all contours
            all_objects.append(new_objects)
    else:
        fatal_error("segment_list must be a list of object ID's or a list of lists of ID's!")

    labeled_img = mask.copy()
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_GRAY2RGB)

    # Color each segment a different color, use a previously saved scale if available
    rand_color = color_palette(num=len(all_objects), saved=True)

    # Plot all segment contours
    for i, cnt in enumerate(all_objects):
        cv2.drawContours(labeled_img, all_objects[i], -1, rand_color[i], params.line_thickness, lineType=8)
        # Store coordinates for labels
        label_coord_x.append(all_objects[i][0][0][0])
        label_coord_y.append(all_objects[i][0][0][1])

    # Label segments
    for i, cnt in enumerate(all_objects):
        w = label_coord_x[i]
        h = label_coord_y[i]
        text = "ID:{}".format(i)
        cv2.putText(img=labeled_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=params.text_size, color=rand_color[i], thickness=2)

    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img,
                    os.path.join(params.debug_outdir, str(params.device) + '_combined_segment_ids.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return labeled_img, all_objects
