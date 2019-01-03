# Background Subtraction:
# Subtracts a background image from a foreground image once.

import os
import cv2
import numpy as np
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def background_subtraction(background_image, foreground_image):
    """Creates a binary image from a background subtraction of the foreground using cv2.BackgroundSubtractorMOG().
    The binary image returned is a mask that should contain mostly foreground pixels.
    The background image should be the same background as the foreground image except not containing the object
    of interest.

    Images must be of the same size and type.
    If not, larger image will be taken and downsampled to smaller image size.
    If they are of different types, an error will occur.

    Inputs:
    background_image       = img object, RGB or binary/grayscale/single-channel
    foreground_image       = img object, RGB or binary/grayscale/single-channel

    Returns:
    fgmask                 = background subtracted foreground image (mask)

    :param background_image: numpy.ndarray
    :param foreground_image: numpy.ndarray
    :return fgmask: numpy.ndarray
    """

    params.device += 1
    # Copying images to make sure not alter originals
    bg_img = np.copy(background_image)
    fg_img = np.copy(foreground_image)
    # Checking if images need to be resized or error raised
    if bg_img.shape != fg_img.shape:
        # If both images are not 3 channel or single channel then raise error.
        if len(bg_img.shape) != len(fg_img.shape):
            fatal_error("Images must both be single-channel/grayscale/binary or RGB")
        # Forcibly resizing largest image to smallest image
        print("WARNING: Images are not of same size.\nResizing")
        if bg_img.shape > fg_img.shape:
            width, height = fg_img.shape[1], fg_img.shape[0]
            bg_img = cv2.resize(bg_img, (width, height), interpolation=cv2.INTER_AREA)
        else:
            width, height = bg_img.shape[1], bg_img.shape[0]
            fg_img = cv2.resize(fg_img, (width, height), interpolation=cv2.INTER_AREA)

    # # Will be depricating opencv version 2
    # Instantiating the background subtractor, for a single history no default parameters need to be changed.
    # if cv2.__version__[0] == '2':
    #     bgsub = cv2.BackgroundSubtractorMOG()
    # else:
    bgsub = cv2.createBackgroundSubtractorMOG2()
    # Applying the background image to the background subtractor first.
    # Anything added after is subtracted from the previous iterations.
    fgmask = bgsub.apply(bg_img)
    # Applying the foreground image to the background subtractor (therefore removing the background)
    fgmask = bgsub.apply(fg_img)

    # Debug options
    if params.debug == "print":
        print_image(fgmask, os.path.join(params.debug_outdir, str(params.device) + "_background_subtraction.png"))
    elif params.debug == "plot":
        plot_image(fgmask, cmap="gray")
    
    return fgmask
