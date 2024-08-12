# Tile output images in a plot to visualize all at once

import cv2
import numpy as np
from plantcv.plantcv._debug import _debug

def _row_resize(row, ncol):
    """ Resizes and concatenates objects in a row """
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
    """ Resized and concatenates objects in a column """
    w_min = min(img.shape[1] for img in col)
    col_resize = [cv2.resize(img, (w_min, int(img.shape[0] * w_min / img.shape[1])), 
                             interpolation=cv2.INTER_CUBIC) for img in col]
    return cv2.vconcat(col_resize)

# The function that does the tiling
def tile(images, nrow, ncol):
    """Tile a list of images into a composite with given dimensions.

    Inputs:
    images      = A list of images
    nrow        = Number of rows in desired composite
    ncol        = Number of columns in desired composite

    Returns:
    comp_img    = A composite image of tiled inputs from list

    :param images: list of numpy.ndarray objects
    :param nrow: int
    :return ncol: int
    """
    tracker = 0
    mat = []
    for i in range(nrow):
        row = []
        for _ in range(ncol):
            if tracker <= (len(images) - 1):
                row.append(images[tracker])
            tracker += 1
        mat.append(_row_resize(row, ncol))
    comp_img = _col_resize(mat)
    _debug(visual=comp_img, filename=os.path.join(params.debug_outdir, f"{params.device}_tile.png"))
    return comp_img
