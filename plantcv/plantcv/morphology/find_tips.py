"""Find tips from skeleton image."""
import os
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _find_tips


def find_tips(skel_img, mask=None, label=None):
    """Find tips in skeletonized image.
    The endpoints algorithm was inspired by Jean-Patrick Pommier: https://gist.github.com/jeanpat/5712699

    Inputs:
    skel_img    = Skeletonized image
    mask        = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.
    label       = Optional label parameter, modifies the variable name of
                  observations recorded (default = pcv.params.sample_label).
    Returns:
    tip_img   = Image with just tips, rest 0

    :param skel_img: numpy.ndarray
    :param mask: numpy.ndarray
    :param label: str
    :return tip_img: numpy.ndarray
    """
    tip_img, tip_list, tip_labels = _find_tips(skel_img=skel_img, mask=mask)

    _debug(visual=tip_img, filename=os.path.join(params.debug_outdir, f"{params.device}_skeleton_tips.png"))

    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label
    # Save coordinates to Outputs
    outputs.add_observation(sample=label, variable='tips', trait='list of tip coordinates identified from a skeleton',
                            method='plantcv.plantcv.morphology.find_tips', scale='pixels', datatype=list,
                            value=tip_list, label=tip_labels)

    return tip_img
