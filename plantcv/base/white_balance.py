# White Balance correction function by Monica Tessman and Malia Gehan

import cv2
import numpy as np
from plantcv.base import print_image
from plantcv.base import plot_image
from plantcv.base import apply_mask
from plantcv.base import fatal_error



def _hist(img, hmax, x,y,h,w,type):
    hist, bins = np.histogram(img[y:y + h, x:x + w], bins='auto')
    max1 = np.amax(bins)
    alpha = hmax / float(max1)
    corrected = np.asarray(np.where(img <= max1, np.multiply(alpha, img), hmax), type)

    return corrected

def _max(img, hmax,mask,x,y,h,w,type):
    imgcp = np.copy(img)
    cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), -1)
    mask_binary = mask[:, :, 0]
    retval, mask_binary = cv2.threshold(mask_binary, 254, 255, cv2.THRESH_BINARY)
    _, masked = apply_mask(imgcp, mask_binary, 'black', 0, debug=None)
    max1 = np.amax(masked)
    alpha = hmax / float(max1)
    corrected = np.asarray(np.where(img <= max1, np.multiply(alpha, img), hmax), type)

    return corrected

def white_balance(device, img, mode='hist',debug=None, roi=None):
    """Corrects the exposure of an image based on its histogram.

    Inputs:
    device  = pipeline step counter
    img     = An RGB image on which to perform the correction, correction is done on each channel and then reassembled,
              alternatively a single channel can be input but is not recommended.
    mode    = 'hist or 'max'
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
        hmax=255
        type = np.uint8
    else:
        iy, ix = np.shape(img)
        if img.dtype == 'uint8':
            hmax=255
            type=np.uint8
        elif img.dtype == 'uint16':
            hmax=65536
            type=np.uint16

    mask = np.zeros((iy, ix, 3), dtype=np.uint8)

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

    if len(np.shape(img)) == 3:
        cv2.rectangle(ori_img, (x, y), (x + w, y + h), (0, 255, 0), 3)
        c1 = img[:, :, 0]
        c2 = img[:, :, 1]
        c3 = img[:, :, 2]
        if mode == 'hist':
            channel1 = _hist(c1, hmax, x, y, h, w, type)
            channel2 = _hist(c2, hmax, x, y, h, w, type)
            channel3 = _hist(c3, hmax, x, y, h, w, type)
        else:
            channel1 = _max(c1, hmax, mask, x, y, h, w, type)
            channel2 = _max(c2, hmax, mask, x, y, h, w, type)
            channel3 = _max(c3, hmax, mask, x, y, h, w, type)

        finalcorrected = np.dstack((channel1, channel2, channel3))

    else:
        cv2.rectangle(ori_img, (x, y), (x + w, y + h), (255, 255, 255), 3)
        if mode == 'hist':
            finalcorrected = _hist(img, hmax, x, y, h, w, type)
        elif mode == 'max':
            finalcorrected = _max(img, hmax, mask, x, y, h, w, type)

    if debug == 'print':
        print_image(ori_img, (str(device) + '_whitebalance_roi.png'))
        print_image(finalcorrected, (str(device) + '_whitebalance.png'))

    elif debug == 'plot':
        plot_image(ori_img, cmap='gray')
        plot_image(finalcorrected, cmap='gray')

    return device, finalcorrected
