# Find euclidean lengths of skeleton segments

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import find_objects
from plantcv.plantcv import color_palette
from scipy.spatial.distance import euclidean
from plantcv.plantcv.morphology import find_tips


def segment_euclidean_length(segmented_img, objects, label="default"):
    """ Use segmented skeleton image to gather euclidean length measurements per segment

        Inputs:
        segmented_img = Segmented image to plot lengths on
        objects       = List of contours
        label         = optional label parameter, modifies the variable name of observations recorded

        Returns:
        labeled_img      = Segmented debugging image with lengths labeled

        :param segmented_img: numpy.ndarray
        :param objects: list
        :param label: str
        :return labeled_img: numpy.ndarray

        """
    x_list = []
    y_list = []
    segment_lengths = []
    # Create a color scale, use a previously stored scale if available
    rand_color = color_palette(num=len(objects), saved=True)

    labeled_img = segmented_img.copy()
    # Store debug
    debug = params.debug
    params.debug = None

    for i, cnt in enumerate(objects):
        # Store coordinates for labels
        x_list.append(objects[i][0][0][0])
        y_list.append(objects[i][0][0][1])

        # Draw segments one by one to group segment tips together
        finding_tips_img = np.zeros(segmented_img.shape[:2], np.uint8)
        cv2.drawContours(finding_tips_img, objects, i, (255, 255, 255), 1, lineType=8)
        segment_tips = find_tips(finding_tips_img)
        tip_objects, tip_hierarchies = find_objects(segment_tips, segment_tips)
        points = []
        if not len(tip_objects) == 2:
            fatal_error("Too many tips found per segment, try pruning again")
        for t in tip_objects:
            # Gather pairs of coordinates
            x, y = t.ravel()
            coord = (x, y)
            points.append(coord)

        # Draw euclidean distance lines
        cv2.line(labeled_img, points[0], points[1], rand_color[i], 1)

        # Calculate euclidean distance between tips of each contour
        segment_lengths.append(float(euclidean(points[0], points[1])))

    segment_ids = []
    # Reset debug mode
    params.debug = debug

    # Put labels of length
    for c, value in enumerate(segment_lengths):
        text = "{:.2f}".format(value)
        w = x_list[c]
        h = y_list[c]
        cv2.putText(img=labeled_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=params.text_size, color=(150, 150, 150), thickness=params.text_thickness)
        # segment_label = "ID" + str(c)
        segment_ids.append(c)

    outputs.add_observation(sample=label, variable='segment_eu_length', trait='segment euclidean length',
                            method='plantcv.plantcv.morphology.segment_euclidean_length', scale='pixels', datatype=list,
                            value=segment_lengths, label=segment_ids)

    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img, os.path.join(params.debug_outdir, str(params.device) + '_segment_eu_lengths.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return labeled_img
