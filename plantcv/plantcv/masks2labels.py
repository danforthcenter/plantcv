# Create labels base on clean mask and optionally, multiple ROIs
#import cv2
import os
import numpy as np
from skimage.color import label2rgb
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def masks2labels(mask_list):
    """Create a labeled mask where connected regions of non-zero
    pixels are assigned a label value based on the provided
    region of interest (ROI).

    Inputs:
    mask            = list of masks
    
    Returns:
    mask            = Labeled mask
    colored_img     = Labeled color image for visualization
    num_labels      = Number of labeled objects

    :param mask: List of numpy.ndarray
    :return labeled_mask: numpy.ndarray
    :return colored_img: numpy.ndarray
    :return num_labels: int
    """
    # Store debug mode
    debug = params.debug
    params.debug = None

    labeled_mask = np.zeros(mask_list[0].shape[:2], dtype=np.int32)
    label1 = []
    mask1 = []
    for label, mask in enumerate(mask_list, start=1):
        labeled_mask[mask > 0] = label
        mask1.append(mask)
        label1.append(label)
    num_label = len(label1)

    # Restore debug parameter
    params.debug = debug
    colorful = label2rgb(labeled_mask)
    colorful2 = (255*colorful).astype(np.uint8)

    _debug(colorful2, filename=os.path.join(params.debug_outdir,
                                            str(params.device) +
                                            '_label_colored_img.png'))

    return labeled_mask, colorful2, num_label