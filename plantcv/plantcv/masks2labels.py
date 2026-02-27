# Create single labeled img from a list of masks
import os
import numpy as np
from skimage.color import label2rgb
from plantcv.plantcv._globals import params
from plantcv.plantcv._debug import _debug


def masks2labels(mask_list):
    """Create a labeled mask where connected regions of non-zero
    pixels are assigned a label value based on the provided
    region of interest (ROI).

    Parameters
    ----------
    mask : list of numpy.ndarray
        List of masks
        
    Returns
    ----------
    mask : numpy.ndarray
        Labeled mask
    colored_img : numpy.ndarray
        Labeled color image for visualization
    num_labels : int
        Number of labeled objects
    """
    # Store debug mode
    debug = params.debug
    params.debug = None

    labeled_mask = np.zeros(mask_list[0].shape[:2], dtype=np.int32)
    label1 = [0]
    mask1 = []
    for _, mask in enumerate(mask_list, start=1):
        if np.sum(mask) > 0:
            value = label1[-1]+1
            labeled_mask[mask > 0] = value
            mask1.append(mask)
            label1.append(value)
    num_label = len(label1)-1

    # Restore debug parameter

    params.debug = debug
    colorful = label2rgb(labeled_mask)
    colorful2 = (255*colorful).astype(np.uint8)

    _debug(colorful2, filename=os.path.join(params.debug_outdir,
                                            str(params.device) +
                                            '_label_colored_img.png'))

    return labeled_mask, colorful2, num_label
