# Find both segment end coordinates
import os
import numpy as np
from plantcv.plantcv import params, outputs
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _find_segment_ends


def segment_ends(skel_img, leaf_objects, mask=None, label=None):
    """Find tips and segment branch points.

    Inputs:
    skel_img         = Skeletonized image
    leaf_objects     = List of leaf segments
    mask             = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.
    label            = Optional label parameter, modifies the variable name of
                       observations recorded (default = pcv.params.sample_label).

    Returns:
    sorted_obs       = Reordered segments based on segment branch point y-coordinates

    :param segmented_img: numpy.ndarray
    :param leaf_objects: list
    :param mask: numpy.ndarray
    :param label: str
    :return sorted_ids: list
    """
    # Store debug
    debug = params.debug
    params.debug = None

    if mask is None:
        labeled_img = skel_img.copy()
    else:
        labeled_img = mask.copy()
    # Find and sort segment ends, and create debug image
    labeled_img, tip_list, inner_list, labels = _find_segment_ends(
        skel_img=skel_img, leaf_objects=leaf_objects, plotting_img=labeled_img, size=1)
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label
    # Save coordinates to Outputs
    outputs.add_observation(sample=label, variable='segment_tips',
                            trait='list of tip coordinates identified from segments',
                            method='plantcv.plantcv.morphology.segment_ends', scale='None', datatype=list,
                            value=tip_list, label=labels)
    outputs.add_observation(sample=label, variable='segment_branch_points',
                            trait='list of branch point coordinates identified from segments',
                            method='plantcv.plantcv.morphology.segment_ends', scale='None', datatype=list,
                            value=inner_list, label=labels)
    # Reset debug mode
    params.debug = debug
    _debug(visual=labeled_img, filename=os.path.join(params.debug_outdir, f"{params.device}_segment_ends.png"))

    # Determine optimal segment order by y-coordinate order
    d = {}
    for i, coord in enumerate(inner_list):
        d[i] = coord[1]  # y-coord is the key and index the value
    values = list(d.values())
    sorted_key_index = np.argsort(values)
    sorted_objs = [leaf_objects[i] for i in sorted_key_index[::-1]]

    return sorted_objs
