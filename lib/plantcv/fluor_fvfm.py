# Fluorescence Analysis

import os
import cv2
import numpy as np
from . import print_image
from . import plot_image
from . import plot_colorbar


def fluor_fvfm(fdark, fmin, fmax, mask, device, filename, bins=1000, debug=None):
    """Analyze PSII camera images.

    Inputs:
    fdark       = 16-bit fdark image
    fmin        = 16-bit fmin image
    fmax        = 16-bit fmax image
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

    device += 1
    if len(np.shape(fmax)) == 3:
        ix, iy, iz = np.shape(fmax)
    else:
        ix, iy = np.shape(fmax)

    size = ix, iy
    background = np.zeros(size, dtype=np.uint8)
    w_back = background + 255

    # QC Fdark Image
    fdark_mask = cv2.bitwise_and(fdark, fdark, mask=mask)
    if np.amax(fdark_mask) > 2000:
        qc_fdark = False
    else:
        qc_fdark = True

    # Mask Fmin and Fmax Image
    fmin_mask = cv2.bitwise_and(fmin, fmin, mask=mask)
    fmax_mask = cv2.bitwise_and(fmax, fmax, mask=mask)

    # Calculate Fvariable
    if len(np.shape(fmax)) == 3:
        ix, iy, iz = np.shape(fmax)
    else:
        ix, iy = np.shape(fmax)
    shape = ix, iy

    fv = []
    fmax_flat = fmax_mask.flatten()
    fmin_flat = fmin_mask.flatten()

    for i, c in enumerate(fmax_flat):
        if fmax_flat[i] <= fmin_flat[i]:
            fv1 = 0
            fv.append(fv1)
        else:
            fv1 = fmax_flat[i] - fmin_flat[i]
            fv.append(fv1)

    fv_nan = np.isnan(fv)
    for i, c in enumerate(fv_nan):
        if fv_nan[i] == True:
            fv[i] = 0
        else:
            pass

    fv2 = np.array(fv, dtype=np.uint16)
    fv3 = np.reshape(fv2, shape)
    fv_img = fv3

    # Calculate Fv/Fm
    fvfm = []
    fm = np.hstack(fmax_flat)
    fv1 = np.array([float(i) for i in fv], dtype=np.float)
    fm1 = np.array([float(i) for i in fm], dtype=np.float)

    for i, c in enumerate(fm1):
        fvfm1 = fv1[i] / fm1[i]
        if np.isnan(fvfm1) == True:
            fvfm2 = 0
            fvfm.append(fvfm2)
        elif np.isinf(fvfm1) == True:
            fvfm2 = 0
            fvfm.append(fvfm2)
        elif np.isneginf(fvfm1) == True:
            fvfm2 = 0
            fvfm.append(fvfm2)
        else:
            fvfm2 = fvfm1
            fvfm.append(fvfm2)

    # Make Fv/Fm Histogram for Non-Zero Values
    fvfm_nonzero = [e for i, e in enumerate(fvfm) if e != 0]
    fvfm_nonzero_hist = np.array(fvfm_nonzero, dtype=np.float)
    fvfm_median = np.median(fvfm_nonzero_hist)
    fvfm_hist, fvfm_bins = np.histogram(fvfm_nonzero_hist, bins, range=(0, 1))
    lower = np.resize(fvfm_bins, len(fvfm_bins) - 1)
    tmid = lower + 0.5 * np.diff(fvfm_bins)
    tmid_list = [l for l in tmid]
    fvfm_hist_list = [l for l in fvfm_hist]
    fvfm_hist_max = np.argmax(fvfm_hist)
    max_bin = tmid[fvfm_hist_max]

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
        tmid_list,
        fvfm_hist_list,
        max_bin,
        fvfm_median,
        qc_fdark
    )

    # Histogram Visualization Slice (normalized to 255 for size)
    fvfm_max = np.amax(fvfm_hist)
    fvfm_min = np.amin(fvfm_hist)
    hist_shape = np.shape(fvfm_hist)
    hist_float = np.array([float(i) for i in fvfm_hist], dtype=np.float)
    hist_background = np.zeros(hist_shape, dtype=np.uint8)
    fvfm_norm_slice = np.array((((hist_float - fvfm_min) / (fvfm_max - fvfm_min)) * 255), dtype=np.uint8)
    fvfm_stack = np.dstack((hist_background, hist_background, fvfm_norm_slice))
    if filename:
        import matplotlib
        matplotlib.use('Agg')
        from matplotlib import pyplot as plt
        from matplotlib import cm as cm
        from matplotlib import colors as colors
        from matplotlib import colorbar as colorbar

        # Print Fv image
        print_image(fv_img, (str(filename[0:-4]) + '_fv_img.png'))
        print('\t'.join(map(str, ('IMAGE', 'fv', str(filename[0:-4]) + '_fv_img.png'))))

        # Print FvFm slice
        print_image(fvfm_stack, (str(filename[0:-4]) + '_fvfm_hist_slice.png'))
        print('\t'.join(map(str, ('IMAGE', 'slice', fig_name))))

        # Create Histogram Plot, if you change the bin number you might need to change binx so that it prints an appropriate number of labels
        binx = bins / 50
        fvfm_plot = plt.plot(tmid, fvfm_hist, color='green', label='FvFm')
        plt.xticks(list(tmid[0::binx]), rotation='vertical', size='xx-small')
        legend = plt.legend()
        ax = plt.subplot(111)
        ax.set_ylabel('Plant Pixels')
        ax.text(0.05, 0.95, ('Peak Bin Value: ' + str(max_bin)), transform=ax.transAxes, verticalalignment='top')
        plt.grid()
        plt.title('Fv/Fm of ' + str(filename[0:-4]))
        fig_name = (str(filename[0:-4]) + '_fvfm_hist.svg')
        plt.savefig(fig_name)
        plt.clf()
        print('\t'.join(map(str, ('IMAGE', 'hist', fig_name))))


        # Pseudocolor FvFm image
        ix, iy = np.shape(fmax)
        size = ix, iy
        background = np.zeros(size)
        w_back = background + 1
        fvfm1 = np.array(fvfm, dtype=np.float)
        fvfm256 = fvfm1 * 255
        fvfm_p = np.array(fvfm256, dtype=np.uint8)
        fvfm_pshape = np.reshape(fvfm_p, shape)
        fvfm_pstack = np.dstack((fvfm_pshape, fvfm_pshape, fvfm_pshape))

        fvfm_img = plt.imshow(fvfm_pshape, vmin=0, vmax=255, cmap=cm.jet_r)
        ax = plt.subplot(111)
        # bar=plt.colorbar(orientation='horizontal', ticks=[0,25.5, 51,76.5, 102, 127.5, 153, 178.5, 204, 229.5, 255])
        # bar.ax.set_xticklabels([0.0,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        mask_inv = cv2.bitwise_not(mask)
        background1 = np.dstack((mask, mask, mask, mask_inv))
        my_cmap = plt.get_cmap('binary_r')
        plt.imshow(background1, cmap=my_cmap)
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
        print_image(fv3, (str(device) + '_fv_convert.png'))
    elif debug == 'plot':
        plot_image(fmin_mask, cmap='gray')
        plot_image(fmax_mask, cmap='gray')
        plot_image(fv3, cmap='gray')

    return device, hist_header, hist_data
