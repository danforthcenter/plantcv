# Pseudocolor any grayscale image

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from matplotlib import pyplot as plt
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error


def pseudocolor(gray_img, mask=None, cmap=None, min_value=0, max_value=255, path="."):
    """Pseudocolor any grayscale image to custom colormap

        Inputs:
        gray_img    = grayscale image data
        mask        = binary mask
        cmap        = colormap
        min_value   = minimum value for range of interest
        max_value   = maximum value for range of interest
        path        = path for location for saving the image

        Returns:
        pseudo_image = pseudocolored image

        :param gray_img: numpy.ndarray
        :param mask: numpy.ndarray
        :param cmap: str
        :param min_value: int
        :param max_value: int
        :param bins: int
        :param path: str
        :return pseudo_image: numpy.ndarray
        """
    # Auto-increment the device counter
    params.device += 1

    # Check if the image is grayscale
    if len(np.shape(gray_img)) != 2:
        fatal_error("Image must be grayscale.")
    if max != 255:
        # Any pixels above the max_value set to the max value
        gray_img[gray_img > max_value] = max_value
    if min_value != 0:
        # Any pixels below min_value set to the min_value value
        gray_img[gray_img < min_value] = min_value

    # Apply the mask if given
    if mask is not None:
        # Apply the mask
        masked_img = cv2.bitwise_and(gray_img, gray_img, mask=mask)

        # Convert black pixels from 0 to np.nan
        masked_img = np.where(masked_img == 0, np.nan, masked_img)

        # Pseudocolor the image
        pseudo_img = plt.imshow(masked_img, cmap=cmap)

        # Include image title
        plt.title('Pseudocolored image')  # + os.path.splitext(filename)[0])

        # Include the colorbar
        plt.colorbar(fraction=0.033, pad=0.04)

        # Print or plot if debug is turned on
        if params.debug == 'print':
            plt.savefig(os.path.join(path, str(params.device) + '_pseudocolored.png'))
        elif params.debug == 'plot':
            plot_image(pseudo_img)
    else:
        # Pseudocolor the image
        pseudo_img = plt.imshow(gray_img, cmap=cmap)

        # Include image title
        plt.title('Pseudocolored image')  # + os.path.splitext(filename)[0])

        # Include the colorbar
        plt.colorbar(fraction=0.033, pad=0.04)

        # Print or plot if debug is turned on
        if params.debug == 'print':
            plt.savefig(os.path.join(path, str(params.device) + '_pseudocolored.png'))
        elif params.debug == 'plot':
            plot_image(pseudo_img)

    return pseudo_img
