# Break skeleton into segments

import os
import cv2
from plantcv.plantcv._globals import params
from plantcv.plantcv.color_palette import color_palette
from plantcv.plantcv.morphology.find_branch_pts import _find_branch_pts
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _cv2_findcontours, _dilate, _image_subtract


def segment_skeleton(skel_img, mask=None):
    """Segment a skeleton image into pieces.

    Parameters
    ----------
    skel_img = numpy.ndarray,
        Skeletonized image
    mask     = numpy.ndarray,
        binary mask for debugging. If provided, debug image will be overlaid on the mask.

    Returns
    -------
    segmented_img    = numpy.ndarray,
        Segmented debugging image
    segment_objects  = list,
        list of contours
    """
    segment_objects = _segment_skeleton(skel_img)

    # Color each segment a different color, do not used a previously saved color scale
    rand_color = color_palette(num=len(segment_objects), saved=False)

    if mask is None:
        segmented_img = skel_img.copy()
    else:
        segmented_img = mask.copy()

    segmented_img = cv2.cvtColor(segmented_img, cv2.COLOR_GRAY2RGB)
    for i, _ in enumerate(segment_objects):
        cv2.drawContours(segmented_img, segment_objects, i, rand_color[i], params.line_thickness, lineType=8)

    _debug(visual=segmented_img, filename=os.path.join(params.debug_outdir, f"{params.device}_segmented.png"))

    return segmented_img, list(segment_objects)


def _segment_skeleton(skel_img):
    """Segment a skeleton image into pieces.

    Parameters
    ----------
    skel_img = numpy.ndarray,
        Skeletonized image

    Returns
    -------
    segmented_img    = numpy.ndarray,
        Segmented debugging image
    segment_objects  = list,
        list of contours
    """
    # Find branch points
    _, _, bp = _find_branch_pts(skel_img)
    bp = _dilate(bp, 3, 1)
    # Subtract from the skeleton so that leaves are no longer connected
    segments = _image_subtract(skel_img, bp)
    # Gather contours of leaves
    segment_objects, _ = _cv2_findcontours(bin_img=segments)

    return segment_objects
