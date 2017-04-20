# White Balance correction function by Monica Tessman and Malia Gehan

import cv2
import numpy as np
from . import print_image
from . import plot_image
from . import apply_mask
from . import fatal_error


def white_balance(device, img, debug=None, roi=None):
    """Corrects the exposure of an image based on its histogram.

    Inputs:
    device  = pipeline step counter
    img     = An RGB image on which to perform the correction, correction is done on each channel and then reassembled,
              alternatively a single channel can be input but is not recommended.
    debug   = None, print, or plot. Print = save to file, Plot = print to screen.
    roi     = A list of 4 points (x, y, width, height) that form the rectangular ROI of the white color standard.
              If a list of 4 points is not given, whole image will be used.

    Returns:
    device  = pipeline step counter
    img     = Image after exposure correction

    :param device: int
    :param img: ndarray
    :param debug: str
    :param roi: list
    """
    device += 1

    ori_img = np.copy(img)

    if roi is not None:
        roiint = all(isinstance(item, int) for item in roi)

        if len(roi) != 4 | roiint is False:
            fatal_error('If ROI is used ROI must have 4 elements as a list and all must be integers')
    else:
        pass

    if len(np.shape(img)) == 3:
        iy, ix, iz = np.shape(img)
        mask = np.zeros((iy, ix, 3), dtype=np.uint8)
        ori_img2 = np.copy(ori_img)

        if roi is None:
            x = 0
            y = 0
            w = ix
            h = iy

        else:
            x = roi[0]
            y = roi[1]
            w = roi[2]
            h = roi[3]

        cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), -1)
        cv2.rectangle(ori_img, (x, y), (x + w, y + h), (0, 255, 0), 3)

        mask_binary = mask[:, :, 0]
        retval, mask_binary = cv2.threshold(mask_binary, 254, 255, cv2.THRESH_BINARY)

        _, masked = apply_mask(ori_img2, mask_binary, 'black', 0, debug=None)

        channel1 = np.amax(masked[:, :, 0])
        channel2 = np.amax(masked[:, :, 1])
        channel3 = np.amax(masked[:, :, 2])

        alpha1 = 255 / float(channel1)

        alpha2 = 255 / float(channel2)

        alpha3 = 255 / float(channel3)

        # Converts values greater than hmax to 255 and scales all others by alpha

        correctedimg1 = np.asarray(np.where(img[:, :, 0] <= channel1, np.multiply(alpha1, img[:, :, 0]), 255), np.uint8)
        correctedimg2 = np.asarray(np.where(img[:, :, 1] <= channel2, np.multiply(alpha2, img[:, :, 1]), 255), np.uint8)
        correctedimg3 = np.asarray(np.where(img[:, :, 2] <= channel3, np.multiply(alpha3, img[:, :, 2]), 255), np.uint8)

        finalcorrected = np.dstack((correctedimg1, correctedimg2, correctedimg3))

        if debug == 'print':
            print_image(ori_img, (str(device) + '_whitebalance_roi.png'))
            print_image(finalcorrected, (str(device) + '_whitebalance.png'))
        elif debug == 'plot':
            if len(np.shape(ori_img)) == 3:
                plot_image(ori_img)
                plot_image(finalcorrected)
            else:
                plot_image(ori_img, cmap='gray')
                plot_image(finalcorrected, cmap='gray')

        return device, finalcorrected

    else:
        if img.dtype == 'uint8':

            if roi is not None:
                x = roi[0]
                y = roi[1]
                w = roi[2]
                h = roi[3]

                hist = cv2.calcHist(tuple(img[y:y + h, x:x + w]), [0], None, [256], [0, 256])
                cv2.rectangle(ori_img, (x, y), (x + w, y + h), (0, 255, 0), 3)

            else:
                hist = cv2.calcHist(tuple(img), [0], None, [256], [0, 256])  # Creates histogram of original image

            hmax = np.argmax(hist)
            alpha = 255 / float(hmax)
            finalcorrected = np.asarray(np.where(img <= hmax, np.multiply(alpha, img), 255), np.uint8)

        elif img.dtype == 'uint16':

            if roi is not None:
                x = roi[0]
                y = roi[1]
                w = roi[2]
                h = roi[3]

                hist, bins = np.histogram(img[y:y + h, x:x + w], bins='auto')
                cv2.rectangle(ori_img, (x, y), (x + w, y + h), (0, 0, 0), 3)

            else:
                hist, bins = np.histogram(img, bins='auto')

            hmax = np.amax(bins)
            alpha = 65536 / float(hmax)
            finalcorrected = np.asarray(np.where(img <= hmax, np.multiply(alpha, img), 65536), np.uint16)

        # Calculates index of maximum of histogram and finds alpha based on the peak

        if debug == 'print':
            print_image(ori_img, (str(device) + '_whitebalance_roi.png'))
            print_image(finalcorrected, (str(device) + '_whitebalance.png'))

        elif debug == 'plot':
            if len(np.shape(img))== 3:
                plot_image(ori_img)
                plot_image(finalcorrected)
            else:
                plot_image(ori_img, cmap='gray')
                plot_image(finalcorrected, cmap='gray')

        return device, finalcorrected
