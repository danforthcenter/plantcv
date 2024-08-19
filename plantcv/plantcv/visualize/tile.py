# Tile output images in a plot to visualize all at once

import cv2
import numpy as np
import os
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def _row_resize(row, ncol):
    """Resizes and concatenates objects in a row.

    Parameters
    ----------
    row : list of numpy.ndarray
        List of images to concatenate.
    ncol : int
        Number of columns in desired composite image.

    Returns
    -------
    numpy.ndarray
        Image concatenated horizontally.
    """
    h_min = min(img.shape[0] for img in row)
    # Resizing each image so they're the same
    row_resize = [cv2.resize(img, (int(img.shape[1] * h_min / img.shape[0]), h_min),
                             interpolation=cv2.INTER_CUBIC) for img in row]
    # Add empty images to the end of the row so things still stay the same size
    while len(row_resize) < ncol:
        row_resize.append(np.zeros(row_resize[0].shape, dtype=np.uint8))
    # Concatenate horizontally
    return cv2.hconcat(row_resize)


# Same as _row_resize but for columns
def _col_resize(col):
    """Resized and concatenates objects in a column.

    Parameters
    ----------
    col : list of numpy.ndarray
        List of images to concatenate vertically.

    Returns
    -------
    numpy.ndarray
        Image concatenated vertically.
    """
    w_min = min(img.shape[1] for img in col)
    col_resize = [cv2.resize(img, (w_min, int(img.shape[0] * w_min / img.shape[1])),
                             interpolation=cv2.INTER_CUBIC) for img in col]
    return cv2.vconcat(col_resize)


# The function that does the tiling
def tile(images, ncol):
    """Tile a list of images into a composite with given dimensions.

    Parameters
    ----------
    images : list of numpy.ndarray
        List of images to tile.
    ncol : int
        Number of columns in desired composite image.

    Returns
    -------
    numpy.ndarray
        Tiled composite image.
    """
    # Increment the device counter
    params.device += 1

    # Calculate number of rows - always rounds up
    nrow = int(len(images) / ncol) + (len(images) % ncol > 0)
    tracker = 0
    mat = []
    for _ in range(nrow):
        row = []
        for _ in range(ncol):
            if tracker <= (len(images) - 1):
                row.append(images[tracker])
            tracker += 1
        mat.append(_row_resize(row, ncol))
    comp_img = _col_resize(mat)
    _debug(visual=comp_img, filename=os.path.join(params.debug_outdir, f"{params.device}_tile.png"))
    return comp_img
