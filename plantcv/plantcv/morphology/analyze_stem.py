# Analyze stem characteristics

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image


def analyze_stem(rgb_img, stem_objects, label="default"):
    """ Calculate angle of segments (in degrees) by fitting a linear regression line to segments.

        Inputs:
        rgb_img       = RGB image to plot debug image
        stem_objects  = List of stem segments (output from segment_sort function)
        label        = optional label parameter, modifies the variable name of observations recorded

        Returns:
        labeled_img    = Stem analysis debugging image


        :param rgb_img: numpy.ndarray
        :param stem_objects: list
        :param label: str
        :return labeled_img: numpy.ndarray
    """
    params.device += 1
    labeled_img = np.copy(rgb_img)
    img_x, img_y, _ = np.shape(labeled_img)
    grouped_stem = np.vstack(stem_objects)

    # Find vertical height of the stem by measuring bounding box
    stem_x, stem_y, width, height = cv2.boundingRect(grouped_stem)

    # Calculate stem angle
    [vx, vy, x, y] = cv2.fitLine(grouped_stem, cv2.DIST_L2, 0, 0.01, 0.01)
    slope = -vy / vx

    # Calculate stem path length
    stem_length = cv2.arcLength(grouped_stem, False) / 2

    outputs.add_observation(sample=label, variable='stem_height', trait='vertical length of stem segments',
                            method='plantcv.plantcv.morphology.analyze_stem', scale='pixels', datatype=float,
                            value=height, label=None)
    outputs.add_observation(sample=label, variable='stem_angle', trait='angle of combined stem object',
                            method='plantcv.plantcv.morphology.analyze_stem', scale='degrees', datatype=float,
                            value=float(slope), label=None)
    outputs.add_observation(sample=label, variable='stem_length', trait='path length of combined stem object',
                            method='plantcv.plantcv.morphology.analyze_stem', scale='None', datatype=float,
                            value=stem_length, label=None)

    if params.debug is not None:
        # Draw culm_height
        cv2.line(labeled_img, (int(stem_x), stem_y), (int(stem_x), stem_y + height), (0, 255, 0), params.line_thickness)
        # Draw combined stem angle
        x_min = 0  # Set bounds for regression lines to get drawn
        x_max = img_x
        intercept1 = int(((x - x_min) * slope) + y)
        intercept2 = int(((x - x_max) * slope) + y)
        if slope > 1000000 or slope < -1000000:
            print("Slope  is ", slope, " and cannot be plotted.")
        else:
            cv2.line(labeled_img, (x_max - 1, intercept2), (x_min, intercept1), (0, 0, 255), 1)
        if params.debug == 'print':
            print_image(labeled_img, os.path.join(params.debug_outdir, str(params.device) + 'stem_analze.png'))
        elif params.debug == 'plot':
            plot_image(labeled_img)

    return labeled_img
