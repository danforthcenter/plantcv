# Binary image -> Skeleton

import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from skimage import morphology as skmorph


def skeletonize(mask):
    """Reduces binary objects to 1 pixel wide representations (skeleton)

    Inputs:
    mask       = Binary image data

    Returns:
    skeleton   = skeleton image

    :param mask: numpy.ndarray
    :return skeleton: numpy.ndarray
    """

    # Convert mask to boolean image, rather than 0 and 255 for skimage to use it
    skeleton = skmorph.skeletonize(mask.astype(bool))

    skeleton = skeleton.astype(np.uint8) * 255

    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(skeleton, os.path.join(params.debug_outdir, str(params.device) + '_skeleton.png'))
    elif params.debug == 'plot':
        plot_image(skeleton, cmap='gray')

    return skeleton
