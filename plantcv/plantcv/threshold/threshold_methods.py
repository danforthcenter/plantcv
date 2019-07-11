# Threshold functions

import os
import cv2
import math
import numpy as np
from matplotlib import pyplot as plt
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from skimage.feature import greycomatrix, greycoprops
from scipy.ndimage import generic_filter

# Binary threshold
def binary(gray_img, threshold, max_value, object_type="light"):
    """Creates a binary image from a grayscale image based on the threshold value.

    Inputs:
    gray_img     = Grayscale image data
    threshold    = Threshold value (0-255)
    max_value    = value to apply above threshold (usually 255 = white)
    object_type  = "light" or "dark" (default: "light")
                   - If object is lighter than the background then standard thresholding is done
                   - If object is darker than the background then inverse thresholding is done

    Returns:
    bin_img      = Thresholded, binary image

    :param gray_img: numpy.ndarray
    :param threshold: int
    :param max_value: int
    :param object_type: str
    :return bin_img: numpy.ndarray
    """
    params.device += 1

    # Set the threshold method
    threshold_method = ""
    if object_type.upper() == "LIGHT":
        threshold_method = cv2.THRESH_BINARY
    elif object_type.upper() == "DARK":
        threshold_method = cv2.THRESH_BINARY_INV
    else:
        fatal_error('Object type ' + str(object_type) + ' is not "light" or "dark"!')

    # Threshold the image
    bin_img = _call_threshold(gray_img, threshold, max_value, threshold_method, "_binary_threshold_")

    return bin_img


# Gaussian adaptive threshold
def gaussian(gray_img, max_value, object_type="light"):
    """Creates a binary image from a grayscale image based on the Gaussian adaptive threshold method.

    Inputs:
    gray_img     = Grayscale image data
    max_value    = value to apply above threshold (usually 255 = white)
    object_type  = "light" or "dark" (default: "light")
                   - If object is lighter than the background then standard thresholding is done
                   - If object is darker than the background then inverse thresholding is done

    Returns:
    bin_img      = Thresholded, binary image

    :param gray_img: numpy.ndarray
    :param max_value: int
    :param object_type: str
    :return bin_img: numpy.ndarray
    """
    params.device += 1

    # Set the threshold method
    threshold_method = ""
    if object_type.upper() == "LIGHT":
        threshold_method = cv2.THRESH_BINARY
    elif object_type.upper() == "DARK":
        threshold_method = cv2.THRESH_BINARY_INV
    else:
        fatal_error('Object type ' + str(object_type) + ' is not "light" or "dark"!')

    bin_img = _call_adaptive_threshold(gray_img, max_value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, threshold_method,
                                       "_gaussian_threshold_")

    return bin_img


# Mean adaptive threshold
def mean(gray_img, max_value, object_type="light"):
    """Creates a binary image from a grayscale image based on the mean adaptive threshold method.

    Inputs:
    gray_img     = Grayscale image data
    max_value    = value to apply above threshold (usually 255 = white)
    object_type  = "light" or "dark" (default: "light")
                   - If object is lighter than the background then standard thresholding is done
                   - If object is darker than the background then inverse thresholding is done

    Returns:
    bin_img      = Thresholded, binary image

    :param gray_img: numpy.ndarray
    :param max_value: int
    :param object_type: str
    :return bin_img: numpy.ndarray
    """
    params.device += 1

    # Set the threshold method
    threshold_method = ""
    if object_type.upper() == "LIGHT":
        threshold_method = cv2.THRESH_BINARY
    elif object_type.upper() == "DARK":
        threshold_method = cv2.THRESH_BINARY_INV
    else:
        fatal_error('Object type ' + str(object_type) + ' is not "light" or "dark"!')

    bin_img = _call_adaptive_threshold(gray_img, max_value, cv2.ADAPTIVE_THRESH_MEAN_C, threshold_method,
                                       "_mean_threshold_")

    return bin_img


# Otsu autothreshold
def otsu(gray_img, max_value, object_type="light"):
    """Creates a binary image from a grayscale image using Otsu's thresholding.

    Inputs:
    gray_img     = Grayscale image data
    max_value    = value to apply above threshold (usually 255 = white)
    object_type  = "light" or "dark" (default: "light")
                   - If object is lighter than the background then standard thresholding is done
                   - If object is darker than the background then inverse thresholding is done

    Returns:
    bin_img      = Thresholded, binary image

    :param gray_img: numpy.ndarray
    :param max_value: int
    :param object_type: str
    :return bin_img: numpy.ndarray
    """
    params.device += 1

    # Set the threshold method
    threshold_method = ""
    if object_type.upper() == "LIGHT":
        threshold_method = cv2.THRESH_BINARY + cv2.THRESH_OTSU
    elif object_type.upper() == "DARK":
        threshold_method = cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    else:
        fatal_error('Object type ' + str(object_type) + ' is not "light" or "dark"!')

    # Threshold the image
    bin_img = _call_threshold(gray_img, 0, max_value, threshold_method, "_otsu_threshold_")

    return bin_img


# Triangle autothreshold
def triangle(gray_img, max_value, object_type="light", xstep=1):
    """Creates a binary image from a grayscale image using Zack et al.'s (1977) thresholding.

    Inputs:
    gray_img     = Grayscale image data
    max_value    = value to apply above threshold (usually 255 = white)
    object_type  = "light" or "dark" (default: "light")
                   - If object is lighter than the background then standard thresholding is done
                   - If object is darker than the background then inverse thresholding is done
    xstep        = value to move along x-axis to determine the points from which to calculate distance recommended to
                   start at 1 and change if needed)

    Returns:
    bin_img      = Thresholded, binary image

    :param gray_img: numpy.ndarray
    :param max_value: int
    :param object_type: str
    :param xstep: int
    :return bin_img: numpy.ndarray
    """
    params.device += 1

    # Calculate automatic threshold value based on triangle algorithm
    hist = cv2.calcHist([gray_img], [0], None, [256], [0, 255])

    # Make histogram one array
    newhist = []
    for item in hist:
        newhist.extend(item)

    # Detect peaks
    show = False
    if params.debug == "plot":
        show = True
    ind = _detect_peaks(newhist, mph=None, mpd=1, show=show)

    # Find point corresponding to highest peak
    # Find intensity value (y) of highest peak
    max_peak_int = max(list(newhist[i] for i in ind))
    # Find value (x) of highest peak
    max_peak = [i for i, x in enumerate(newhist) if x == max(newhist)]
    # Combine x,y
    max_peak_xy = [max_peak[0], max_peak_int]

    # Find final point at end of long tail
    end_x = len(newhist) - 1
    end_y = newhist[end_x]
    end_xy = [end_x, end_y]

    # Define the known points
    points = [max_peak_xy, end_xy]
    x_coords, y_coords = zip(*points)

    # Get threshold value
    peaks = []
    dists = []

    for i in range(x_coords[0], x_coords[1], xstep):
        distance = (((x_coords[1] - x_coords[0]) * (y_coords[0] - hist[i])) -
                    ((x_coords[0] - i) * (y_coords[1] - y_coords[0]))) / math.sqrt(
            (float(x_coords[1]) - float(x_coords[0])) *
            (float(x_coords[1]) - float(x_coords[0])) +
            ((float(y_coords[1]) - float(y_coords[0])) *
             (float(y_coords[1]) - float(y_coords[0]))))
        peaks.append(i)
        dists.append(distance)
    autothresh = [peaks[x] for x in [i for i, x in enumerate(list(dists)) if x == max(list(dists))]]
    autothreshval = autothresh[0]

    # Set the threshold method
    threshold_method = ""
    if object_type.upper() == "LIGHT":
        threshold_method = cv2.THRESH_BINARY + cv2.THRESH_OTSU
    elif object_type.upper() == "DARK":
        threshold_method = cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    else:
        fatal_error('Object type ' + str(object_type) + ' is not "light" or "dark"!')

    # Threshold the image
    bin_img = _call_threshold(gray_img, autothreshval, max_value, threshold_method, "_triangle_threshold_")

    # Additional figures created by this method, if debug is on
    if params.debug is not None:
        if params.debug == 'print':
            plt.plot(hist)
            plt.title('Threshold value = {t}'.format(t=autothreshval))
            plt.axis([0, 256, 0, max(hist)])
            plt.grid(True)
            fig_name_hist = os.path.join(params.debug_outdir,
                                         str(params.device) + '_triangle_thresh_hist_' + str(autothreshval) + ".png")
            # write the figure to current directory
            plt.savefig(fig_name_hist, dpi=params.dpi)
            # close pyplot plotting window
            plt.clf()
        elif params.debug == 'plot':
            print('Threshold value = {t}'.format(t=autothreshval))
            plt.plot(hist)
            plt.axis([0, 256, 0, max(hist)])
            plt.grid(True)
            plt.show()

    return bin_img


def texture(gray_img, ksize, threshold, offset=3, texture_method='dissimilarity', borders='nearest',
            max_value=255):
    """Creates a binary image from a grayscale image using skimage texture calculation for thresholding.
    This function is quite slow.

    Inputs:
    gray_img       = Grayscale image data
    ksize          = Kernel size for texture measure calculation
    threshold      = Threshold value (0-255)
    offset         = Distance offsets
    texture_method = Feature of a grey level co-occurrence matrix, either
                     'contrast', 'dissimilarity', 'homogeneity', 'ASM', 'energy',
                     or 'correlation'.For equations of different features see
                     scikit-image.
    borders        = How the array borders are handled, either 'reflect',
                     'constant', 'nearest', 'mirror', or 'wrap'
    max_value      = Value to apply above threshold (usually 255 = white)

    Returns:
    bin_img        = Thresholded, binary image

    :param gray_img: numpy.ndarray
    :param ksize: int
    :param threshold: int
    :param offset: int
    :param texture_method: str
    :param borders: str
    :param max_value: int
    :return bin_img: numpy.ndarray
    """

    # Function that calculates the texture of a kernel
    def calc_texture(inputs):
        inputs = np.reshape(a=inputs, newshape=[ksize, ksize])
        inputs = inputs.astype(np.uint8)
        # Greycomatrix takes image, distance offset, angles (in radians), symmetric, and normed
        # http://scikit-image.org/docs/dev/api/skimage.feature.html#skimage.feature.greycomatrix
        glcm = greycomatrix(inputs, [offset], [0], 256, symmetric=True, normed=True)
        diss = greycoprops(glcm, texture_method)[0, 0]
        return diss

    # Make an array the same size as the original image
    output = np.zeros(gray_img.shape, dtype=gray_img.dtype)

    # Apply the texture function over the whole image
    generic_filter(gray_img, calc_texture, size=ksize, output=output, mode=borders)

    # Threshold so higher texture measurements stand out
    bin_img = binary(gray_img=output, threshold=threshold, max_value=max_value, object_type='light')
    return bin_img


def custom_range(rgb_img, lower_thresh, upper_thresh, channel='gray'):
    """Creates a thresholded image and mask from an RGB image and threshold values.

    Inputs:
    rgb_img      = RGB image data
    lower_thresh = List of lower threshold values (0-255)
    upper_thresh = List of upper threshold values (0-255)
    channel      = Color-space channels of interest (RGB, HSV, LAB, or gray)

    Returns:
    mask         = Mask, binary image
    masked_img   = Masked image, keeping the part of image of interest

    :param rgb_img: numpy.ndarray
    :param lower_thresh: list
    :param upper_thresh: list
    :param channel: str
    :return mask: numpy.ndarray
    :return masked_img: numpy.ndarray
    """

    # Auto-increment the device counter
    params.device += 1

    if channel.upper() == 'HSV':

        # Check threshold inputs
        if not (len(lower_thresh) == 3 and len(upper_thresh) == 3):
            fatal_error("If using the HSV colorspace, 3 thresholds are needed for both lower_thresh and " +
                        "upper_thresh. If thresholding isn't needed for a channel, set lower_thresh=0 and " +
                        "upper_thresh=255")

        # Convert the RGB image to HSV colorspace
        hsv_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2HSV)

        # Separate channels
        hue = hsv_img[:, :, 0]
        saturation = hsv_img[:, :, 1]
        value = hsv_img[:, :, 2]

        # Make a mask for each channel
        h_mask = cv2.inRange(hue, lower_thresh[0], upper_thresh[0])
        s_mask = cv2.inRange(saturation, lower_thresh[1], upper_thresh[1])
        v_mask = cv2.inRange(value, lower_thresh[2], upper_thresh[2])

        # Apply the masks to the image
        result = cv2.bitwise_and(rgb_img, rgb_img, mask=h_mask)
        result = cv2.bitwise_and(result, result, mask=s_mask)
        masked_img = cv2.bitwise_and(result, result, mask=v_mask)

        # Combine masks
        mask = cv2.bitwise_and(s_mask, h_mask)
        mask = cv2.bitwise_and(mask, v_mask)

    elif channel.upper() == 'RGB':

        # Check threshold inputs
        if not (len(lower_thresh) == 3 and len(upper_thresh) == 3):
            fatal_error("If using the RGB colorspace, 3 thresholds are needed for both lower_thresh and " +
                        "upper_thresh. If thresholding isn't needed for a channel, set lower_thresh=0 and " +
                        "upper_thresh=255")

        # Separate channels (pcv.readimage reads RGB images in as BGR)
        blue = rgb_img[:, :, 0]
        green = rgb_img[:, :, 1]
        red = rgb_img[:, :, 2]

        # Make a mask for each channel
        b_mask = cv2.inRange(blue, lower_thresh[0], upper_thresh[0])
        g_mask = cv2.inRange(green, lower_thresh[1], upper_thresh[1])
        r_mask = cv2.inRange(red, lower_thresh[2], upper_thresh[2])

        # Apply the masks to the image
        result = cv2.bitwise_and(rgb_img, rgb_img, mask=b_mask)
        result = cv2.bitwise_and(result, result, mask=g_mask)
        masked_img = cv2.bitwise_and(result, result, mask=r_mask)

        # Combine masks
        mask = cv2.bitwise_and(b_mask, g_mask)
        mask = cv2.bitwise_and(mask, r_mask)

    elif channel.upper() == 'LAB':

        # Check threshold inputs
        if not (len(lower_thresh) == 3 and len(upper_thresh) == 3):
            fatal_error("If using the LAB colorspace, 3 thresholds are needed for both lower_thresh and " +
                        "upper_thresh. If thresholding isn't needed for a channel, set lower_thresh=0 and " +
                        "upper_thresh=255")

        # Convert the RGB image to LAB colorspace
        lab_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2LAB)

        # Separate channels (pcv.readimage reads RGB images in as BGR)
        lightness = lab_img[:, :, 0]
        green_magenta = lab_img[:, :, 1]
        blue_yellow = lab_img[:, :, 2]

        # Make a mask for each channel
        l_mask = cv2.inRange(lightness, lower_thresh[0], upper_thresh[0])
        gm_mask = cv2.inRange(green_magenta, lower_thresh[1], upper_thresh[1])
        by_mask = cv2.inRange(blue_yellow, lower_thresh[2], upper_thresh[2])

        # Apply the masks to the image
        result = cv2.bitwise_and(rgb_img, rgb_img, mask=l_mask)
        result = cv2.bitwise_and(result, result, mask=gm_mask)
        masked_img = cv2.bitwise_and(result, result, mask=by_mask)

        # Combine masks
        mask = cv2.bitwise_and(l_mask, gm_mask)
        mask = cv2.bitwise_and(mask, by_mask)

    elif channel.upper() == 'GRAY' or channel.upper() == 'GREY':

        # Check threshold input
        if not (len(lower_thresh) == 1 and len(upper_thresh) == 1):
            fatal_error("If useing a grayscale colorspace, 1 threshold is needed for both the " +
                        "lower_thresh and upper_thresh.")
        if len(np.shape(rgb_img))==3:
            # Convert RGB image to grayscale colorspace
            gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
        else:
            gray_img = rgb_img

        # Make a mask
        mask = cv2.inRange(gray_img, lower_thresh[0], upper_thresh[0])

        # Apply the masks to the image
        masked_img = cv2.bitwise_and(rgb_img, rgb_img, mask=mask)

    else:
        fatal_error(str(channel) + " is not a valid colorspace. Channel must be either 'RGB', 'HSV', or 'gray'.")

    # Print or plot the binary image if debug is on
    if params.debug == 'print':
        print_image(masked_img, os.path.join(params.debug_outdir,
                                             str(params.device) + channel + 'custom_thresh.png'))
        print_image(mask, os.path.join(params.debug_outdir,
                                       str(params.device) + channel + 'custom_thresh_mask.png'))
    elif params.debug == 'plot':
        plot_image(masked_img)
        plot_image(mask)

    return mask, masked_img


# Internal method for calling the OpenCV threshold function to reduce code duplication
def _call_threshold(gray_img, threshold, max_value, threshold_method, method_name):
    # Threshold the image
    ret, bin_img = cv2.threshold(gray_img, threshold, max_value, threshold_method)

    if bin_img.dtype != 'uint16':
        bin_img = np.uint8(bin_img)

    # Print or plot the binary image if debug is on
    if params.debug == 'print':
        print_image(bin_img, os.path.join(params.debug_outdir,
                                          str(params.device) + method_name + str(threshold) + '.png'))
    elif params.debug == 'plot':
        plot_image(bin_img, cmap='gray')

    return bin_img


# Internal method for calling the OpenCV adaptiveThreshold function to reduce code duplication
def _call_adaptive_threshold(gray_img, max_value, adaptive_method, threshold_method, method_name):
    # Threshold the image
    bin_img = cv2.adaptiveThreshold(gray_img, max_value, adaptive_method, threshold_method, 11, 2)

    # Print or plot the binary image if debug is on
    if params.debug == 'print':
        print_image(bin_img, os.path.join(params.debug_outdir,
                                          str(params.device) + method_name + '.png'))
    elif params.debug == 'plot':
        plot_image(bin_img, cmap='gray')

    return bin_img


# Internal method for detecting peaks for the triangle autothreshold method
def _detect_peaks(x, mph=None, mpd=1, threshold=0, edge='rising', kpsh=False, valley=False, show=False, ax=None):
    """Marcos Duarte, https://github.com/demotu/BMC; version 1.0.4; license MIT

    Detect peaks in data based on their amplitude and other features.

    Parameters
    ----------
    x : 1D array_like
        data.
    mph : {None, number}, optional (default = None)
        detect peaks that are greater than minimum peak height.
    mpd : positive integer, optional (default = 1)
        detect peaks that are at least separated by minimum peak distance (in
        number of data).
    threshold : positive number, optional (default = 0)
        detect peaks (valleys) that are greater (smaller) than `threshold`
        in relation to their immediate neighbors.
    edge : {None, 'rising', 'falling', 'both'}, optional (default = 'rising')
        for a flat peak, keep only the rising edge ('rising'), only the
        falling edge ('falling'), both edges ('both'), or don't detect a
        flat peak (None).
    kpsh : bool, optional (default = False)
        keep peaks with same height even if they are closer than `mpd`.
    valley : bool, optional (default = False)
        if True (1), detect valleys (local minima) instead of peaks.
    show : bool, optional (default = False)
        if True (1), plot data in matplotlib figure.
    ax : a matplotlib.axes.Axes instance, optional (default = None).

    Returns
    -------
    ind : 1D array_like
        indices of the peaks in `x`.

    Notes
    -----
    The detection of valleys instead of peaks is performed internally by simply
    negating the data: `ind_valleys = detect_peaks(-x)`

    The function can handle NaN's

    See this IPython Notebook [1]_.

    References
    ----------
    .. [1] http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/DetectPeaks.ipynb

    Examples
    --------
    from detect_peaks import detect_peaks
    x = np.random.randn(100)
    x[60:81] = np.nan
    # detect all peaks and plot data
    ind = detect_peaks(x, show=True)
    print(ind)

    x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + np.random.randn(200)/5
    # set minimum peak height = 0 and minimum peak distance = 20
    detect_peaks(x, mph=0, mpd=20, show=True)

    x = [0, 1, 0, 2, 0, 3, 0, 2, 0, 1, 0]
    # set minimum peak distance = 2
    detect_peaks(x, mpd=2, show=True)

    x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + np.random.randn(200)/5
    # detection of valleys instead of peaks
    detect_peaks(x, mph=0, mpd=20, valley=True, show=True)

    x = [0, 1, 1, 0, 1, 1, 0]
    # detect both edges
    detect_peaks(x, edge='both', show=True)

    x = [-2, 1, -2, 2, 1, 1, 3, 0]
    # set threshold = 2
    detect_peaks(x, threshold = 2, show=True)
    """

    x = np.atleast_1d(x).astype('float64')

    # It is always the case that x.size=256 since 256 hardcoded in line 186 -> cv2.calcHist([gray_img], [0], None, [256], [0, 255])
    # if x.size < 3:
    #     return np.array([], dtype=int)

    # # Where this function is used it is hardcoded to use the default valley=False so this will never be used
    # if valley:
    #     x = -x
    # find indices of all peaks
    dx = x[1:] - x[:-1]
    # handle NaN's
    indnan = np.where(np.isnan(x))[0]

    # x will never contain NaN since calcHist will never return NaN
    # if indnan.size:
    #     x[indnan] = np.inf
    #     dx[np.where(np.isnan(dx))[0]] = np.inf
    ine, ire, ife = np.array([[], [], []], dtype=int)
    # # Where this function is used it is hardcoded to use the default edge='rising' so we will never have
    # # edge=None, thus this will never be used
    # if not edge:
    #     ine = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) > 0))[0]

    if edge.lower() in ['rising', 'both']:
        ire = np.where((np.hstack((dx, 0)) <= 0) & (np.hstack((0, dx)) > 0))[0]
        # # Where this function is used it is hardcoded to use the default edge='rising' so this will never be used
        # if edge.lower() in ['falling', 'both']:
        #     ife = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) >= 0))[0]
    ind = np.unique(np.hstack((ine, ire, ife)))
    # x will never contain NaN since calcHist will never return NaN
    # if ind.size and indnan.size:
    #     # NaN's and values close to NaN's cannot be peaks
    #     ind = ind[np.in1d(ind, np.unique(np.hstack((indnan, indnan - 1, indnan + 1))), invert=True)]
    # first and last values of x cannot be peaks
    if ind.size and ind[0] == 0:
        ind = ind[1:]
    if ind.size and ind[-1] == x.size - 1:
        ind = ind[:-1]

    # # Where this function is used has hardcoded mph=None so this will never be used
    # # remove peaks < minimum peak height
    # if ind.size and mph is not None:
    #     ind = ind[x[ind] >= mph]
    # remove peaks - neighbors < threshold

    # # Where this function is used threshold is hardcoded to the default threshold=0 so this will never be used
    # if ind.size and threshold > 0:
    #     dx = np.min(np.vstack([x[ind] - x[ind - 1], x[ind] - x[ind + 1]]), axis=0)
    #     ind = np.delete(ind, np.where(dx < threshold)[0])

    # # Where this function is used has hardcoded mpd=1 so this will never be used
    # # detect small peaks closer than minimum peak distance
    # if ind.size and mpd > 1:
    #     ind = ind[np.argsort(x[ind])][::-1]  # sort ind by peak height
    #     idel = np.zeros(ind.size, dtype=bool)
    #     for i in range(ind.size):
    #         if not idel[i]:
    #             # keep peaks with the same height if kpsh is True
    #             idel = idel | (ind >= ind[i] - mpd) & (ind <= ind[i] + mpd) \
    #                           & (x[ind[i]] > x[ind] if kpsh else True)
    #             idel[i] = 0  # Keep current peak
    #     # remove the small peaks and sort back the indices by their occurrence
    #     ind = np.sort(ind[~idel])

    if show:
        # x will never contain NaN since calcHist will never return NaN
        # if indnan.size:
        #     x[indnan] = np.nan
        # # Where this function is used it is hardcoded to use the default valley=False so this will never be used
        # if valley:
        #     x = -x
        _plot(x, mph, mpd, threshold, edge, valley, ax, ind)

    return ind


# Internal plotting function for the triangle autothreshold method
def _plot(x, mph, mpd, threshold, edge, valley, ax, ind):
    """Plot results of the detect_peaks function, see its help."""
    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=(8, 4))

    ax.plot(x, 'b', lw=1)
    if ind.size:
        label = 'valley' if valley else 'peak'
        label = label + 's' if ind.size > 1 else label
        ax.plot(ind, x[ind], '+', mfc=None, mec='r', mew=2, ms=8,
                label='%d %s' % (ind.size, label))
        ax.legend(loc='best', framealpha=.5, numpoints=1)
    ax.set_xlim(-.02 * x.size, x.size * 1.02 - 1)
    ymin, ymax = x[np.isfinite(x)].min(), x[np.isfinite(x)].max()
    yrange = ymax - ymin if ymax > ymin else 1
    ax.set_ylim(ymin - 0.1 * yrange, ymax + 0.1 * yrange)
    ax.set_xlabel('Data #', fontsize=14)
    ax.set_ylabel('Amplitude', fontsize=14)
    mode = 'Valley detection' if valley else 'Peak detection'
    ax.set_title("%s (mph=%s, mpd=%d, threshold=%s, edge='%s')"
                 % (mode, str(mph), mpd, str(threshold), edge))
    # plt.grid()
    plt.show()
