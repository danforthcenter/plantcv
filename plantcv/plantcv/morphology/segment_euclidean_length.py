# Find euclidean lenghts of skeleton segments

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import find_objects
from scipy.spatial.distance import euclidean
from plantcv.plantcv.morphology import find_tips



def segment_euclidean_length(segmented_img, objects, hierarchies):
    """ Use segmented skeleton image to gather measurements per segment

        Inputs:
        segmented_img = Segmented image to plot lengths on
        objects       = List of contours

        Returns:
        labeled_img   = Segmented debugging image with lengths labeled
        leaf_lengths  = List of leaf lengths

        :param segmented_img: numpy.ndarray
        :param objects: list
        :return labeled_img: numpy.ndarray
        :return leaf_lengths: list

        """
    # Store debug
    debug = params.debug

    # Don't print/plot the debug images from plantcv functions
    params.debug = None

    x_list = []
    y_list = []
    leaf_lengths = []
    labeled_img = segmented_img.copy()

    for i, cnt in enumerate(objects):
        # Store coordinates for labels
        x_list.append(objects[i][0][0][0])
        y_list.append(objects[i][0][0][1])

        # Draw segments one by one to group segment tips together
        finding_tips_img = np.zeros(segmented_img.shape[:2], np.uint8)
        cv2.drawContours(finding_tips_img, objects, i, (255, 255, 255), 1, lineType=8,
                         hierarchy=hierarchies)
        segment_tips = find_tips(finding_tips_img)
        tip_objects, tip_hierarchies = find_objects(segment_tips, segment_tips)
        points = []
        if not len(tip_objects) == 2:
            fatal_error("Too many tips found per segment, try pruning again")
        for i in tip_objects:
            # Gather pairs of coordinates
            x, y = i.ravel()
            coord = (x, y)
            points.append(coord)

        # Calculate euclidean distance between tip
        leaf_lengths.append(euclidean(points[0], points[1]))

        # Draw euclidean distance lines
        cv2.line(labeled_img, points[0], points[1], (20, 20, 20), 2)

    # Put labels of length
    for c, value in enumerate(leaf_lengths):
        text = "id:{} length:{:.1f}".format(c, value)
        w = x_list[c]
        h = y_list[c]
        cv2.putText(img=labeled_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=.4,
                    color=(255, 255, 255), thickness=1)

    # Reset debug mode
    params.debug = debug

    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img, os.path.join(params.debug_outdir, str(params.device) + '_segmented_eu_lengths.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return labeled_img, leaf_lengths
