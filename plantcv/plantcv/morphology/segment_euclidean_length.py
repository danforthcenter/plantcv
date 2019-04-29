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



def segment_euclidean_length(segmented_img, objects, hierarchies):
    """ Use segmented skeleton image to gather euclidean length measurements per segment

        Inputs:
        segmented_img = Segmented image to plot lengths on
        objects       = List of contours
        hierarchy     = Contour hierarchy NumPy array

        Returns:
        eu_length_header = Segment euclidean length data header
        eu_length_data   = Segment euclidean length data values
        labeled_img      = Segmented debugging image with lengths labeled

        :param segmented_img: numpy.ndarray
        :param objects: list
        :param hierarchy: numpy.ndarray
        :return labeled_img: numpy.ndarray
        :return eu_length_header: list
        :return eu_length_data: list

        """
    # Store debug
    debug = params.debug
    params.debug = None

    x_list = []
    y_list = []
    segment_lengths = []
    rand_color = color_palette(len(objects))


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
        for t in tip_objects:
            # Gather pairs of coordinates
            x, y = t.ravel()
            coord = (x, y)
            points.append(coord)

        # Draw euclidean distance lines
        cv2.line(labeled_img, points[0], points[1], rand_color[i], 1)

        # Calculate euclidean distance between tips of each contour
        segment_lengths.append(euclidean(points[0], points[1]))

    eu_length_header = ['HEADER_EU_LENGTH']
    eu_length_data = ['EU_LENGTH_DATA']
    # Put labels of length
    for c, value in enumerate(segment_lengths):
        text = "{:.2f}".format(value)
        w = x_list[c]
        h = y_list[c]
        cv2.putText(img=labeled_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=.4,
                    color=(150, 150, 150), thickness=1)
        segment_label = "ID" + str(c)
        eu_length_header.append(segment_label)
        eu_length_data.append(segment_lengths[c])

    if 'morphology_data' not in outputs.measurements:
        outputs.measurements['morphology_data'] = {}
    outputs.measurements['morphology_data']['segment_eu_lengths'] = segment_lengths

    # Reset debug mode
    params.debug = debug
    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img, os.path.join(params.debug_outdir, str(params.device) + '_segment_eu_lengths.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return eu_length_header, eu_length_data, labeled_img
