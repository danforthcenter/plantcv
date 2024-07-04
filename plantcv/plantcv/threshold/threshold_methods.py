"""Threshold functions."""
import os
import cv2
import math
import numpy as np
from matplotlib import pyplot as plt
from plantcv.plantcv import rgb2gray
from plantcv.plantcv import rgb2gray_hsv
from plantcv.plantcv import rgb2gray_lab
from plantcv.plantcv import fatal_error, warn
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from skimage.feature import graycomatrix, graycoprops
from scipy.ndimage import generic_filter


# Binary threshold
def binary(gray_img, threshold, object_type="light"):
    """Creates a binary image from a grayscale image based on the threshold value.

    Inputs:
    gray_img     = Grayscale image data
    threshold    = Threshold value (0-255)
    object_type  = "light" or "dark" (default: "light")
                   - If object is lighter than the background then standard thresholding is done
                   - If object is darker than the background then inverse thresholding is done

    Returns:
    bin_img      = Thresholded, binary image

    :param gray_img: numpy.ndarray
    :param threshold: int
    :param object_type: str
    :return bin_img: numpy.ndarray
    """
    # Set the threshold method
    threshold_method = ""
    if object_type.upper() == "LIGHT":
        threshold_method = cv2.THRESH_BINARY
    elif object_type.upper() == "DARK":
        threshold_method = cv2.THRESH_BINARY_INV
    else:
        fatal_error('Object type ' + str(object_type) + ' is not "light" or "dark"!')

    params.device += 1

    # Threshold the image
    bin_img = _call_threshold(gray_img, threshold, threshold_method, "_binary_threshold_")

    return bin_img


# Gaussian adaptive threshold
def gaussian(gray_img, ksize, offset, object_type="light"):
    """Creates a binary image from a grayscale image based on the Gaussian adaptive threshold method.

    Adaptive thresholds use a threshold value that varies across the image.
    This local threshold depends on the local average, computed in a squared portion of the image of
    ksize by ksize pixels, and on the offset relative to that local average.

    In the Gaussian adaptive threshold, the local average is a weighed average of the pixel values
    in the block, where the weights are a 2D Gaussian centered in the middle.

    Inputs:
    gray_img     = Grayscale image data
    ksize        = Size of the block of pixels used to compute the local average
    offset       = Value substracted from the local average to compute the local threshold.
                    A negative offset sets the local threshold above the local average.
    object_type  = "light" or "dark" (default: "light")
                   - "light" (for objects brighter than the background) sets the pixels above
                        the local threshold to 255 and the pixels below to 0.
                   - "dark" (for objects darker than the background) sets the pixels below the
                        local threshold to 255 and the pixels above to 0.

    Returns:
    bin_img      = Thresholded, binary image

    :param gray_img: numpy.ndarray
    :param ksize: int
    :param offset: float
    :param object_type: str
    :return bin_img: numpy.ndarray
    """
    # Set the threshold method
    threshold_method = ""
    if object_type.upper() == "LIGHT":
        threshold_method = cv2.THRESH_BINARY
    elif object_type.upper() == "DARK":
        threshold_method = cv2.THRESH_BINARY_INV
    else:
        fatal_error('Object type ' + str(object_type) + ' is not "light" or "dark"!')

    params.device += 1

    bin_img = _call_adaptive_threshold(gray_img, ksize, offset, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       threshold_method, "_gaussian_threshold_")

    return bin_img


# Mean adaptive threshold
def mean(gray_img, ksize, offset, object_type="light"):
    """Creates a binary image from a grayscale image based on the mean adaptive threshold method.

    Adaptive thresholds use a threshold value that varies across the image.
    This local threshold depends on the local average, computed in a squared portion of the image of
    ksize by ksize pixels, and on the offset relative to that local average.

    In the mean adaptive threshold, the local average is the average of the pixel values in the block.

    Inputs:
    gray_img     = Grayscale image data
    ksize        = Size of the block of pixels used to compute the local average
    offset       = Value substracted from the local average to compute the local threshold.
                    A negative offset sets the local threshold above the local average.
    object_type  = "light" or "dark" (default: "light")
                   - "light" (for objects brighter than the background) sets the pixels above
                        the local threshold to 255 and the pixels below to 0.
                   - "dark" (for objects darker than the background) sets the pixels below the
                        local threshold to 255 and the pixels above to 0.

    Returns:
    bin_img      = Thresholded, binary image

    :param gray_img: numpy.ndarray
    :param ksize: int
    :param offset: float
    :param object_type: str
    :return bin_img: numpy.ndarray
    """
    # Set the threshold method
    threshold_method = ""
    if object_type.upper() == "LIGHT":
        threshold_method = cv2.THRESH_BINARY
    elif object_type.upper() == "DARK":
        threshold_method = cv2.THRESH_BINARY_INV
    else:
        fatal_error('Object type ' + str(object_type) + ' is not "light" or "dark"!')

    params.device += 1

    bin_img = _call_adaptive_threshold(gray_img, ksize, offset, cv2.ADAPTIVE_THRESH_MEAN_C,
                                       threshold_method, "_mean_threshold_")

    return bin_img


# Otsu autothreshold
def otsu(gray_img, object_type="light"):
    """Creates a binary image from a grayscale image using Otsu's thresholding.

    Inputs:
    gray_img     = Grayscale image data
    object_type  = "light" or "dark" (default: "light")
                   - If object is lighter than the background then standard thresholding is done
                   - If object is darker than the background then inverse thresholding is done

    Returns:
    bin_img      = Thresholded, binary image

    :param gray_img: numpy.ndarray
    :param object_type: str
    :return bin_img: numpy.ndarray
    """
    # Set the threshold method
    threshold_method = ""
    if object_type.upper() == "LIGHT":
        threshold_method = cv2.THRESH_BINARY + cv2.THRESH_OTSU
    elif object_type.upper() == "DARK":
        threshold_method = cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    else:
        fatal_error('Object type ' + str(object_type) + ' is not "light" or "dark"!')

    params.device += 1

    # Threshold the image
    bin_img = _call_threshold(gray_img, 0, threshold_method, "_otsu_threshold_")

    return bin_img


# Triangle autothreshold
def triangle(gray_img, object_type="light", xstep=1):
    """Creates a binary image from a grayscale image using Zack et al.'s (1977) thresholding.

    Inputs:
    gray_img     = Grayscale image data
    object_type  = "light" or "dark" (default: "light")
                   - If object is lighter than the background then standard thresholding is done
                   - If object is darker than the background then inverse thresholding is done
    xstep        = value to move along x-axis to determine the points from which to calculate distance recommended to
                   start at 1 and change if needed)

    Returns:
    bin_img      = Thresholded, binary image

    :param gray_img: numpy.ndarray
    :param object_type: str
    :param xstep: int
    :return bin_img: numpy.ndarray
    """
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
    max_peak_int = max(newhist[i] for i in ind)
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

    params.device += 1

    # Threshold the image
    bin_img = _call_threshold(gray_img, autothreshval, threshold_method, "_triangle_threshold_")

    # Additional figures created by this method, if debug is on
    if params.debug is not None:
        if params.debug == 'print':
            _, ax = plt.subplots()
            ax.plot(hist)
            ax.set(title=f"Threshold value = {autothreshval}")
            ax.axis([0, 256, 0, max(hist)])
            ax.grid(True)
            fig_name_hist = os.path.join(params.debug_outdir,
                                         str(params.device) + '_triangle_thresh_hist_' + str(autothreshval) + ".png")
            # write the figure to current directory
            plt.savefig(fig_name_hist, dpi=params.dpi)
            # close pyplot plotting window
            plt.clf()
        elif params.debug == 'plot':
            print(f"Threshold value = {autothreshval}")
            _, ax = plt.subplots()
            ax.plot(hist)
            ax.axis([0, 256, 0, max(hist)])
            ax.grid(True)
            plt.show()

    return bin_img


def texture(gray_img, ksize, threshold, offset=3, texture_method='dissimilarity', borders='nearest'):
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

    Returns:
    bin_img        = Thresholded, binary image

    :param gray_img: numpy.ndarray
    :param ksize: int
    :param threshold: int
    :param offset: int
    :param texture_method: str
    :param borders: str
    :return bin_img: numpy.ndarray
    """
    # Function that calculates the texture of a kernel
    def calc_texture(inputs):
        """Kernel calculate texture function.

        Parameters
        ----------
        inputs : numpy.ndarray
            Input pixel array

        Returns
        -------
        float
            Texture value
        """
        inputs = np.reshape(a=inputs, newshape=[ksize, ksize])
        inputs = inputs.astype(np.uint8)
        # Greycomatrix takes image, distance offset, angles (in radians), symmetric, and normed
        # http://scikit-image.org/docs/dev/api/skimage.feature.html#skimage.feature.graycomatrix
        glcm = graycomatrix(inputs, [offset], [0], 256, symmetric=True, normed=True)
        diss = graycoprops(glcm, texture_method)[0, 0]
        return diss

    # Make an array the same size as the original image
    output = np.zeros(gray_img.shape, dtype=gray_img.dtype)

    # Apply the texture function over the whole image
    generic_filter(gray_img, calc_texture, size=ksize, output=output, mode=borders)

    # Threshold so higher texture measurements stand out
    bin_img = binary(gray_img=output, threshold=threshold, object_type='light')

    _debug(visual=bin_img, filename=os.path.join(params.debug_outdir, str(params.device) + "_texture_mask.png"))

    return bin_img


def custom_range(img, lower_thresh, upper_thresh, channel='gray'):
    """Creates a thresholded image and mask from an RGB image and threshold values.

    Inputs:
    img      = RGB or grayscale image data
    lower_thresh = List of lower threshold values (0-255)
    upper_thresh = List of upper threshold values (0-255)
    channel      = Color-space channels of interest (RGB, HSV, LAB, or gray)

    Returns:
    mask         = Mask, binary image
    masked_img   = Masked image, keeping the part of image of interest

    :param img: numpy.ndarray
    :param lower_thresh: list
    :param upper_thresh: list
    :param channel: str
    :return mask: numpy.ndarray
    :return masked_img: numpy.ndarray
    """
    if channel.upper() == 'HSV':

        # Check threshold inputs
        if not (len(lower_thresh) == 3 and len(upper_thresh) == 3):
            fatal_error("If using the HSV colorspace, 3 thresholds are needed for both lower_thresh and " +
                        "upper_thresh. If thresholding isn't needed for a channel, set lower_thresh=0 and " +
                        "upper_thresh=255")

        # Convert the RGB image to HSV colorspace
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Separate channels
        hue = hsv_img[:, :, 0]
        sat = hsv_img[:, :, 1]
        value = hsv_img[:, :, 2]

        # Make a mask for each channel
        h_mask = cv2.inRange(hue, lower_thresh[0], upper_thresh[0])
        s_mask = cv2.inRange(sat, lower_thresh[1], upper_thresh[1])
        v_mask = cv2.inRange(value, lower_thresh[2], upper_thresh[2])

        # Apply the masks to the image
        result = cv2.bitwise_and(img, img, mask=h_mask)
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
        blue = img[:, :, 0]
        green = img[:, :, 1]
        red = img[:, :, 2]

        # Make a mask for each channel
        b_mask = cv2.inRange(blue, lower_thresh[2], upper_thresh[2])
        g_mask = cv2.inRange(green, lower_thresh[1], upper_thresh[1])
        r_mask = cv2.inRange(red, lower_thresh[0], upper_thresh[0])

        # Apply the masks to the image
        result = cv2.bitwise_and(img, img, mask=b_mask)
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
        lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

        # Separate channels (pcv.readimage reads RGB images in as BGR)
        lightness = lab_img[:, :, 0]
        green_magenta = lab_img[:, :, 1]
        blue_yellow = lab_img[:, :, 2]

        # Make a mask for each channel
        l_mask = cv2.inRange(lightness, lower_thresh[0], upper_thresh[0])
        gm_mask = cv2.inRange(green_magenta, lower_thresh[1], upper_thresh[1])
        by_mask = cv2.inRange(blue_yellow, lower_thresh[2], upper_thresh[2])

        # Apply the masks to the image
        result = cv2.bitwise_and(img, img, mask=l_mask)
        result = cv2.bitwise_and(result, result, mask=gm_mask)
        masked_img = cv2.bitwise_and(result, result, mask=by_mask)

        # Combine masks
        mask = cv2.bitwise_and(l_mask, gm_mask)
        mask = cv2.bitwise_and(mask, by_mask)

    elif channel.upper() in ('GRAY', 'GREY'):

        # Check threshold input
        if not (len(lower_thresh) == 1 and len(upper_thresh) == 1):
            fatal_error("If useing a grayscale colorspace, 1 threshold is needed for both the " +
                        "lower_thresh and upper_thresh.")
        if len(np.shape(img)) == 3:
            # Convert RGB image to grayscale colorspace
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray_img = img

        # Make a mask
        mask = cv2.inRange(gray_img, lower_thresh[0], upper_thresh[0])

        # Apply the masks to the image
        masked_img = cv2.bitwise_and(img, img, mask=mask)

    else:
        fatal_error(str(channel) + " is not a valid colorspace. Channel must be either 'RGB', 'HSV', or 'gray'.")

    # Auto-increment the device counter

    # Print or plot the binary image if debug is on
    _debug(visual=masked_img, filename=os.path.join(params.debug_outdir,
                                                    str(params.device) + channel + 'custom_thresh.png'))
    _debug(visual=mask, filename=os.path.join(params.debug_outdir,
                                              str(params.device) + channel + 'custom_thresh_mask.png'))
    return mask, masked_img


# Internal method for calling the OpenCV threshold function to reduce code duplication
def _call_threshold(gray_img, threshold, threshold_method, method_name):
    """Calls the OpenCV threshold function to reduce code duplication

    Parameters
    ----------
    gray_img : numpy.ndarray
        Grayscale image data
    threshold : int
        Threshold value
    threshold_method : int
        OpenCV thresholding method
    method_name : str
        Name of the method used for debugging purposes

    Returns
    -------
    numpy.ndarray
        Thresholded, binary image
    """
    # Threshold the image
    _, bin_img = cv2.threshold(gray_img, threshold, 255, threshold_method)

    if bin_img.dtype != 'uint16':
        bin_img = np.uint8(bin_img)

    # Print or plot the binary image if debug is on
    _debug(visual=bin_img, filename=os.path.join(params.debug_outdir,
                                                 str(params.device) + method_name + str(threshold) + '.png'))

    return bin_img


# Internal method for calling the OpenCV adaptiveThreshold function to reduce code duplication
def _call_adaptive_threshold(gray_img, ksize, offset, adaptive_method, threshold_method, method_name):
    """Calls the OpenCV adaptiveThreshold function to reduce code duplication

    Parameters
    ----------
    gray_img : numpy.ndarray
        Grayscale image data
    ksize : int
        Size of the block of pixels used to compute the local average
    offset : float
        Value substracted from the local average to compute the local threshold
    adaptive_method : int
        Adaptive thresholding algorithm to use
    threshold_method : int
        Thresholding method to use
    method_name : str
        Name of the method used for debugging purposes

    Returns
    -------
    numpy.ndarray
        Thresholded, binary image
    """
    if ksize < 3:
        fatal_error("ksize must be >= 3")

    # Force ksize to be odd number
    ksize = int(ksize)
    if (ksize % 2) != 1:
        ksize = ksize + 1

    # Threshold the image
    bin_img = cv2.adaptiveThreshold(gray_img, 255, adaptive_method, threshold_method, ksize, offset)

    # Print or plot the binary image if debug is on
    _debug(visual=bin_img, filename=os.path.join(params.debug_outdir, str(params.device) + method_name + '.png'))

    return bin_img


# Internal method for detecting peaks for the triangle autothreshold method
def _detect_peaks(x, mph=None, mpd=1, threshold=0, edge='rising', valley=False, show=False, ax=None):
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

    # It is always the case that x.size=256 since 256 hardcoded in line 186 ->
    # cv2.calcHist([gray_img], [0], None, [256], [0, 255])
    # if x.size < 3:
    #     return np.array([], dtype=int)

    # # Where this function is used it is hardcoded to use the default valley=False so this will never be used
    # if valley:
    #     x = -x
    # find indices of all peaks
    dx = x[1:] - x[:-1]
    # handle NaN's
    # indnan = np.where(np.isnan(x))[0]

    # x will never contain NaN since calcHist will never return NaN
    # if indnan.size:
    #     x[indnan] = np.inf
    #     dx[np.where(np.isnan(dx))[0]] = np.inf
    ine, ire, ife = np.array([[], [], []], dtype=int)

    if edge.lower() in ['rising', 'both']:
        ire = np.where((np.hstack((dx, 0)) <= 0) & (np.hstack((0, dx)) > 0))[0]
    ind = np.unique(np.hstack((ine, ire, ife)))
    # x will never contain NaN since calcHist will never return NaN
    # if ind.size and indnan.size:
    #     # NaN's and values close to NaN's cannot be peaks
    #     ind = ind[np.in1d(ind, np.unique(np.hstack((indnan, indnan - 1, indnan + 1))), invert=True)]
    # first and last values of x cannot be peaks
    # if ind.size and ind[0] == 0:
    #     ind = ind[1:]
    # if ind.size and ind[-1] == x.size - 1:
    #     ind = ind[:-1]
    # We think the above code will never be reached given some of the hardcoded properties used

    # # Where this function is used has hardcoded mph=None so this will never be used
    # # remove peaks < minimum peak height
    # if ind.size and mph is not None:
    #     ind = ind[x[ind] >= mph]
    # remove peaks - neighbors < threshold

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
                label=f'{ind.size} {label}')
        ax.legend(loc='best', framealpha=.5, numpoints=1)
    ax.set_xlim(-.02 * x.size, x.size * 1.02 - 1)
    ymin, ymax = x[np.isfinite(x)].min(), x[np.isfinite(x)].max()
    yrange = ymax - ymin if ymax > ymin else 1
    ax.set_ylim(ymin - 0.1 * yrange, ymax + 0.1 * yrange)
    ax.set_xlabel('Data #', fontsize=14)
    ax.set_ylabel('Amplitude', fontsize=14)
    mode = 'Valley detection' if valley else 'Peak detection'
    ax.set_title(f"{mode} ({mph=}, {mpd=}, {threshold=}, {edge=})")
    plt.show()


def saturation(rgb_img, threshold=255, channel="any"):
    """Return a mask filtering out saturated pixels.

    Inputs:
    rgb_img    = RGB image
    threshold  = value for threshold, above which is considered saturated
    channel    = how many channels must be saturated for the pixel to be masked out ("any", "all")

    Returns:
    masked_img = A binary image with the saturated regions blacked out.

    :param rgb_img: np.ndarray
    :param threshold: int
    :param channel: str
    :return masked_img: np.ndarray
    """
    # Mask red, green, and blue saturation separately
    b, g, r = cv2.split(rgb_img)
    b_saturated = cv2.inRange(b, threshold, 255)
    g_saturated = cv2.inRange(g, threshold, 255)
    r_saturated = cv2.inRange(r, threshold, 255)

    # Combine channel masks
    if channel.lower() == "any":
        # Consider a pixel saturated if any channel is saturated
        saturated = cv2.bitwise_or(b_saturated, g_saturated)
        saturated = cv2.bitwise_or(saturated, r_saturated)
    elif channel.lower() == "all":
        # Consider a pixel saturated only if all channels are saturated
        saturated = cv2.bitwise_and(b_saturated, g_saturated)
        saturated = cv2.bitwise_and(saturated, r_saturated)
    else:
        fatal_error(str(channel) + " is not a valid option. Channel must be either 'any', or 'all'.")

    # Invert "saturated" before returning, so saturated = black
    bin_img = cv2.bitwise_not(saturated)

    _debug(visual=bin_img, filename=os.path.join(params.debug_outdir, str(params.device), '_saturation_threshold.png'))
    return bin_img


def mask_bad(float_img, bad_type='native'):
    """Create a mask with desired "bad" pixels of the input floaat image marked.
    Inputs:
    float_img = image represented by an nd-array (data type: float). Most probably, it is the result of some
                calculation based on the original image. So the datatype is float, and it is possible to have some
                "bad" values, i.e. nan and/or inf
    bad_type = definition of "bad" type, can be 'nan', 'inf' or 'native'
    Returns:
    mask = A mask indicating the locations of "bad" pixels

    :param float_img: numpy.ndarray
    :param bad_type: str
    :return mask: numpy.ndarray
    """
    size_img = np.shape(float_img)
    if len(size_img) != 2:
        fatal_error('Input image is not a single channel image!')

    mask = np.zeros(size_img, dtype='uint8')
    idx_nan, idy_nan = np.where(np.isnan(float_img) == 1)
    idx_inf, idy_inf = np.where(np.isinf(float_img) == 1)

    # neither nan nor inf exists in the image, print out a message and the mask would just be all zero
    if len(idx_nan) == 0 and len(idx_inf) == 0:
        print('Neither nan nor inf appears in the current image.')
    # at least one of the "bad" exists
    # desired bad to mark is "native"
    elif bad_type.lower() == 'native':
        mask[idx_nan, idy_nan] = 255
        mask[idx_inf, idy_inf] = 255
    elif bad_type.lower() == 'nan' and len(idx_nan) >= 1:
        mask[idx_nan, idy_nan] = 255
    elif bad_type.lower() == 'inf' and len(idx_inf) >= 1:
        mask[idx_inf, idy_inf] = 255
    # "bad" exists but not the user desired bad type, return the all-zero mask
    else:
        print(f'{format(bad_type.lower())} does not appear in the current image.')

    _debug(visual=mask, filename=os.path.join(params.debug_outdir, str(params.device) + "_bad_mask.png"))

    return mask


# functions to get a given channel with parameters compatible
# with rgb2gray_lab and rgb2gray_hsv to use in the dict
def _get_R(rgb_img, _):
    """Get the red channel from a RGB image"""
    return rgb_img[:, :, 2]


def _get_G(rgb_img, _):
    """Get the green channel from a RGB image"""
    return rgb_img[:, :, 1]


def _get_B(rgb_img, _):
    """Get the blue channel from a RGB image"""
    return rgb_img[:, :, 0]


def _get_gray(rgb_img, _):
    """Get the gray scale transformation of a RGB image"""
    return rgb2gray(rgb_img=rgb_img)


def _get_index(rgb_img, _):
    """Get a vector with linear indices of the pixels in an image"""
    h, w, _ = rgb_img.shape
    return np.arange(h*w).reshape(h, w)


def _not_valid(*args):
    """Error for a non valid channel"""
    return fatal_error("channel not valid, use R, G, B, l, a, b, h, s, v, gray, or index")


def dual_channels(rgb_img, x_channel, y_channel, points, above=True):
    """Create a binary image from an RGB image based on the pixels values in two channels.
    The x and y channels define a 2D plane and the two input points define a straight line.
    Pixels in the plane above and below the straight line are assigned two different values.
    Inputs:
    rgb_img   = RGB image
    ch_x      = Channel to use for the horizontal coordinate.
                Options:  'R', 'G', 'B', 'l', 'a', 'b', 'h', 's', 'v', 'gray', and 'index'
    ch_y      = Channel to use for the vertical coordinate.
                Options:  'R', 'G', 'B', 'l', 'a', 'b', 'h', 's', 'v', 'gray', and 'index'
    points    = List containing two points as tuples defining the segmenting straight line
    above     = Whether the pixels above the line are given the value of 0 or max_value

    Returns:
    bin_img      = Thresholded, binary image
    :param rgb_img: numpy.ndarray
    :param x_channel: str
    :param y_channel: str
    :param points: list of two tuples
    :param above: bool
    :return bin_img: numpy.ndarray
    """
    # dictionary returns the function that gets the required image channel
    channel_dict = {
        'R': _get_R,
        'G': _get_G,
        'B': _get_B,
        'l': rgb2gray_lab,
        'a': rgb2gray_lab,
        'b': rgb2gray_lab,
        'gray': _get_gray,
        'h': rgb2gray_hsv,
        's': rgb2gray_hsv,
        'v': rgb2gray_hsv,
        'index': _get_index,
    }

    debug = params.debug
    params.debug = None
    # get channels
    img_x_ch = channel_dict.get(x_channel, _not_valid)(rgb_img, x_channel)
    img_x_ch = img_x_ch.astype(np.float64)
    img_y_ch = channel_dict.get(y_channel, _not_valid)(rgb_img, y_channel)
    img_y_ch = img_y_ch.astype(np.float64)
    params.debug = debug

    if len(points) < 2:
        fatal_error('Two points are required')

    if len(points) > 2:
        # Print warning statement
        warn("only the first two points are used in this function")

    x0, y0 = points[0]
    x1, y1 = points[1]

    m = (y1-y0) / (x1-x0+1e-10)  # avoid division by 0
    b = y0 - m*x0

    y_line = m*img_x_ch + b

    max_value = 255
    if above:
        bin_img = max_value*(img_y_ch > y_line)
    else:
        bin_img = max_value*(img_y_ch < y_line)

    bin_img = bin_img.astype(np.uint8)

    _debug(visual=bin_img, filename=os.path.join(params.debug_outdir,
                                                 str(params.device) + '_' + x_channel + y_channel + '_2D_threshold_mask.png'))

    return bin_img
