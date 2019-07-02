import numpy as np
from plantcv.plantcv import fatal_error
from plantcv.plantcv import outputs


def within_frame(mask):
    """
    This function tests whether the plant touches the edge of the image, i.e. it is completely in the field of view.
    Input:
    mask = a binary image of 0 and nonzero values

    Returns:
    in_bounds = a boolean (True or False) confirming that the object does not touch the edge of the image

    :param mask: numpy.ndarray
    :return in_bounds: bool

    """

    # Check if object is touching image boundaries (QC)
    if len(np.shape(mask)) > 2 or len(np.unique(mask)) > 2:
        fatal_error("Mask should be a binary image of 0 and nonzero values.")

    # First column
    first_col = mask[:, 0]

    # Last column
    last_col = mask[:, -1]

    # First row
    first_row = mask[0, :]

    # Last row
    last_row = mask[-1, :]

    edges = np.concatenate([first_col, last_col, first_row, last_row])

    out_of_bounds = bool(np.count_nonzero(edges))
    in_bounds = not out_of_bounds

    outputs.add_observation(variable='in_bounds', trait='whether the plant goes out of bounds ',
                            method='plantcv.plantcv.within_frame', scale='none', datatype=bool,
                            value=in_bounds, label='none')

    return in_bounds
