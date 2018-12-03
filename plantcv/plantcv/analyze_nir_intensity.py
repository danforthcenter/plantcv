# Analyze signal data in NIR image

import os
import cv2
import numpy as np
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import plot_colorbar
from plantcv.plantcv.threshold import binary as binary_threshold
from plantcv.plantcv import apply_mask
from plantcv.plantcv import params


def analyze_nir_intensity(gray_img, mask, bins, histplot=False, filename=False):
    """This function calculates the intensity of each pixel associated with the plant and writes the values out to
       a file. It can also print out a histogram plot of pixel intensity and a pseudocolor image of the plant.

    Inputs:
    gray_img     = 8- or 16-bit grayscale image data
    mask         = Binary mask made from selected contours
    bins         = number of classes to divide spectrum into
    histplot     = if True plots histogram of intensity values
    filename     = False or image name. If defined print image

    Returns:
    hist_header  = NIR histogram data table headers
    hist_data    = NIR histogram data table values
    analysis_img = output image

    :param gray_img: numpy array
    :param mask: numpy array
    :param bins: int
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
    masked = np.multiply(gray_img, mask1)

    # calculate histogram
    if gray_img.dtype == 'uint16':
        maxval = 65536
    else:
        maxval = 256

    # Make a pseudo-RGB image
    rgbimg = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)

    hist_nir, hist_bins = np.histogram(masked, bins, (1, maxval), False, None, None)

    hist_bins1 = hist_bins[:-1]
    hist_bins2 = [l for l in hist_bins1]

    hist_nir1 = [l for l in hist_nir]

    # make hist percentage for plotting
    pixels = cv2.countNonZero(mask1)
    hist_percent = (hist_nir / float(pixels)) * 100

    # report histogram data
    hist_header = [
        'HEADER_HISTOGRAM',
        'bin-number',
        'bin-values',
        'nir'
    ]

    hist_data = [
        'HISTOGRAM_DATA',
        bins,
        hist_bins2,
        hist_nir1
    ]

    analysis_img = []

    # make mask to select the background
    mask_inv = cv2.bitwise_not(mask)
    img_back = cv2.bitwise_and(rgbimg, rgbimg, mask=mask_inv)
    img_back1 = cv2.applyColorMap(img_back, colormap=1)

    # mask the background and color the plant with color scheme 'jet'
    cplant = cv2.applyColorMap(rgbimg, colormap=2)
    masked1 = apply_mask(cplant, mask, 'black')
    cplant_back = cv2.add(masked1, img_back1)

    if filename:
        path = os.path.dirname(filename)
        fig_name = 'NIR_pseudocolor_colorbar.svg'
        if not os.path.isfile(path + '/' + fig_name):
            plot_colorbar(path, fig_name, bins)

        fig_name_pseudo = (os.path.splitext(filename)[0] + '_nir_pseudo_col.jpg')
        print_image(cplant_back, fig_name_pseudo)
        analysis_img.append(['IMAGE', 'pseudo', fig_name_pseudo])

    if params.debug is not None:
        if params.debug == "print":
            print_image(masked1, os.path.join(params.debug_outdir, str(params.device) + "_nir_pseudo_plant.jpg"))
            print_image(cplant_back,
                        os.path.join(params.debug_outdir, str(params.device) + "_nir_pseudo_plant_back.jpg"))
        if params.debug == "plot":
            plot_image(masked1)
            plot_image(cplant_back)

    if histplot is True:
        import matplotlib
        matplotlib.use('Agg', warn=False)
        from matplotlib import pyplot as plt

        # plot hist percent
        plt.plot(hist_percent, color='green', label='Signal Intensity')
        plt.xlim([0, (bins - 1)])
        plt.xlabel(('Grayscale pixel intensity (0-' + str(bins) + ")"))
        plt.ylabel('Proportion of pixels (%)')

        if filename:
            fig_name_hist = (os.path.splitext(filename)[0] + '_nir_hist.svg')
            plt.savefig(fig_name_hist)
            analysis_img.append(['IMAGE', 'hist', fig_name_hist])
        if params.debug == "print":
            plt.savefig(os.path.join(params.debug_outdir, str(params.device) + "_nir_histogram.png"))
        if params.debug == "plot":
            plt.figure()
        plt.clf()

    return hist_header, hist_data, analysis_img
