# Visualize an RGB image in all potential colorspaces as one glance

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv.transform import resize_factor
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import print_image
from plantcv.plantcv import rgb2gray_hsv
from plantcv.plantcv import rgb2gray_lab


def colorspaces(rgb_img, original_img=True):
    """ Visualize an RGB image in all potential colorspaces

    Inputs:
    rgb_img      = RGB image data
    original_img = Whether or not to include the original image the the debugging plot

    Returns:
    plotting_img = Plotting image containing the original image and L,A,B,H,S, and V colorspaces

    :param rgb_img: numpy.ndarray
    :param original_img: bool
    :return labeled_img: numpy.ndarray
    """

    if not len(np.shape(rgb_img)) == 3:
        fatal_error("Input image is not RGB!")

    # Store and disable debug mode
    debug = params.debug
    params.debug = None

    # Initialize grayscale images list, rgb images list, plotting coordinates
    colorspace_names = ["H", "S", "V", "L", "A", "B"]
    all_colorspaces = []
    labeled_imgs = []
    y = int(np.shape(rgb_img)[0] / 2)
    x = int(np.shape(rgb_img)[1] / 2)

    # Loop through and create grayscale imgs from each colorspace
    for i in range(0, 3):
        channel = colorspace_names[i]
        all_colorspaces.append(rgb2gray_hsv(rgb_img=rgb_img, channel=channel))
    for i in range(3, 6):
        channel = colorspace_names[i]
        all_colorspaces.append(rgb2gray_lab(rgb_img=rgb_img, channel=channel))

    # Plot labels of each colorspace on the corresponding img
    for i, colorspace in enumerate(all_colorspaces):
        converted_img = cv2.cvtColor(colorspace, cv2.COLOR_GRAY2RGB)
        labeled = cv2.putText(img=converted_img, text=colorspace_names[i], org=(x, y),
                              fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                              fontScale=params.text_size, color=(255, 0, 255), thickness=params.text_thickness)
        labeled_imgs.append(labeled)

    # Compile images together, including a larger version of the original image
    plotting_img = np.vstack([np.hstack([labeled_imgs[0], labeled_imgs[1], labeled_imgs[2]]),
                              np.hstack([labeled_imgs[3], labeled_imgs[4], labeled_imgs[5]])])

    # If original_img is True then also plot the original image with the rest of them
    if original_img:
        plotting_img = np.hstack([resize_factor(img=rgb_img, factors=(2, 2)), plotting_img])
    plotting_img = resize_factor(plotting_img, factors=(0.5, 0.5))

    # Reset debug mode
    params.debug = debug

    if params.debug == "print":
        # If debug is print, save the image to a file
        print_image(plotting_img, os.path.join(params.debug_outdir, str(params.device) + "_vis_colorspaces.png"))
    elif params.debug == "plot":
        # If debug is plot, print to the plotting device
        plot_image(plotting_img)

    return plotting_img
