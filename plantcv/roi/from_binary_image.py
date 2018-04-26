# Create an ROI from a binary mask


import cv2
import numpy as np
from plantcv import print_image
from plantcv import plot_image
from plantcv import fatal_error
from plantcv import params


def from_binary_image(bin_img, rgb_img=None):
    # Autoincrement the device counter
    params.device += 1
    # Make sure the image is binary
    if len(np.unique(bin_img)) != 2:
        fatal_error("Input image is not binary!")
    # Use the binary image to create an ROI contour
    roi_contour, roi_hierarchy = cv2.findContours(np.copy(bin_img), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    # Draw the ROI if requested
    if params.debug is not None and rgb_img is not None:
        if len(np.shape(rgb_img)) != 3:
            fatal_error("RGB image is not a color image!")
        ref_img = np.copy(rgb_img)
        cv2.drawContours(ref_img, roi_contour, -1, (255, 0, 0), 5)
        if params.debug == "print":
            # If debug is print, save the image to a file
            print_image(ref_img, (str(params.device) + "_roi.png"))
        elif params.debug == "plot":
            # If debug is plot, print to the plotting device
            plot_image(ref_img)
    return roi_contour, roi_hierarchy
