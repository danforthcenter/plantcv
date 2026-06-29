# Helper function to take an ROI and turn it into a binary mask

import os
import cv2
import numpy as np
from skimage.color import label2rgb
from plantcv.plantcv._globals import params
from plantcv.plantcv._debug import _debug


def roi2mask(img, roi):
    """
    Create a binary mask from an ROI contour

    Parameters:
    -----------
    img = numpy.ndarray,
        RGB or grayscale image data
    roi = plantcv.plantcv.classes.Objects,
        A region of interest as an instance of the class Objects

    Returns:
    --------
    mask   = numpy.ndarray,
        Labeled mask or binary mask if only one ROI is given
    """
    # create a blank image of same size
    labeled_mask = np.zeros(img.shape[:2], dtype=np.int32)
    # get number of labels
    num_labels = len(roi.contours)
    for i, obj in enumerate(roi):
        # Pixel intensity of (i+1) such that the first object has value 1
        cv2.drawContours(labeled_mask, obj.contours[0], -1, (i+1), -1)

    colorful = label2rgb(labeled_mask)
    colorful2 = (255*colorful).astype(np.uint8)

    if num_labels == 1:
        labeled_mask = (labeled_mask*255).astype(np.uint8)

    _debug(visual=colorful2,
           filename=os.path.join(params.debug_outdir,
                                 f"{params.device}_roi2mask.png"))

    return labeled_mask
