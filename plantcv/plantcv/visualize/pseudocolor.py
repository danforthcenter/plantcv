# Pseudocolor any grayscale image

import os
import numpy as np
from matplotlib import pyplot as plt
from plantcv.plantcv import params
from plantcv.plantcv import fatal_error
from plantcv.plantcv.apply_mask import apply_mask


def pseudocolor(gray_img, mask=None, cmap=None, background="image", min_value=0, max_value=255,
                axes=True, colorbar=True, title=None, bad_mask=None, bad_color="red"):
    """Pseudocolor any grayscale image to custom colormap

    Inputs:
    gray_img    = grayscale image data
    mask        = (optional) binary or labeled mask
    cmap        = (optional) colormap. default is the matplotlib default, viridis
    background  = (optional) background color/type, options are "image" (gray_img), "white", or "black"
                  (requires a mask). default = 'image'
    min_value   = (optional) minimum value for range of interest. default = 0
    max_value   = (optional) maximum value for range of interest. default = 255
    axes        = (optional) if False then x- and y-axis won't be displayed, nor will the title. default = True
    colorbar    = (optional) if False then colorbar won't be displayed. default = True
    title       = (optional) custom title for the plot gets drawn if title is not None. default = None
    bad_mask    = (optional) binary mask of pixels with "bad" values, e.g. nan or inf or any other values considered
                  to be not informative and to be excluded from analysis. default = None
    bad_color   = (optional) desired color to show "bad" pixels. default = "red"
    Returns:
    pseudo_image = pseudocolored image

    :param gray_img: numpy.ndarray
    :param mask: numpy.ndarray
    :param cmap: str
    :param background: str
    :param min_value: numeric
    :param max_value: numeric
    :param axes: bool
    :param colorbar: bool
    :param title: str
    :param bad_mask: numpy.ndarray
    :param bad_color: str
    :return pseudo_image: matplotlib.figure.Figure
    """
    # Auto-increment the device counter
    params.device += 1

    # Make copies of the gray image
    gray_img1 = np.copy(gray_img)

    # Check if the image is grayscale
    if len(np.shape(gray_img)) != 2:
        fatal_error("Image must be grayscale.")

    # Check if background is a supported type
    if background.upper() not in ["IMAGE", "WHITE", "BLACK"]:
        fatal_error(f"Background type {background} is not supported. Please use 'white', 'black', or 'image'.")

    bad_idx, bad_idy = [], []

    # Create a whole-image mask if mask is None
    if mask is None:
        mask = np.ones(np.shape(gray_img), dtype=np.uint8)

    # Convert the input mask to binary
    mask = mask.copy()
    # Set all values greater than 0 to 255
    mask[np.where(mask > 0)] = 255
    # Change type to unsigned 8-bit integer
    mask = mask.astype(np.uint8)

    # Apply the mask
    masked_img = np.ma.array(gray_img1, mask=~mask.astype(bool))

    # Set the background color or type
    bkgd = {
        "BLACK": {
            "image": np.zeros(np.shape(gray_img1), dtype=np.uint8),
            "cmap": "gray"
            },
        "WHITE": {
            "image": np.zeros(np.shape(gray_img1), dtype=np.uint8) + 255,
            "cmap": "gray_r"
            },
        "IMAGE": {
            "image": gray_img1,
            "cmap": "gray"
            }
    }
    bkg_img = bkgd[background.upper()]["image"]
    bkg_cmap = bkgd[background.upper()]["cmap"]

    if bad_mask is not None:
        debug_mode = params.debug
        params.debug = None
        bad_mask = apply_mask(bad_mask, mask, mask_color='black')
        bad_idx, bad_idy = np.where(bad_mask > 0)
        params.debug = debug_mode

    plt.figure()
    # Pseudocolor the image, plot the background first
    plt.imshow(bkg_img, cmap=bkg_cmap)
    # Overlay the masked grayscale image with the user input colormap
    plt.imshow(masked_img, cmap=cmap, vmin=min_value, vmax=max_value)
    plt.plot(bad_idy, bad_idx, '.', color=bad_color)

    if colorbar:
        plt.colorbar(fraction=0.033, pad=0.04)

    if axes and title is not None:
        # Include image title
        plt.title(title)
    else:
        # Remove axes
        plt.xticks([])
        plt.yticks([])

    # Store the current figure
    pseudo_img = plt.gcf()

    # Print or plot if debug is turned on
    if params.debug is not None:
        if params.debug == 'print':
            plt.savefig(os.path.join(params.debug_outdir, str(
                params.device) + '_pseudocolored.png'), dpi=params.dpi)
            plt.close()
        elif params.debug == 'plot':
            # Use non-blocking mode in case the function is run more than once
            plt.show(block=False)
    else:
        plt.close()

    return pseudo_img
