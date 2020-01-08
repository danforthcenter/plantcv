# Count the number of tillers in grass like species of plants

import os
import cv2
import numpy as np
from plantcv.plantcv import dilate
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import find_objects
from plantcv.plantcv import color_palette


def count_tillers(skel_img, stem_objects):
    """ Estimate the number of tillers by plotting and counting the number of separate contours

    Inputs:
    skel_img     = Skeletonized image
    stem_objects = List of primary objects (stem)

    Returns:
    labeled_img = Debugging image with separate tillers labeled with different colors

    :param skel_img: numpy.ndarray
    :param stem_objects: list
    :return labeled_img: numpy.ndarray
    """

    # Store debug mode
    debug = params.debug
    params.debug = None

    plotting_img = np.zeros(skel_img.shape[:2], np.uint8)

    cv2.drawContours(plotting_img, stem_objects, -1, 255, params.line_thickness, lineType=8)
    dilated = dilate(gray_img=plotting_img, ksize=4, i=1)
    tiller_objects, _ = find_objects(img=skel_img, mask=dilated)
    num_tillers = len(tiller_objects)

    outputs.add_observation(variable='num_tillers', trait='estimated number of tillers',
                            method='plantcv.plantcv.morphology.count_tillers', scale='none', datatype=int,
                            value=num_tillers, label='none')

    rand_color = color_palette(num_tillers)
    print(np.shaoe(skel_img))
    labeled_img = cv2.cvtColor(skel_img.copy(), cv2.COLOR_GRAY2RGB)
    for i, cnt in enumerate(tiller_objects):
        labeled_img = cv2.drawContours(labeled_img, cnt, -1, rand_color[i],
                                         params.line_thickness, lineType=8)

    # Reset debug mode
    params.debug = debug

    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img,
                    os.path.join(params.debug_outdir, str(params.device) + '_tillers.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return labeled_img
