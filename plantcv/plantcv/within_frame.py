# Check if mask in within the frame

import numpy as np
from plantcv.plantcv import fatal_error
from plantcv.plantcv import outputs


def within_frame(mask, border_width=1, label="default"):
    """
    This function tests whether the plant touches the edge of the image, i.e. it is completely in the field of view.
    Input:
    mask         = a binary image of 0 and nonzero values
    border_width = distance from border of image considered out of frame (default = 1)
    label        = optional label parameter, modifies the variable name of observations recorded

    Returns:
    in_bounds = a boolean (True or False) confirming that the object does not touch the edge of the image

    :param mask: numpy.ndarray
    :param border_width: int
    :param label: str
    :return in_bounds: bool
    """

    # Check if object is touching image boundaries (QC)
    if len(np.shape(mask)) > 2 or len(np.unique(mask)) > 2:
        fatal_error("Mask should be a binary image of 0 and nonzero values.")

    # First column
    first_col = mask[:, range(0, border_width)]

    # Last column
    last_col = mask[:, range(-border_width, 0)]

    # First row
    first_row = mask[range(0, border_width), :]

    # Last row
    last_row = mask[range(-border_width, 0), :]

    border_pxs = np.concatenate([first_col.flatten(), last_col.flatten(), first_row.flatten(), last_row.flatten()])

    out_of_bounds = bool(np.count_nonzero(border_pxs))
    in_bounds = not out_of_bounds

    outputs.add_observation(sample=label, variable='in_bounds', trait='whether the plant goes out of bounds ',
                            method='plantcv.plantcv.within_frame', scale='none', datatype=bool,
                            value=in_bounds, label='none')

    return in_bounds
