# Fluorescence Analysis

import os
import cv2
import numpy as np
import pandas as pd
from plotnine import ggplot, geom_label, aes, geom_line
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def fluor_fvfm(fdark, fmin, fmax, mask, bins=256):
    """Analyze PSII camera images.
    Inputs:
    fdark       = grayscale fdark image
    fmin        = grayscale fmin image
    fmax        = grayscale fmax image
    mask        = mask of plant (binary, single channel)
    bins        = number of bins (1 to 256 for 8-bit; 1 to 65,536 for 16-bit; default is 256)
    Returns:
    analysis_images = list of images (fv image and fvfm histogram image)
    :param fdark: numpy.ndarray
    :param fmin: numpy.ndarray
    :param fmax: numpy.ndarray
    :param mask: numpy.ndarray
    :param bins: int
    :return analysis_images: numpy.ndarray
    """

    # Auto-increment the device counter
    params.device += 1
    # Check that fdark, fmin, and fmax are grayscale (single channel)
    if not all(len(np.shape(i)) == 2 for i in [fdark, fmin, fmax]):
        fatal_error("The fdark, fmin, and fmax images must be grayscale images.")
    # # Check that fdark, fmin, and fmax are the same bit
    # if  not (all(i.dtype == "uint16" for i in [fdark, fmin, fmax]) or
    #         (all(i.dtype == "uint8" for i in [fdark, fmin, fmax]))):
    #     fatal_error("The fdark, fmin, and fmax images must all be the same bit depth.")
    # Check that fdark, fmin, and fmax are 16-bit images
    # if not all(i.dtype == "uint16" for i in [fdark, fmin, fmax]):
    #     fatal_error("The fdark, fmin, and fmax images must be 16-bit images.")

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
    analysis_images = []
    analysis_images.append(fv)

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

    # Print F-variable image
    # print_image(fv, (os.path.splitext(filename)[0] + '_fv_img.png'))
    # analysis_images.append(['IMAGE', 'fv', os.path.splitext(filename)[0] + '_fv_img.png'])

    # Create Histogram Plot, if you change the bin number you might need to change binx so that it prints
    # an appropriate number of labels
    # Create a dataframe
    dataset = pd.DataFrame({'Plant Pixels': fvfm_hist, 'Fv/Fm': midpoints})
    # Make the histogram figure using plotnine
    fvfm_hist_fig = (ggplot(data=dataset, mapping=aes(x='Fv/Fm', y='Plant Pixels'))
                     + geom_line(color='green', show_legend=True)
                     + geom_label(label='Peak Bin Value: ' + str(max_bin),
                                  x=.15, y=205, size=8, color='green'))
    analysis_images.append(fvfm_hist_fig)

    # Changed histogram method over from matplotlib pyplot to plotnine
    # binx = int(bins / 50)
    # plt.plot(midpoints, fvfm_hist, color='green', label='Fv/Fm')
    # plt.xticks(list(midpoints[0::binx]), rotation='vertical', size='xx-small')
    # plt.legend()
    # ax = plt.subplot(111)
    # ax.set_ylabel('Plant Pixels')
    # ax.text(0.05, 0.95, ('Peak Bin Value: ' + str(max_bin)), transform=ax.transAxes, verticalalignment='top')
    # plt.grid()
    # plt.title('Fv/Fm of ' + os.path.splitext(filename)[0])
    # fig_name = (os.path.splitext(filename)[0] + '_fvfm_hist.svg')
    # plt.savefig(fig_name)
    # plt.clf()
    # analysis_images.append(['IMAGE', 'fvfm_hist', fig_name])

    # No longer pseudocolor the image, instead can be pseudocolored by pcv.pseudocolor
    # # Pseudocolored Fv/Fm image
    # plt.imshow(fvfm, vmin=0, vmax=1, cmap="viridis")
    # plt.colorbar()
    # # fvfm_8bit = fvfm * 255
    # # fvfm_8bit = fvfm_8bit.astype(np.uint8)
    # # plt.imshow(fvfm_8bit, vmin=0, vmax=1, cmap=cm.jet_r)
    # # plt.subplot(111)
    # # mask_inv = cv2.bitwise_not(mask)
    # # background = np.dstack((mask, mask, mask, mask_inv))
    # # my_cmap = plt.get_cmap('binary_r')
    # # plt.imshow(background, cmap=my_cmap)
    # plt.axis('off')
    # fig_name = (os.path.splitext(filename)[0] + '_pseudo_fvfm.png')
    # plt.savefig(fig_name, dpi=600, bbox_inches='tight')
    # plt.clf()
    # analysis_images.append(['IMAGE', 'fvfm_pseudo', fig_name])

    # path = os.path.dirname(filename)
    # fig_name = 'FvFm_pseudocolor_colorbar.svg'
    # if not os.path.isfile(os.path.join(path, fig_name)):
    #     plot_colorbar(path, fig_name, 2)

    if params.debug == 'print':
        print_image(fmin_mask, os.path.join(params.debug_outdir, str(params.device) + '_fmin_mask.png'))
        print_image(fmax_mask, os.path.join(params.debug_outdir, str(params.device) + '_fmax_mask.png'))
        print_image(fv, os.path.join(params.debug_outdir, str(params.device) + '_fv_convert.png'))
        fvfm_hist_fig.save(os.path.join(params.debug_outdir, str(params.device) + '_fv_hist.png'))
    elif params.debug == 'plot':
        plot_image(fmin_mask, cmap='gray')
        plot_image(fmax_mask, cmap='gray')
        plot_image(fv, cmap='gray')
        print(fvfm_hist_fig)

    outputs.add_observation(variable='fvfm_hist', trait='Fv/Fm frequencies',
                            method='plantcv.plantcv.fluor_fvfm', scale='none', datatype=list,
                            value=fvfm_hist.tolist(), label=np.around(midpoints, decimals=len(str(bins))).tolist())
    outputs.add_observation(variable='fvfm_hist_peak', trait='peak Fv/Fm value',
                            method='plantcv.plantcv.fluor_fvfm', scale='none', datatype=float,
                            value=float(max_bin), label='none')
    outputs.add_observation(variable='fvfm_median', trait='Fv/Fm median',
                            method='plantcv.plantcv.fluor_fvfm', scale='none', datatype=float,
                            value=float(np.around(fvfm_median, decimals=4)), label='none')
    outputs.add_observation(variable='fdark_passed_qc', trait='Fdark passed QC',
                            method='plantcv.plantcv.fluor_fvfm', scale='none', datatype=bool,
                            value=qc_fdark, label='none')

    # Store images
    outputs.images.append(analysis_images)

    return analysis_images
