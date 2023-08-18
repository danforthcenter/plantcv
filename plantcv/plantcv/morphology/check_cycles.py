"""Check for cycles in a skeleton image."""
import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import erode
from plantcv.plantcv import dilate
from plantcv.plantcv import outputs
from plantcv.plantcv import color_palette
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _cv2_findcontours


def check_cycles(skel_img, label=None):
    """Check for cycles in a skeleton image.

    Inputs:
    skel_img     = Skeletonized image
    label        = Optional label parameter, modifies the variable name of
                   observations recorded (default = pcv.params.sample_label).

    Returns:
    cycle_img    = Image with cycles identified

    :param skel_img: numpy.ndarray
    :param label: str
    :return cycle_img: numpy.ndarray
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

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
    cycle_objects, cycle_hierarchies = _cv2_findcontours(bin_img=just_cycles)

    # Count the number of holes
    num_cycles = len(cycle_objects)

    # Make debugging image
    cycle_img = skel_img.copy()
    cycle_img = dilate(cycle_img, params.line_thickness, 1)
    cycle_img = cv2.cvtColor(cycle_img, cv2.COLOR_GRAY2RGB)
    if num_cycles > 0:
        # Get a new color scale
        rand_color = color_palette(num=num_cycles, saved=False)
        for i in range(0, len(cycle_objects)):
            cv2.drawContours(cycle_img, cycle_objects, i, rand_color[i], params.line_thickness, lineType=8,
                             hierarchy=cycle_hierarchies)

    # Store Cycle Data
    outputs.add_observation(sample=label, variable='num_cycles', trait='number of cycles',
                            method='plantcv.plantcv.morphology.check_cycles', scale='none', datatype=int,
                            value=int(num_cycles), label='none')

    # Reset debug mode
    params.debug = debug

    _debug(visual=cycle_img, filename=os.path.join(params.debug_outdir, f"{params.device}_cycles.png"))

    return cycle_img
