# Analyze stem characteristics

import os
import cv2
import numpy as np
import pandas as pd
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import color_palette


def analyze_stem(stem_objects, segmented_img, mask=mask):
    """ Calculate angle of segments (in degrees) by fitting a linear regression line to segments.

        Inputs:
        stem_objects  =
        mask          =

        Returns:
        labeled_img    = Segmented debugging image with angles labeled


        :param stem_objects: list
        :param mask: numpy.ndarray
        :return labeled_img: numpy.ndarray
        """

    labeled_img = np.copy(segmented_img)
    img_x, img_y, _ = np.shape(labeled_img)
    grouped_stem = np.vstack(stem_objects)
    x, y, width, height = cv2.boundingRect(grouped_stem)

    x_max = img_x
    x_min = 0

    # Find line fit to each segment
    [vx, vy, x, y] = cv2.fitLine(grouped_stem, cv2.DIST_L2, 0, 0.01, 0.01)
    slope = -vy / vx
    left_list = int(((x - x_min) * slope) + y)
    right_list = int(((x - x_max) * slope) + y)

    outputs.add_observation(variable='stem_height', trait='vertical length of stem segments',
                            method='plantcv.plantcv.morphology.analyze_stem', scale='pixels', datatype=float,
                            value=height, label=None)
    outputs.add_observation(variable='stem_angle', trait='angle of combined stem object',
                            method='plantcv.plantcv.morphology.analyze_stem', scale='degrees', datatype=float,
                            value=slope, label=None)

    if params.debug is not None:
        params.device += 1
        # draw culm_height
        cv2.line(labeled_img, (int(x), y), (int(x), y + height), (0, 255, 0), params.line_thickness)
        # draw combined stem angle
        if slope > 1000000 or slope < -1000000:
            print("Slope  is ", slope, " and cannot be plotted.")
        else:
            # Draw slope lines
            cv2.line(labeled_img, (x_max - 1, right_list), (x_min, left_list), (0, 0, 255), 1)

    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img, os.path.join(params.debug_outdir, str(params.device) + '_segmented_angles.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return labeled_img
