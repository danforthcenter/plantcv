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


def analyze_stem(stem_objects, segmented_img):
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
    grouped_stem = np.vstack(stem_objects)
    x, y, width, height = cv2.boundingRect(grouped_stem)
    stem_base = x + (width/2)



    outputs.add_observation(variable='culm_height', trait='vertical length of stem segments',
                            method='plantcv.plantcv.morphology.analyze_stem', scale='pixels', datatype=float,
                            value=height, label=None)



    if params.debug is not None:
        params.device += 1

        cv2.line(labeled_img, (int(stem_base), y), (int(stem_base), y + height), (0, 255, 0), params.line_thickness)


    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img, os.path.join(params.debug_outdir, str(params.device) + '_segmented_angles.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)



    return labeled_img
