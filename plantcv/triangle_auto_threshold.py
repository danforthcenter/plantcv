# Binary image auto threshold

from __future__ import division, print_function
import cv2
import math
import numpy as np
from . import print_image
from . import plot_image


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
    if x.size < 3:
        return np.array([], dtype=int)
    if valley:
        x = -x
    # find indices of all peaks
    dx = x[1:] - x[:-1]
    # handle NaN's
    indnan = np.where(np.isnan(x))[0]
    if indnan.size:
        x[indnan] = np.inf
        dx[np.where(np.isnan(dx))[0]] = np.inf
    ine, ire, ife = np.array([[], [], []], dtype=int)
    if not edge:
        ine = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) > 0))[0]
    else:
        if edge.lower() in ['rising', 'both']:
            ire = np.where((np.hstack((dx, 0)) <= 0) & (np.hstack((0, dx)) > 0))[0]
        if edge.lower() in ['falling', 'both']:
            ife = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) >= 0))[0]
    ind = np.unique(np.hstack((ine, ire, ife)))
    # handle NaN's
    if ind.size and indnan.size:
        # NaN's and values close to NaN's cannot be peaks
        ind = ind[np.in1d(ind, np.unique(np.hstack((indnan, indnan - 1, indnan + 1))), invert=True)]
    # first and last values of x cannot be peaks
    if ind.size and ind[0] == 0:
        ind = ind[1:]
    if ind.size and ind[-1] == x.size - 1:
        ind = ind[:-1]
    # remove peaks < minimum peak height
    if ind.size and mph is not None:
        ind = ind[x[ind] >= mph]
    # remove peaks - neighbors < threshold
    if ind.size and threshold > 0:
        dx = np.min(np.vstack([x[ind] - x[ind - 1], x[ind] - x[ind + 1]]), axis=0)
        ind = np.delete(ind, np.where(dx < threshold)[0])
    # detect small peaks closer than minimum peak distance
    if ind.size and mpd > 1:
        ind = ind[np.argsort(x[ind])][::-1]  # sort ind by peak height
        idel = np.zeros(ind.size, dtype=bool)
        for i in range(ind.size):
            if not idel[i]:
                # keep peaks with the same height if kpsh is True
                idel = idel | (ind >= ind[i] - mpd) & (ind <= ind[i] + mpd) \
                              & (x[ind[i]] > x[ind] if kpsh else True)
                idel[i] = 0  # Keep current peak
        # remove the small peaks and sort back the indices by their occurrence
        ind = np.sort(ind[~idel])

    if show:
        if indnan.size:
            x[indnan] = np.nan
        if valley:
            x = -x
        _plot(x, mph, mpd, threshold, edge, valley, ax, ind)

    return ind


def _plot(x, mph, mpd, threshold, edge, valley, ax, ind):
    """Plot results of the detect_peaks function, see its help."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print('matplotlib is not available.')
    else:
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


def triangle_auto_threshold(device, img, maxvalue, object_type, xstep=1, debug=None):
    """Creates a binary image from a grayscaled image using Zack et al.'s (1977) thresholding.

    Inputs:
    device      = device number. Used to count steps in the pipeline
    img         = img object, grayscale
    maxvalue    = value to apply above threshold (usually 255 = white)
    object_type = light or dark
                  - If object is light then standard thresholding is done
                  - If object is dark then inverse thresholding is done
    xstep       = value to move along x-axis to determine the points from which to calculate distance
                    recommended to start at 1 and change if needed)
    debug       = True/False. If True, print image

    Returns:
    device      = device number
    t_img       = the thresholded image


    :param img: numpy array
    :param maxvalue: int
    :param object_type: str
    :param device: int
    :param debug: bool
    :param xstep: optional int
    :return device: int
    :return t_img: numpy array
    """
    device += 1

    # Calculate automatic threshold value based on triangle algorithm
    hist = cv2.calcHist([img], [0], None, [256], [0, 255])

    # Make histogram one array
    newhist = []
    for item in hist:
        newhist.extend(item)

    # Detect peaks
    ind = _detect_peaks(newhist, mph=None, mpd=1)

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

    # check whether to inverse the image or not and make an ending extension
    obj = 0
    extension = ''
    if object_type == 'light':
        extension = '.png'
        obj = cv2.THRESH_BINARY
    elif object_type == 'dark':
        extension = '_inv.png'
        obj = cv2.THRESH_BINARY_INV

    # threshold the image based on the object type using triangle binarization
    t_val, t_img = cv2.threshold(img, autothreshval, maxvalue, obj)

    if debug is not None:
        import matplotlib
        matplotlib.use('Agg')
        from matplotlib import pyplot as plt

    if debug == 'print':
        name = str(device) + '_triangle_thresh_img_' + str(t_val) + str(extension)
        print_image(t_img, name)
        plt.clf()

        plt.plot(hist)
        plt.title('Threshold value = {t}'.format(t=autothreshval))
        plt.axis([0, 256, 0, max(hist)])
        plt.grid('on')
        fig_name_hist = str(device) + '_triangle_thresh_hist_' + str(t_val) + str(extension)
        # write the figure to current directory
        plt.savefig(fig_name_hist)
        # close pyplot plotting window
        plt.clf()

    elif debug == 'plot':
        print('Threshold value = {t}'.format(t=autothreshval))
        plot_image(t_img, cmap="gray")

        plt.plot(hist)
        plt.axis([0, 256, 0, max(hist)])
        plt.grid('on')
        plt.show()

    return device, t_img
