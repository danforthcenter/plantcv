# Binary image -> Skeleton

import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
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

    _debug(visual=skeleton, filename=os.path.join(params.debug_outdir, f"{params.device}_skeleton.png"))

    return skeleton
