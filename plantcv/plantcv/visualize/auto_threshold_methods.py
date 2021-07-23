# Compare auto threshold methods for a grayscale image

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv.transform import resize_factor
from plantcv.plantcv import fatal_error
from plantcv.plantcv._debug import _debug
from plantcv.plantcv.threshold import mean
from plantcv.plantcv.threshold import otsu
from plantcv.plantcv.threshold import gaussian
from plantcv.plantcv.threshold import triangle


def auto_threshold_methods(gray_img, grid_img=True, object_type="light"):
    """ Compare auto threshold methods for a grayscale image

    Inputs:
    gray_img     = Grayscale image data
    grid_img     = Whether or not to compile masks into a single plot
    object_type  = "light" or "dark" (default: "light")
                   - If object is lighter than the background then standard thresholding is done
                   - If object is darker than the background then inverse thresholding is done

    Returns:
    labeled_imgs = List of labeled plotting images

    :param gray_img: numpy.ndarray
    :param grid_img: bool
    :param object_type: str
    :return labeled_imgs: list

    """
    # Check that the image is grayscale
    if not len(np.shape(gray_img)) == 2:
        fatal_error("Input image is not grayscale!")

    # Store and disable debug mode
    debug = params.debug
    params.debug = None

    # Initialize threshold method names, mask list, final images
    method_names = ["Gaussian", "Mean", "Otsu", "Triangle"]
    all_methods = []
    labeled_imgs = []

    # Set starting location for labeling different masks
    y = int(np.shape(gray_img)[0] / 8)
    x = int(np.shape(gray_img)[1] / 8)

    # Create mask imgs from each thresholding method
    all_methods.append(gaussian(gray_img=gray_img, max_value=255, object_type=object_type))
    all_methods.append(mean(gray_img=gray_img, max_value=255, object_type=object_type))
    all_methods.append(otsu(gray_img=gray_img, max_value=255, object_type=object_type))
    all_methods.append(triangle(gray_img=gray_img, max_value=255, object_type=object_type, xstep=1))

    # Plot labels of each colorspace on the corresponding img
    for i, method in enumerate(all_methods):
        converted_img = cv2.cvtColor(method, cv2.COLOR_GRAY2RGB)
        labeled = cv2.putText(img=converted_img, text=method_names[i], org=(x, y),
                              fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                              fontScale=params.text_size, color=(255, 0, 255), thickness=params.text_thickness)
        # Reset debug mode
        params.debug = debug
        _debug(visual=labeled,
               filename=os.path.join(params.debug_outdir,
                                     str(params.device) + "_" + method_names[i] + "_vis_thresholds.png"))
        labeled_imgs.append(labeled)

    if grid_img:
        # Store and disable debug mode
        debug = params.debug
        params.debug = None
        # Compile images together into one
        top_row = np.hstack([labeled_imgs[0], labeled_imgs[1]])
        bot_row = np.hstack([labeled_imgs[2], labeled_imgs[3]])
        plotting_img = np.vstack([top_row, bot_row])
        labeled_imgs.append(plotting_img)
        plotting_img = resize_factor(plotting_img, factors=(0.5, 0.5))
        # Reset debug mode
        params.debug = debug
        _debug(visual=plotting_img,
               filename=os.path.join(params.debug_outdir, str(params.device) + "_vis_all_thresholds.png"))

    return labeled_imgs
