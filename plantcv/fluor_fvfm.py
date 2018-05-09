# Fluorescence Analysis

import os
import cv2
import numpy as np
from . import print_image
from . import plot_image
from . import plot_colorbar
from . import fatal_error


def fluor_fvfm(fdark, fmin, fmax, mask, device, filename, bins=1000, debug=None):
    """Analyze PSII camera images.

    Inputs:
    fdark       = 16-bit grayscale fdark image
    fmin        = 16-bit grayscale fmin image
    fmax        = 16-bit grayscale fmax image
    mask        = mask of plant (binary,single channel)
    device      = counter for debug
    filename    = name of file
    bins        = number of bins from 0 to 65,536 (default is 1000)
    debug       = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device      = device number
    hist_header = fvfm data table headers
    hist_data   = fvfm data table values

    :param fdark: numpy array
    :param fmin: numpy array
    :param fmax: numpy array
    :param mask: numpy array
    :param device: int
    :param filename: str
    :param bins: int
    :param debug: str
    :return device: int
    :return hist_header: list
    :return hist_data: list
    """

    # Auto-increment the device counter
    device += 1
    # Check that fdark, fmin, and fmax are grayscale (single channel)
    if not all(len(np.shape(i)) == 2 for i in [fdark, fmin, fmax]):
        fatal_error("The fdark, fmin, and fmax images must be grayscale images.")
    # Check that fdark, fmin, and fmax are 16-bit images
    if not all(i.dtype == "uint16" for i in [fdark, fmin, fmax]):
        fatal_error("The fdark, fmin, and fmax images must be 16-bit images.")

    # QC Fdark Image
    fdark_mask = cv2.bitwise_and(fdark, fdark, mask=mask)
    if np.amax(fdark_mask) > 2000:
        qc_fdark = False
    else:
        qc_fdark = True

    # Mask Fmin and Fmax Image
    fmin_mask = cv2.bitwise_and(fmin, fmin, mask=mask)
    fmax_mask = cv2.bitwise_and(fmax, fmax, mask=mask)

    # Calculate Fvariable, where Fv = Fmax - Fmin (masked)
    fv = np.subtract(fmax_mask, fmin_mask)

    # When Fmin is greater than Fmax, a negative value is returned.
    # Because the data type is unsigned integers, negative values roll over, resulting in nonsensical values
    # Wherever Fmin is greater than Fmax, set Fv to zero
    fv[np.where(fmax_mask < fmin_mask)] = 0

    # Calculate Fv/Fm (Fvariable / Fmax) where Fmax is greater than zero
    # By definition above, wherever Fmax is zero, Fvariable will also be zero
    # To calculate the divisions properly we need to change from unit16 to float64 data types
    fvfm = fv.astype(np.float64)
    fmax_flt = fmax_mask.astype(np.float64)
    fvfm[np.where(fmax_mask > 0)] /= fmax_flt[np.where(fmax_mask > 0)]

    # Calculate the median Fv/Fm value for non-zero pixels
    fvfm_median = np.median(fvfm[np.where(fvfm > 0)])

    # Calculate the histogram of Fv/Fm non-zero values
    fvfm_hist, fvfm_bins = np.histogram(fvfm[np.where(fvfm > 0)], bins, range=(0, 1))
    # fvfm_bins is a bins + 1 length list of bin endpoints, so we need to calculate bin midpoints so that
    # the we have a one-to-one list of x (FvFm) and y (frequency) values.
    # To do this we add half the bin width to each lower bin edge x-value
    midpoints = fvfm_bins[:-1] + 0.5 * np.diff(fvfm_bins)

    # Calculate which non-zero bin has the maximum Fv/Fm value
    max_bin = midpoints[np.argmax(fvfm_hist)]

    # Store Fluorescence Histogram Data
    hist_header = (
        'HEADER_HISTOGRAM',
        'bin-number',
        'fvfm_bins',
        'fvfm_hist',
        'fvfm_hist_peak',
        'fvfm_median',
        'fdark_passed_qc'
    )

    hist_data = (
        'FLU_DATA',
        bins,
        np.around(midpoints, decimals=len(str(bins))).tolist(),
        fvfm_hist.tolist(),
        float(max_bin),
        float(np.around(fvfm_median, decimals=4)),
        qc_fdark
    )

    if filename:
        import matplotlib
        matplotlib.use('Agg', warn=False)
        from matplotlib import pyplot as plt
        from matplotlib import cm as cm

        # Print F-variable image
        print_image(fv, (str(filename[0:-4]) + '_fv_img.png'))
        print('\t'.join(map(str, ('IMAGE', 'fv', str(filename[0:-4]) + '_fv_img.png'))))

        # Create Histogram Plot, if you change the bin number you might need to change binx so that it prints
        # an appropriate number of labels
        binx = int(bins / 50)
        plt.plot(midpoints, fvfm_hist, color='green', label='Fv/Fm')
        plt.xticks(list(midpoints[0::binx]), rotation='vertical', size='xx-small')
        plt.legend()
        ax = plt.subplot(111)
        ax.set_ylabel('Plant Pixels')
        ax.text(0.05, 0.95, ('Peak Bin Value: ' + str(max_bin)), transform=ax.transAxes, verticalalignment='top')
        plt.grid()
        plt.title('Fv/Fm of ' + str(filename[0:-4]))
        fig_name = (str(filename[0:-4]) + '_fvfm_hist.svg')
        plt.savefig(fig_name)
        plt.clf()
        print('\t'.join(map(str, ('IMAGE', 'hist', fig_name))))

        # Pseudocolored Fv/Fm image
        fvfm_8bit = fvfm * 255
        fvfm_8bit = fvfm_8bit.astype(np.uint8)
        plt.imshow(fvfm_8bit, vmin=0, vmax=1, cmap=cm.jet_r)
        plt.subplot(111)
        mask_inv = cv2.bitwise_not(mask)
        background = np.dstack((mask, mask, mask, mask_inv))
        my_cmap = plt.get_cmap('binary_r')
        plt.imshow(background, cmap=my_cmap)
        plt.axis('off')
        fig_name = (str(filename[0:-4]) + '_pseudo_fvfm.png')
        plt.savefig(fig_name, dpi=600, bbox_inches='tight')
        plt.clf()
        print('\t'.join(map(str, ('IMAGE', 'pseudo', fig_name))))

        path = os.path.dirname(filename)
        fig_name = 'FvFm_pseudocolor_colorbar.svg'
        if not os.path.isfile(path + '/' + fig_name):
            plot_colorbar(path, fig_name, 2)

    if debug == 'print':
        print_image(fmin_mask, (str(device) + '_fmin_mask.png'))
        print_image(fmax_mask, (str(device) + '_fmax_mask.png'))
        print_image(fv, (str(device) + '_fv_convert.png'))
    elif debug == 'plot':
        plot_image(fmin_mask, cmap='gray')
        plot_image(fmax_mask, cmap='gray')
        plot_image(fv, cmap='gray')

    return device, hist_header, hist_data
