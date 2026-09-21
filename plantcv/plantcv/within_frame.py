"""Check if mask in within the frame."""

import numpy as np
from plantcv.plantcv import fatal_error
from plantcv.plantcv import outputs, params


def within_frame(mask, border_width=1, label=None):
    """Determine whether the plant is completely within the image frame.

    Parameters
    ----------
    mask : numpy.ndarray
        Binary image containing zero and nonzero values.
    border_width : int, optional
        Distance from the image border considered out of frame. The default
        is 1.
    label : str, optional
        Label used for recorded observations. Defaults to
        ``pcv.params.sample_label``.

    Returns
    -------
    bool
        ``True`` if the plant does not touch the image border, otherwise
        ``False``.
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    # Check if object is touching image boundaries (QC)
    if len(np.shape(mask)) > 2 or _over_two_values(mask):
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


def _over_two_values(mask):
    """Test whether a mask holds more than two distinct values.

    Parameters
    ----------
    mask : numpy.ndarray
        Mask to test.

    Returns
    -------
    bool
        True if the mask contains three or more distinct values.
    """
    values = np.asarray(mask)
    # An empty mask has no values to disagree, matching len(np.unique([])) == 0
    if values.size == 0:
        return False
    low = values.min()
    high = values.max()
    if low == high:
        return False
    return bool(np.any((values != low) & (values != high)))
