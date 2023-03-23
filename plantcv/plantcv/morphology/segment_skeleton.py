# Break skeleton into segments

import os
import cv2
from plantcv.plantcv import dilate
from plantcv.plantcv import params
from plantcv.plantcv import color_palette
from plantcv.plantcv import image_subtract
from plantcv.plantcv.morphology import find_branch_pts
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _cv2_findcontours


def segment_skeleton(skel_img, mask=None):
    """Segment a skeleton image into pieces.

    Inputs:
    skel_img         = Skeletonized image
    mask             = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.

    Returns:
    segmented_img       = Segmented debugging image
    segment_objects     = list of contours

    :param skel_img: numpy.ndarray
    :param mask: numpy.ndarray
    :return segmented_img: numpy.ndarray
    :return segment_objects: list
    """
    # Store debug
    debug = params.debug
    params.debug = None

    # Find branch points
    bp = find_branch_pts(skel_img)
    bp = dilate(bp, 3, 1)

    # Subtract from the skeleton so that leaves are no longer connected
    segments = image_subtract(skel_img, bp)

    # Gather contours of leaves
    segment_objects, _ = _cv2_findcontours(bin_img=segments)

    # Reset debug mode
    params.debug = debug

    # Color each segment a different color, do not used a previously saved color scale
    rand_color = color_palette(num=len(segment_objects), saved=False)

    if mask is None:
        segmented_img = skel_img.copy()
    else:
        segmented_img = mask.copy()

    segmented_img = cv2.cvtColor(segmented_img, cv2.COLOR_GRAY2RGB)
    for i, cnt in enumerate(segment_objects):
        cv2.drawContours(segmented_img, segment_objects, i, rand_color[i], params.line_thickness, lineType=8)

    _debug(visual=segmented_img, filename=os.path.join(params.debug_outdir, f"{params.device}_segmented.png"))

    return segmented_img, segment_objects
