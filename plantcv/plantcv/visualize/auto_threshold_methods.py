# Visualize an RGB image in all potential colorspaces as one glance

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import resize
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv.threshold import gaussian
from plantcv.plantcv.threshold import mean
from plantcv.plantcv.threshold import otsu
from plantcv.plantcv.threshold import triangle


def thresholds(gray_img, original_img=True, object_type="light"):
    """ Visualize an RGB image in all potential colorspaces

    Inputs:
    gray_img     = grayscale image data
    original_img = Whether or not to include the original image the the debugging plot

    Returns:
    plotting_img = Plotting image containing the original image and L,A,B,H,S, and V colorspaces

    :param gray_img: numpy.ndarray
    :param original_img: bool
    :return labeled_img: numpy.ndarray

    """

    if not len(np.shape(gray_img)) == 2:
        fatal_error("Input image is not grayscale!")

    # Store and disable debug mode
    debug = params.debug
    params.debug = None

    # Initialize grayscale images list, rgb images list, plotting coordinates
    method_names = ["Gaussian", "Mean", "Otsu", "Triangle"]
    all_methods = []
    labeled_imgs = []
    y = int(np.shape(gray_img)[0] )
    x = int(np.shape(gray_img)[1] )

    # Create mask imgs from each thresholding method
    all_methods.append(gaussian(gray_img=gray_img, max_value=255, object_type=object_type))
    all_methods.append(mean(gray_img=gray_img, max_value=255, object_type=object_type))
    all_methods.append(otsu(gray_img=gray_img, max_value=255, object_type=object_type))
    all_methods.append(triangle(gray_img=gray_img, max_value=255, object_type=object_type, xstep=10))

    # Plot labels of each colorspace on the corresponding img
    for i, method in enumerate(all_methods):
        converted_img = cv2.cvtColor(method, cv2.COLOR_GRAY2RGB)
        labeled = cv2.putText(img=converted_img, text=method_names[i], org=(x, y),
                              fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                              fontScale=params.text_size, color=(255, 0, 255), thickness=params.text_thickness)
        labeled_imgs.append(labeled)

    # Compile images together, including a larger version of the original image
    plotting_img = np.hstack([labeled_imgs[0], labeled_imgs[1],labeled_imgs[2], labeled_imgs[3]])

    # If original_img is True then also plot the original image with the rest of them
    if original_img:
        converted_gray_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2RGB)
        plotting_img = np.hstack([converted_gray_img, plotting_img])
    plotting_img = resize(plotting_img,  resize_x=.5, resize_y=.5)

    # Reset debug mode
    params.debug = debug

    if params.debug == "print":
        # If debug is print, save the image to a file
        print_image(plotting_img, os.path.join(params.debug_outdir, str(params.device) + "_vis_colorspaces.png"))
    elif params.debug == "plot":
        # If debug is plot, print to the plotting device
        plot_image(plotting_img)

    return plotting_img
