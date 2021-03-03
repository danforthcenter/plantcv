import os
import cv2
import numpy as np
import pandas as pd
from scipy import stats
from plotnine import ggplot, aes, geom_line, scale_x_continuous, scale_color_manual, labs
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv.visualize import histogram


def analyze_nir_intensity(gray_img, mask, bins=256, histplot=False, label="default"):
    """This function calculates the intensity of each pixel associated with the plant and writes the values out to
       a file. It can also print out a histogram plot of pixel intensity and a pseudocolor image of the plant.

    Inputs:
    gray_img     = 8- or 16-bit grayscale image data
    mask         = Binary mask made from selected contours
    bins         = number of classes to divide spectrum into
    histplot     = if True plots histogram of intensity values
    label        = optional label parameter, modifies the variable name of observations recorded

    Returns:
    analysis_images = NIR histogram image

    :param gray_img: numpy array
    :param mask: numpy array
    :param bins: int
    :param histplot: bool
    :param label: str
    :return analysis_images: plotnine ggplot
    """
    params.device += 1
    debug = params.debug

    # calculate histogram
    if gray_img.dtype == 'uint16':
        maxval = 65536
    else:
        maxval = 256

    masked_array = gray_img[np.where(mask > 0)]
    masked_nir_mean = np.average(masked_array)
    masked_nir_median = np.median(masked_array)
    masked_nir_std = np.std(masked_array)

    # Make a pseudo-RGB image
    rgbimg = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)

    # Calculate histogram
    params.debug = None
    fig_hist, hist_data = histogram(gray_img, mask=mask, bins=bins, lower_bound=0, upper_bound=maxval, title=None)

    bin_labels, hist_nir, hist_percent = hist_data["pixel intensity"].tolist(), hist_data['hist_count'].tolist(), \
                                         hist_data["proportion of pixels (%)"].tolist()

    masked1 = cv2.bitwise_and(rgbimg, rgbimg, mask=mask)
    params.debug = debug
    if params.debug is not None:
        params.device += 1
        if params.debug == "print":
            print_image(masked1, os.path.join(params.debug_outdir, str(params.device) + "_masked_nir_plant.png"))
        if params.debug == "plot":
            plot_image(masked1)

    analysis_image = None

    if histplot:
        fig_hist = fig_hist + labs(x="Grayscale pixel intensity (0-{})".format(maxval), y="Proportion of pixels (%)")
        if params.debug == "print":
            fig_hist.save(os.path.join(params.debug_outdir, str(params.device) + '_nir_hist.png'), verbose=False)
        elif params.debug == "plot":
            print(fig_hist)
        analysis_image = fig_hist

    outputs.add_observation(sample=label, variable='nir_frequencies', trait='near-infrared frequencies',
                            method='plantcv.plantcv.analyze_nir_intensity', scale='frequency', datatype=list,
                            value=hist_nir, label=bin_labels)
    outputs.add_observation(sample=label, variable='nir_mean', trait='near-infrared mean',
                            method='plantcv.plantcv.analyze_nir_intensity', scale='none', datatype=float,
                            value=masked_nir_mean, label='none')
    outputs.add_observation(sample=label, variable='nir_median', trait='near-infrared median',
                            method='plantcv.plantcv.analyze_nir_intensity', scale='none', datatype=float,
                            value=masked_nir_median, label='none')
    outputs.add_observation(sample=label, variable='nir_stdev', trait='near-infrared standard deviation',
                            method='plantcv.plantcv.analyze_nir_intensity', scale='none', datatype=float,
                            value=masked_nir_std, label='none')

    # Store images
    outputs.images.append(analysis_image)

    return analysis_image

