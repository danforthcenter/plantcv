# Check for cycles in a skeleton image

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import erode
from plantcv.plantcv import dilate
from plantcv.plantcv import outputs
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import find_objects
from plantcv.plantcv import color_palette


def check_cycles(skel_img, label="default"):
    """ Check for cycles in a skeleton image
    Inputs:
    skel_img     = Skeletonized image
    label        = optional label parameter, modifies the variable name of observations recorded

    Returns:
    cycle_img    = Image with cycles identified

    :param skel_img: numpy.ndarray
    :param label: str
    :return cycle_img: numpy.ndarray
    """

    # Create the mask needed for cv2.floodFill, must be larger than the image
    h, w = skel_img.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    # Copy the skeleton since cv2.floodFill will draw on it
    skel_copy = skel_img.copy()
    cv2.floodFill(skel_copy, mask=mask, seedPoint=(0, 0), newVal=255)

    # Invert so the holes are white and background black
    just_cycles = cv2.bitwise_not(skel_copy)

    # Store debug
    debug = params.debug
    params.debug = None

    # Erode slightly so that cv2.findContours doesn't think diagonal pixels are separate contours
    just_cycles = erode(just_cycles, 2, 1)

    # Use pcv.find_objects to turn plots of holes into countable contours
    cycle_objects, cycle_hierarchies = find_objects(just_cycles, just_cycles)

    # Count the number of holes
    num_cycles = len(cycle_objects)

    # Make debugging image
    cycle_img = skel_img.copy()
    cycle_img = dilate(cycle_img, params.line_thickness, 1)
    cycle_img = cv2.cvtColor(cycle_img, cv2.COLOR_GRAY2RGB)
    if num_cycles > 0:
        # Get a new color scale
        rand_color = color_palette(num=num_cycles, saved=False)
        for i, cnt in enumerate(cycle_objects):
            cv2.drawContours(cycle_img, cycle_objects, i, rand_color[i], params.line_thickness, lineType=8,
                             hierarchy=cycle_hierarchies)

    # Store Cycle Data
    outputs.add_observation(sample=label, variable='num_cycles', trait='number of cycles',
                            method='plantcv.plantcv.morphology.check_cycles', scale='none', datatype=int,
                            value=int(num_cycles), label='none')

    # Reset debug mode
    params.debug = debug
    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(cycle_img, os.path.join(params.debug_outdir, str(params.device) + '_cycles.png'))
    elif params.debug == 'plot':
        plot_image(cycle_img)

    return cycle_img
