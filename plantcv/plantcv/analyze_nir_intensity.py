# Analyze signal data in NIR image

import os
import cv2
import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_line, scale_x_continuous
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv.threshold import binary as binary_threshold
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def analyze_nir_intensity(gray_img, mask, bins=256, histplot=False):
    """This function calculates the intensity of each pixel associated with the plant and writes the values out to
       a file. It can also print out a histogram plot of pixel intensity and a pseudocolor image of the plant.

    Inputs:
    gray_img     = 8- or 16-bit grayscale image data
    mask         = Binary mask made from selected contours
    bins         = number of classes to divide spectrum into
    histplot     = if True plots histogram of intensity values

    Returns:
    analysis_images = NIR histogram image

    :param gray_img: numpy array
    :param mask: numpy array
    :param bins: int
    :param histplot: bool
    :return analysis_images: plotnine ggplot
    """

    params.device += 1

    # apply plant shaped mask to image
    mask1 = binary_threshold(mask, 0, 255, 'light')
    mask1 = (mask1 / 255)
    # masked = np.multiply(gray_img, mask1)

    # calculate histogram
    if gray_img.dtype == 'uint16':
        maxval = 65536
    else:
        maxval = 256

    # Make a pseudo-RGB image
    rgbimg = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)

    # Calculate histogram
    hist_nir = [float(l[0]) for l in cv2.calcHist([gray_img], [0], mask, [bins], [0, maxval])]
    # Create list of bin labels
    bin_width = maxval / float(bins)
    b = 0
    bin_labels = [float(b)]
    for i in range(bins - 1):
        b += bin_width
        bin_labels.append(b)

    # make hist percentage for plotting
    pixels = cv2.countNonZero(mask1)
    hist_percent = [(p / float(pixels)) * 100 for p in hist_nir]

    # No longer returning a pseudocolored image
    # make mask to select the background
    # mask_inv = cv2.bitwise_not(mask)
    # img_back = cv2.bitwise_and(rgbimg, rgbimg, mask=mask_inv)
    # img_back1 = cv2.applyColorMap(img_back, colormap=1)

    # mask the background and color the plant with color scheme 'jet'
    # cplant = cv2.applyColorMap(rgbimg, colormap=2)
    # masked1 = apply_mask(cplant, mask, 'black')
    masked1 = cv2.bitwise_and(rgbimg, rgbimg, mask=mask)
    # cplant_back = cv2.add(masked1, img_back1)
    if params.debug is not None:
        if params.debug == "print":
            print_image(masked1, os.path.join(params.debug_outdir, str(params.device) + "_masked_nir_plant.jpg"))
        if params.debug == "plot":
            plot_image(masked1)

    analysis_image = None

    if histplot is True:
        hist_x = hist_percent
        # bin_labels = np.arange(0, bins)
        dataset = pd.DataFrame({'Grayscale pixel intensity': bin_labels,
                                'Proportion of pixels (%)': hist_x})
        fig_hist = (ggplot(data=dataset,
                           mapping=aes(x='Grayscale pixel intensity',
                                       y='Proportion of pixels (%)'))
                    + geom_line(color='red')
                    + scale_x_continuous(breaks=list(range(0, maxval, 25))))

        analysis_image = fig_hist
        if params.debug == "print":
            fig_hist.save(os.path.join(params.debug_outdir, str(params.device) + '_nir_hist.png'))
        elif params.debug == "plot":
            print(fig_hist)

    outputs.add_observation(variable='nir_frequencies', trait='near-infrared frequencies',
                            method='plantcv.plantcv.analyze_nir_intensity', scale='frequency', datatype=list,
                            value=hist_nir, label=bin_labels)

    # Store images
    outputs.images.append(analysis_image)

    return analysis_image
