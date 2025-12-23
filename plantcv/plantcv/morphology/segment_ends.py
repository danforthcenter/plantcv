# Find both segment end coordinates
import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _find_segment_ends


def segment_ends(skel_img, leaf_objects, mask=None):
    """Find tips and segment branch points, resort objects based on inner_list of coordinates.

    Inputs:
    skel_img         = Skeletonized image
    leaf_objects     = List of leaf segments
    mask             = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.

    Returns:
    sorted_obs       = Reordered segments based on segment branch point y-coordinates
    inner_list       = List of branch point coordinates of the input leaf_objects
    tip_list         = List of leaf tip coordinates of the input leaf_object

    :param segmented_img: numpy.ndarray
    :param leaf_objects: list
    :param mask: numpy.ndarray
    :return sorted_ids: list
    :return inner_list: list
    :return tip_list: list
    """
    # Store debug
    debug = params.debug
    params.debug = None

    if mask is None:
        labeled_img = skel_img.copy()
    else:
        labeled_img = mask.copy()
    # Find and sort segment ends, and create debug image
    labeled_img, tip_list, inner_list, _, objs = _find_segment_ends(
        skel_img=skel_img, leaf_objects=leaf_objects, plotting_img=labeled_img, size=1)

    # Reset debug mode
    params.debug = debug
    _debug(visual=labeled_img, filename=os.path.join(params.debug_outdir, f"{params.device}_segment_ends.png"))

    # Determine optimal segment order by y-coordinate order
    d = {}
    for i, coord in enumerate(inner_list):
        d[i] = coord[1]  # y-coord is the key and index the value
    values = list(d.values())
    sorted_key_index = np.argsort(values)
    sorted_objs = [objs[i] for i in sorted_key_index[::-1]]

    return sorted_objs, inner_list, tip_list
