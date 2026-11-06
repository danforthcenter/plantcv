"""Fill a mask using watershed and skeleton segments."""
import cv2
import numpy as np
from skimage.segmentation import watershed
from plantcv.plantcv._globals import params, outputs
from plantcv.plantcv._helpers import _scale_size, _area_unit


def _fill_segments(morph, stems=False, label=None):
    """Fills masked segments from contours.

    Parameters
    ----------
    morph = plantcv.plantcv.morphology.morph object,
        Morphology object to analyze
    stems = boolean,
        Should stems be separated? Defaults to False.
    label        = str,
        Optional label parameter, modifies the variable name of
        observations recorded (default = pcv.params.sample_label).

    Returns
    -------
    filled_mask = numpy.ndarray, Labeled mask
    """
    mask = morph.mask
    objects = morph.leaves
    stem_objects = None
    if stems:
        stem_objects = morph.stem

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
                                method='plantcv.plantcv.analyze.morphology',
                                scale=_area_unit(), datatype=list,
                                value=_scale_size(value=counts[1:].tolist(), trait_type="area"),
                                label=(ids[1:]-1).tolist())
    else:
        outputs.add_observation(sample=label, variable='leaf_area', trait='segment area',
                                method='plantcv.plantcv.analyze.morphology',
                                scale=_area_unit(), datatype=list,
                                value=_scale_size(value=counts[1:-1].tolist(), trait_type="area"),
                                label=(ids[1:-1]-1).tolist())
        outputs.add_observation(sample=label, variable='stem_area', trait='segment area',
                                method='plantcv.plantcv.analyze.morphology',
                                scale=_area_unit(), datatype=list,
                                value=_scale_size(value=counts[-1].tolist(), trait_type="area"),
                                label=(ids[-1]-1).tolist())

    return filled_mask
