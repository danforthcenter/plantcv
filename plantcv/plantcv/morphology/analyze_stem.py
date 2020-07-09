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


def analyze_stem(stem_objects, segmented_img, mask=None):
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



    outputs.add_observation(variable='culm_height', trait='vertical length of stem segments',
                            method='plantcv.plantcv.morphology.analyze_stem', scale='pixels', datatype=float,
                            value=culm_height, label=None)

    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img, os.path.join(params.debug_outdir, str(params.device) + '_segmented_angles.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return labeled_img
