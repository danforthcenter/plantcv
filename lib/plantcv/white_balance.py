import cv2
import numpy as np
import plantcv as pcv


def white_balance(device,img, roi=None, debug=None):

    """Corrects the exposure of an image based on its histogram.
    Inputs:
    img - A grayscale image on which to perform the correction
    roi - A list of 4 points (x, y, width, height) that form the rectangular ROI of the white color standard.
            If a list of 4 points is not given, whole image will be used.

    Returns:
    img - Image after exposure correction
    """
    # Finds histogram of roi if valid roi is given. Otherwise, finds histogram of entire image
    if roi is not None and len(roi) == 4:
        hist = cv2.calcHist(tuple(img[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]), [0], None, [256], [0, 256])
    else:
        hist = cv2.calcHist(tuple(img), [0], None, [256], [0, 256])  # Creates histogram of original image

    # Calculates index of maximum of histogram and finds alpha based on the peak
    hmax = np.argmax(hist)
    alpha = 255 / float(hmax)
    
    if debug == 'print':
        print_image(ori_img, (str(device) + '_roi.png'))
    elif debug == 'plot':
        if len(np.shape(img)) == 3:
            ix, iy, iz = np.shape(img)
            plot_image(ori_img)
        else:
            ix, iy = np.shape(img)
            plot_image(ori_img,cmap='gray')

    # Converts values greater than hmax to 255 and scales all others by alpha
    img = np.asarray(np.where(img <= hmax, np.multiply(alpha, img), 255), np.uint8)
    return device,img
