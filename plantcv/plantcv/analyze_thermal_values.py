# Analyze signal data in Thermal image

import os
import cv2
import numpy as np
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import plot_colorbar
from plantcv.plantcv.threshold import binary as binary_threshold
from plantcv.plantcv import apply_mask
from plantcv.plantcv import params


def analyze_thermal_values(rgb_img, array, mask, name,histplot=False, filename=False):
    """This extracts the thermal values of each pixel writes the values out to
       a file. It can also print out a histogram plot of pixel intensity
       and a pseudocolor image of the plant.

    Inputs:
    rgb_img      = rgb image to create pseudocolored img
    array        = numpy array of thermal values
    mask         = Binary mask made from selected contours
    histplot     = if True plots histogram of intensity values
    filename     = False or image name. If defined print image

    Returns:
    hist_header  = thermal histogram data table headers
    hist_data    = thermal histogram data table values
    analysis_img = output image

    :param rgb_img: numpy array
    :param array: numpy array
    :param mask: numpy array
    :param histplot: bool
    :param filename: str
    :return hist_header: list
    :return hist_data: list
    :return analysis_img: str
    """
    params.device += 1

    # apply plant shaped mask to image
    mask1 = binary_threshold(mask, 0, 255, 'light')
    mask1 = (mask1 / 255)
    masked = np.multiply(mask1, array)
    nonzero = masked[np.nonzero(masked)]

    hist_therm, hist_bins = np.histogram(nonzero, range=(np.amin(array), np.amax(array)))
    maxtemp = np.amax(nonzero)
    mintemp = np.amin(nonzero)
    avgtemp = np.average(nonzero)
    mediantemp = np.median(nonzero)

    hist_bins1 = hist_bins[:-1]
    hist_bins2 = [l for l in hist_bins1]

    hist_therm1 = [l for l in hist_therm]

    # make hist percentage for plotting
    pixels = cv2.countNonZero(mask1)
    hist_percent = (hist_therm / float(pixels)) * 100

    # report histogram data
    hist_header = [
        'HEADER_HISTOGRAM',
        'name'
        'max-temp',
        'min-temp,'
        'average-temp',
        'median-temp',
        'bin-values',
        'thermal'
    ]

    hist_data = [
        'HISTOGRAM_DATA',
        name,
        maxtemp,
        mintemp,
        avgtemp,
        mediantemp,
        hist_bins2,
        hist_therm1
    ]

    analysis_img = []

    # make mask to select the background
    mask_inv = cv2.bitwise_not(mask)
    img_back = cv2.bitwise_and(rgb_img, rgb_img, mask=mask_inv)
    img_back1 = cv2.applyColorMap(img_back, colormap=1)

    # mask the background and color the plant with color scheme 'jet'
    cplant = cv2.applyColorMap(rgb_img, colormap=2)
    masked1 = apply_mask(cplant, mask, 'black')
    cplant_back = cv2.add(masked1, img_back1)

    if filename:
        path = os.path.dirname(filename)
        fig_name = 'therm_pseudocolor_colorbar.svg'
        if not os.path.isfile(path + '/' + fig_name):
            plot_colorbar(path, fig_name, bins)

        fig_name_pseudo = (str(filename[0:-4]) + '_therm_pseudo_col.jpg')
        print_image(cplant_back, fig_name_pseudo)
        analysis_img.append(['IMAGE', 'pseudo', fig_name_pseudo])

    if params.debug is not None:
        if params.debug == "print":
            print_image(masked1, os.path.join(params.debug_outdir, str(params.device) + "_therm_pseudo_plant.jpg"))
            print_image(cplant_back,
                        os.path.join(params.debug_outdir, str(params.device) + "_therm_pseudo_plant_back.jpg"))
        if params.debug == "plot":
            plot_image(masked1)
            plot_image(cplant_back)

    if histplot is True:
        import matplotlib
        matplotlib.use('Agg', warn=False)
        from matplotlib import pyplot as plt

        # plot hist percent
        plt.plot(hist_percent, color='green', label='Signal Intensity')
        plt.xticks(np.arange(10), hist_bins2, rotation=90)
        plt.xlabel(('Tempurature C'))
        plt.ylabel('Proportion of pixels (%)')

        if filename:
            fig_name_hist = (str(filename[0:-4]) + '_therm_hist.svg')
            plt.savefig(fig_name_hist)
            analysis_img.append(['IMAGE', 'hist', fig_name_hist])
        if params.debug == "print":
            plt.savefig(os.path.join(params.debug_outdir, str(params.device) + "_therm_histogram.png"))
        if params.debug == "plot":
            plt.figure()
        plt.clf()

    return hist_header, hist_data, analysis_img
