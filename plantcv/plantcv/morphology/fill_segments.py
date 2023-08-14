"""Fill a mask using watershed and skeleton segments."""
import os
import cv2
import numpy as np
from skimage.segmentation import watershed
from plantcv.plantcv import outputs
from plantcv.plantcv import params
from plantcv.plantcv.visualize import colorize_label_img
from plantcv.plantcv._debug import _debug


def fill_segments(mask, objects, stem_objects=None, label=None):
    """Fills masked segments from contours.

    Inputs:
    mask         = Binary image, single channel, object = 1 and background = 0
    objects      = List of contours
    stem_objects = Array of stem contours
    label        = Optional label parameter, modifies the variable name of
                   observations recorded (default = pcv.params.sample_label).

    Returns:
    filled_mask   = Labeled mask

    :param mask: numpy.ndarray
    :param objects: list
    :param stem_objects: numpy.ndarray
    :param label: str
    :return filled_mask: numpy.ndarray
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    h, w = mask.shape
    markers = np.zeros((h, w), dtype=np.int32)

    objects_unique = objects.copy()
    if stem_objects is not None:
        objects_unique.append(np.vstack(stem_objects))

    labels = np.arange(len(objects_unique)) + 1
    for i, l in enumerate(labels):
        cv2.drawContours(markers, objects_unique, i, int(l), 5)

    # Fill as a watershed segmentation from contours as markers
    filled_mask = watershed(mask == 0, markers=markers,
                            mask=mask != 0, compactness=0)

    # Count area in pixels of each segment
    ids, counts = np.unique(filled_mask, return_counts=True)

    if stem_objects is None:
        outputs.add_observation(sample=label, variable='segment_area', trait='segment area',
                                method='plantcv.plantcv.morphology.fill_segments',
                                scale='pixels', datatype=list,
                                value=counts[1:].tolist(),
                                label=(ids[1:]-1).tolist())
    else:
        outputs.add_observation(sample=label, variable='leaf_area', trait='segment area',
                                method='plantcv.plantcv.morphology.fill_segments',
                                scale='pixels', datatype=list,
                                value=counts[1:-1].tolist(),
                                label=(ids[1:-1]-1).tolist())
        outputs.add_observation(sample=label, variable='stem_area', trait='segment area',
                                method='plantcv.plantcv.morphology.fill_segments',
                                scale='pixels', datatype=list,
                                value=counts[-1].tolist(),
                                label=(ids[-1]-1).tolist())

    debug = params.debug
    params.debug = None
    filled_img = colorize_label_img(filled_mask)
    params.debug = debug
    _debug(visual=filled_img, filename=os.path.join(params.debug_outdir,
                                                    str(params.device) + "_filled_segments_img.png"))

    return filled_mask
