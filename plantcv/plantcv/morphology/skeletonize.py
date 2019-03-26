# Binary image -> Skeleton

import os
from plantcv.plantcv import params
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv.threshold import binary
from skimage.morphology import skeletonize


def skeletonize(mask):
    """Reduces binary objects to 1 pixel wide representations (skeleton)

    Inputs:
    mask       = Binary image data

    Returns:
    skeleton   = skeleton image

    :param bin_img: numpy.ndarray
    :return skeleton: numpy.ndarray
    """
    # Store debug
    debug = params.debug

    # Don't print/plot the binary image
    params.debug = None

    # Convert mask to 0 and 1 rather than 0 and 255
    binary_img = binary(mask, 2, 1) # should we ask users for bin_img or mask??

    skeleton = skeletonize(binary_img)

    # Auto-increment device
    params.device += 1

    # Reset debug mode
    params.debug = debug

    if params.debug == 'print':
        print_image(skeleton, os.path.join(params.debug_outdir, str(params.device) + '_skeleton.png'))
    elif params.debug == 'plot':
        plot_image(skeleton, cmap='gray')

    return skeleton
