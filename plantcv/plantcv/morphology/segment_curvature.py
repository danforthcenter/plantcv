# Find curvature measure of skeleton segments

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import find_objects
from plantcv.plantcv import color_palette
from plantcv.plantcv.morphology import find_tips
from plantcv.plantcv.morphology import segment_path_length
from plantcv.plantcv.morphology import segment_euclidean_length


def segment_curvature(segmented_img, objects, label="default"):
    """ Calculate segment curvature as defined by the ratio between geodesic and euclidean distance.
        Measurement of two-dimensional tortuosity.

        Inputs:
        segmented_img     = Segmented image to plot lengths on
        objects           = List of contours
        label          = optional label parameter, modifies the variable name of observations recorded

        Returns:
        labeled_img        = Segmented debugging image with curvature labeled


        :param segmented_img: numpy.ndarray
        :param objects: list
        :param label: str
        :return labeled_img: numpy.ndarray

        """

    label_coord_x = []
    label_coord_y = []
    labeled_img = segmented_img.copy()

    # Store debug
    debug = params.debug
    params.debug = None

    _ = segment_euclidean_length(segmented_img, objects, label="backend")
    _ = segment_path_length(segmented_img, objects, label="backend")
    eu_lengths = outputs.observations['backend']['segment_eu_length']['value']
    path_lengths = outputs.observations['backend']['segment_path_length']['value']
    curvature_measure = [float(x / y) for x, y in zip(path_lengths, eu_lengths)]
    # Create a color scale, use a previously stored scale if available
    rand_color = color_palette(num=len(objects), saved=True)

    for i, cnt in enumerate(objects):
        # Store coordinates for labels
        label_coord_x.append(objects[i][0][0][0])
        label_coord_y.append(objects[i][0][0][1])

        # Draw segments one by one to group segment tips together
        finding_tips_img = np.zeros(segmented_img.shape[:2], np.uint8)
        cv2.drawContours(finding_tips_img, objects, i, (255, 255, 255), 1, lineType=8)
        segment_tips = find_tips(finding_tips_img)
        tip_objects, tip_hierarchies = find_objects(segment_tips, segment_tips)
        points = []

        for t in tip_objects:
            # Gather pairs of coordinates
            x, y = t.ravel()
            coord = (x, y)
            points.append(coord)

        # Draw euclidean distance lines
        cv2.line(labeled_img, points[0], points[1], rand_color[i], 1)

    segment_ids = []
    # Reset debug mode
    params.debug = debug

    for i, cnt in enumerate(objects):
        # Calculate geodesic distance
        text = "{:.3f}".format(curvature_measure[i])
        w = label_coord_x[i]
        h = label_coord_y[i]
        cv2.putText(img=labeled_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=params.text_size, color=(150, 150, 150), thickness=params.text_thickness)
        # segment_label = "ID" + str(i)
        segment_ids.append(i)

    outputs.add_observation(sample=label, variable='segment_curvature', trait='segment curvature',
                            method='plantcv.plantcv.morphology.segment_curvature', scale='none', datatype=list,
                            value=curvature_measure, label=segment_ids)

    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img, os.path.join(params.debug_outdir, str(params.device) + '_segment_curvature.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return labeled_img
