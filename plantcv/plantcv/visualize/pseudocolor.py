# Pseudocolor any grayscale image

import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error


def pseudocolor(gray_img, obj=None, mask=None, cmap=None, background="image", min_value=0, max_value=255,
                axes=True, colorbar=True):
    """Pseudocolor any grayscale image to custom colormap

    Inputs:
    gray_img    = grayscale image data
    obj         = if provided, the pseudocolored image gets cropped down to the region of interest
    mask        = binary mask
    cmap        = colormap
    background  = background color/type, options are "image" (gray_img), "white", or "black"
                  (a mask must be supplied)
    min_value   = minimum value for range of interest
    max_value   = maximum value for range of interest
    axes        = if False then x- and y-axis won't be displayed, nor will the title
    colorbar    = if False then colorbar won't be displayed

    Returns:
    pseudo_image = pseudocolored image

    :param gray_img: numpy.ndarray
    :param obj: numpy.ndarray
    :param mask: numpy.ndarray
    :param cmap: str
    :param background: str
    :param min_value: numeric
    :param max_value: numeric
    :param dpi: int
    :param axes: bool
    :return pseudo_image: numpy.ndarray
    """

    # Auto-increment the device counter
    params.device += 1

    # Make copies of the gray image
    gray_img1 = np.copy(gray_img)

    # Check if the image is grayscale
    if len(np.shape(gray_img)) != 2:
        fatal_error("Image must be grayscale.")

    # Apply the mask if given
    if mask is not None:
        if obj is not None:
            # Copy the image
            img_copy = np.copy(gray_img1)
            # Extract contour size
            x, y, w, h = cv2.boundingRect(obj)
            cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 5)

            # Crop down the image
            crop_img = gray_img[y:y + h, x:x + w]

            # Calculate the buffer size based on the contour size
            offsetx = int(w / 5)
            offsety = int(h / 5)

            if background.upper() == "IMAGE":
                gray_img1 = gray_img1[y - offsety:y + h + offsety, x - offsetx:x + w + offsetx]
            else:
                # Crop img including buffer
                gray_img1 = cv2.copyMakeBorder(crop_img, offsety, offsety, offsetx, offsetx, cv2.BORDER_CONSTANT,
                                               value=(0, 0, 0))

            # Crop the mask to the same size as the image
            crop_mask = mask[y:y + h, x:x + w]
            mask = cv2.copyMakeBorder(crop_mask, offsety, offsety, offsetx, offsetx, cv2.BORDER_CONSTANT,
                                      value=(0, 0, 0))

        # Apply the mask
        masked_img = np.ma.array(gray_img1, mask=~mask.astype(np.bool))

        # Set the background color or type
        if background.upper() == "BLACK":
            # Background is all zeros
            bkg_img = np.zeros(np.shape(gray_img1), dtype=np.uint8)
            # Use the gray cmap for the background
            bkg_cmap = "gray"
        elif background.upper() == "WHITE":
            # Background is all 255 (white)
            bkg_img = np.zeros(np.shape(gray_img1), dtype=np.uint8)
            bkg_img += 255
            bkg_cmap = "gray"
        elif background.upper() == "IMAGE":
            # Set the background to the input gray image
            bkg_img = gray_img1
            bkg_cmap = "gray"
        else:
            fatal_error(
                "Background type {0} is not supported. Please use 'white', 'black', or 'image'.".format(background))

        # Pseudocolor the image, plot the background first
        pseudo_img1 = plt.imshow(bkg_img, cmap=bkg_cmap, vmin=min_value, vmax=max_value)
        # Overlay the masked grayscale image with the user input colormap
        plt.imshow(masked_img, cmap=cmap, vmin=min_value, vmax=max_value)

        if colorbar:
            plt.colorbar(fraction=0.033, pad=0.04)

        if axes:
            # Include image title
            plt.title('Pseudocolored image')
        else:
            # Remove axes
            plt.xticks([])
            plt.yticks([])

        # Store the current figure
        pseudo_img = plt.gcf()

        # Print or plot if debug is turned on
        if params.debug == 'print':
            plt.savefig(os.path.join(params.debug_outdir, str(params.device) + '_pseudocolored.png'), dpi=params.dpi)
            plt.close()
        elif params.debug == 'plot':
            plot_image(pseudo_img1)
            # Use non-blocking mode in case the function is run more than once
            plt.show(block=False)
        elif params.debug == None:
            plt.show(block=False)

    else:
        # Pseudocolor the image
        pseudo_img1 = plt.imshow(gray_img1, cmap=cmap, vmin=min_value, vmax=max_value)

        if colorbar:
            # Include the colorbar
            plt.colorbar(fraction=0.033, pad=0.04)

        if axes:
            # Include image title
            plt.title('Pseudocolored image')  # + os.path.splitext(filename)[0])
        else:
            # Remove axes
            plt.xticks([])
            plt.yticks([])

        pseudo_img = plt.gcf()

        # Print or plot if debug is turned on
        if params.debug == 'print':
            plt.savefig(os.path.join(params.debug_outdir, str(params.device) + '_pseudocolored.png'), dpi=params.dpi)
            pseudo_img.clear()
            plt.close()
        elif params.debug == 'plot':
            plot_image(pseudo_img1)
            # Use non-blocking mode in case the function is run more than once
            plt.show(block=False)
        elif params.debug == None:
            plt.show(block=False)

    return pseudo_img
