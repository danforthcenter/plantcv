import cv2
import numpy as np
import math
from skimage import morphology
from plantcv.plantcv import fatal_error, warn
from plantcv.plantcv import params
import pandas as pd


def _closing(gray_img, kernel=None, roi=None):
    """Wrapper for scikit-image closing functions.

    Opening can remove small dark spots (i.e. pepper).

    Parameters
    ----------
    gray_img = numpy.ndarray
             input image (grayscale or binary)
    kernel   = numpy.ndarray
             optional neighborhood, expressed as an array of 1s and 0s. If None, use cross-shaped structuring element.
    roi : Objects class
             Optional rectangular ROI to erode within

    Returns
    -------
    numpy.ndarray
         filtered (holes closed) image

    Raises
    ------
    ValueError
        If input image is not gray-scale
    """
    # Make sure the image is binary/grayscale
    if len(np.shape(gray_img)) != 2:
        fatal_error("Input image must be grayscale or binary")

    if len(np.unique(gray_img)) <= 2:
        bool_img = gray_img.astype(bool)
        sub_img = _rect_filter(bool_img, roi=roi, function=morphology.binary_closing,
                               **{"footprint": kernel})
        filtered_img = sub_img.astype(np.uint8) * 255
        replaced_img = _rect_replace(bool_img.astype(np.uint8) * 255, filtered_img, roi)
    # Otherwise use method appropriate for grayscale images
    else:
        filtered_img = _rect_filter(gray_img,
                                    roi=roi,
                                    function=morphology.closing,
                                    **{"footprint": kernel})
        replaced_img = _rect_replace(gray_img, filtered_img, roi)

    return replaced_img


def _image_subtract(gray_img1, gray_img2):
    """Subtract values of one gray-scale image array from another gray-scale image array.

    The
    resulting gray-scale image array has a minimum element value of zero. That is all negative values resulting from the
    subtraction are forced to zero.

    Parameters
    ----------
    gray_img1 : numpy.ndarray
              Grayscale image data from which gray_img2 will be subtracted
    gray_img2 : numpy.ndarray
              Grayscale image data which will be subtracted from gray_img1

    Returns
    -------
    new_img = subtracted image

    Raises
    ------
    ValueError
         If input image is not gray scale
    """
    # check inputs for gray-scale
    if len(np.shape(gray_img1)) != 2 or len(np.shape(gray_img2)) != 2:
        fatal_error("Input image is not gray-scale")

    new_img = gray_img1.astype(np.float64) - gray_img2.astype(np.float64)  # subtract values
    new_img[np.where(new_img < 0)] = 0  # force negative array values to zero
    new_img = new_img.astype(np.uint8)  # typecast image to 8-bit image

    return new_img  # return


def _erode(gray_img, ksize, i, roi=None):
    """Perform morphological 'erosion' filtering.

    Keeps pixel in center of the kernel if conditions set in kernel are
       true, otherwise removes pixel.

    Parameters
    ----------
    gray_img : numpy.ndarray
             Grayscale (usually binary) image data
    ksize : int
             Kernel size (int). A ksize x ksize kernel will be built. Must be greater than 1 to have an effect.
    i : int
             interations, i.e. number of consecutive filtering passes
    roi : Objects class
             Optional rectangular ROI to erode within

    Returns
    -------
    numpy.ndarray
         Eroded result image

    Raises
    ------
    ValueError
        If ksize is less than or equal to 1.
    """
    if ksize <= 1:
        raise ValueError('ksize needs to be greater than 1 for the function to have an effect')

    kernel1 = int(ksize)
    kernel2 = np.ones((kernel1, kernel1), np.uint8)
    sub_er_img = _rect_filter(img=gray_img, roi=roi, function=cv2.erode,
                              **{"kernel": kernel2, "iterations": i})
    er_img = _rect_replace(gray_img, sub_er_img, roi)

    return er_img


def _dilate(gray_img, ksize, i, roi=None):
    """Performs morphological 'dilation' filtering.

    Parameters
    ----------
    gray_img : numpy.ndarray
        Grayscale image data to be dilated
    ksize : int
        Kernel size (int). A k x k kernel will be built. Must be greater than 1 to have an effect.
    i : int
        Number of iterations (i.e. how many times to apply the dilation).
    roi : Objects class
        Optional rectangular ROI to erode within

    Returns
    -------
    numpy.ndarray
        Dilation result image

    Raises
    ------
    ValueError
        If ksize is less than or equal to 1.
    """
    if ksize <= 1:
        raise ValueError('ksize needs to be greater than 1 for the function to have an effect')

    kernel1 = int(ksize)
    kernel2 = np.ones((kernel1, kernel1), np.uint8)
    sub_dil_img = _rect_filter(img=gray_img, roi=roi, function=cv2.dilate,
                               **{"kernel": kernel2, "iterations": i})
    dil_img = _rect_replace(gray_img, sub_dil_img, roi)

    return dil_img


def _find_segment_ends(skel_img, leaf_objects, plotting_img, size):
    """Find both segment ends and sort into tips or inner branchpoints.
    Inputs:
    skel_img         = Skeletonized image
    leaf_objects     = List of leaf segments
    plotting_img     = Mask for debugging, might be a copy of the Skeletonized image
    size             = Size of inner segment ends (in pixels)
    :param skel_img: numpy.ndarray
    :param leaf_objects: list
    :param plotting_img: numpy.ndarray
    """
    labeled_img = cv2.cvtColor(plotting_img, cv2.COLOR_GRAY2RGB)
    tips, _, _ = _find_tips(skel_img)
    # Initialize list of tip data points
    labels = []
    tip_list = []
    inner_list = []
    remove = []
    sortabled_objs = leaf_objects.copy()

    # Find segment end coordinates
    for i in range(len(leaf_objects)):
        labels.append(i)
        # Draw leaf objects
        find_segment_tangents = np.zeros(labeled_img.shape[:2], np.uint8)
        cv2.drawContours(find_segment_tangents, leaf_objects, i, 255, 1, lineType=8)
        cv2.drawContours(labeled_img, leaf_objects, i, (150, 150, 150), params.line_thickness, lineType=8)  # segments debug
        # Prune back ends of leaves
        pruned_segment = _iterative_prune(find_segment_tangents, size)
        # Segment ends are the portions pruned off
        ends = find_segment_tangents - pruned_segment
        segment_end_obj, _ = _cv2_findcontours(bin_img=ends)
        branch_pt_found = False
        coords = []
        # Determine if a segment is segment tip or branch point
        for j, obj in enumerate(segment_end_obj):
            segment_plot = np.zeros(skel_img.shape[:2], np.uint8)
            cv2.drawContours(segment_plot, obj, -1, 255, 1, lineType=8)
            segment_plot = _dilate(segment_plot, 3, 1)
            overlap_img = _logical_operation(segment_plot, tips, 'and')
            x, y = segment_end_obj[j].ravel()[:2]
            coord = (int(x), int(y))
            coords.append(coord)
            # If none of the tips are within a segment_end then it's an insertion segment
            if np.sum(overlap_img) == 0:
                inner_list.append(coord)
                cv2.circle(labeled_img, coord, params.line_thickness, (50, 0, 255), -1)  # Red auricles/branch points
                branch_pt_found = True
            else:
                tip_list.append(coord)
                cv2.circle(labeled_img, coord, params.line_thickness, (0, 255, 0), -1)  # green tips
        if not branch_pt_found:  # there is no branch point associated with a given segment and therefore it cannot be sorted
            remove.append(i)
            # Plot the ends if found
            if len(coords) > 1:
                # Plot the tip that is closest to the stem
                x_min, y_min, w, h = cv2.boundingRect(skel_img)
                cx = int((x_min + (w / 2)))
                cy = int(y_min + h)
                dist0 = math.dist(coords[0], (cx, cy))
                dist1 = math.dist(coords[1], (cx, cy))
                m = 1
                if dist0 < dist1:
                    m = 0

                cv2.circle(labeled_img, (cx, cy), params.line_thickness + 10, (255, 0, 0), 5)  # estimated centroid point
                cv2.circle(labeled_img, coords[m], params.line_thickness, (255, 20, 20), -1)  # estimated sorting point
                cv2.putText(img=labeled_img, text=str(int(dist0)), org=coords[0], fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=params.text_size, color=(150, 150, 150), thickness=params.text_thickness)
                cv2.putText(img=labeled_img, text=str(int(dist1)), org=coords[1], fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=params.text_size, color=(150, 150, 150), thickness=params.text_thickness)

    # Remove the segments that cannot be resorted, since they do not have a branch point
    for k in remove:
        sortabled_objs.pop(k)

    return labeled_img, tip_list, inner_list, labels, sortabled_objs


def _iterative_prune(skel_img, size):
    """Iteratively remove endpoints (tips) from a skeletonized image.
    The pruning algorithm was inspired by Jean-Patrick Pommier: https://gist.github.com/jeanpat/5712699
    "Prunes" barbs off a skeleton.
    Inputs:
    skel_img    = Skeletonized image
    size        = Size to get pruned off each branch
    Returns:
    pruned_img  = Pruned image
    :param skel_img: numpy.ndarray
    :param size: int
    :return pruned_img: numpy.ndarray
    """
    pruned_img = skel_img.copy()
    # Store debug
    debug = params.debug
    params.debug = None

    # Iteratively remove endpoints (tips) from a skeleton
    for _ in range(0, size):
        endpoints, _, _ = _find_tips(pruned_img)
        pruned_img = _image_subtract(pruned_img, endpoints)

    # Make debugging image
    pruned_plot = np.zeros(skel_img.shape[:2], np.uint8)
    pruned_plot = cv2.cvtColor(pruned_plot, cv2.COLOR_GRAY2RGB)
    skel_obj, skel_hierarchy = _cv2_findcontours(bin_img=pruned_img)
    pruned_obj, pruned_hierarchy = _cv2_findcontours(bin_img=pruned_img)

    # Reset debug mode
    params.debug = debug

    cv2.drawContours(pruned_plot, skel_obj, -1, (0, 0, 255), params.line_thickness,
                     lineType=8, hierarchy=skel_hierarchy)
    cv2.drawContours(pruned_plot, pruned_obj, -1, (255, 255, 255), params.line_thickness,
                     lineType=8, hierarchy=pruned_hierarchy)

    return pruned_img


def _find_tips(skel_img, mask=None):
    """Helper function to find tips in skeletonized image.
    The endpoints algorithm was inspired by Jean-Patrick Pommier: https://gist.github.com/jeanpat/5712699

    Inputs:
    skel_img    = Skeletonized image
    mask        = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.
    label       = Optional label parameter, modifies the variable name of
                  observations recorded (default = pcv.params.sample_label).
    Returns:
    tip_img   = Image with just tips, rest 0

    :param skel_img: numpy.ndarray
    :param mask: numpy.ndarray
    :param label: str
    :return tip_img: numpy.ndarray
    """
    # In a kernel: 1 values line up with 255s, -1s line up with 0s, and 0s correspond to dont care
    endpoint1 = np.array([[-1, -1, -1],
                          [-1, 1, -1],
                          [0, 1,  0]])
    endpoint2 = np.array([[-1, -1, -1],
                          [-1, 1, 0],
                          [-1, 0, 1]])

    endpoint3 = np.rot90(endpoint1)
    endpoint4 = np.rot90(endpoint2)
    endpoint5 = np.rot90(endpoint3)
    endpoint6 = np.rot90(endpoint4)
    endpoint7 = np.rot90(endpoint5)
    endpoint8 = np.rot90(endpoint6)

    endpoints = [endpoint1, endpoint2, endpoint3, endpoint4, endpoint5, endpoint6, endpoint7, endpoint8]
    tip_img = np.zeros(skel_img.shape[:2], dtype=int)
    for endpoint in endpoints:
        tip_img = np.logical_or(cv2.morphologyEx(skel_img, op=cv2.MORPH_HITMISS, kernel=endpoint,
                                                 borderType=cv2.BORDER_CONSTANT, borderValue=0), tip_img)
    tip_img = tip_img.astype(np.uint8) * 255
    # Store debug
    debug = params.debug
    params.debug = None
    tip_objects, _ = _cv2_findcontours(bin_img=tip_img)

    if mask is None:
        # Make debugging image
        dilated_skel = _dilate(skel_img, params.line_thickness, 1)
        tip_plot = cv2.cvtColor(dilated_skel, cv2.COLOR_GRAY2RGB)

    else:
        # Make debugging image on mask
        mask_copy = mask.copy()
        tip_plot = cv2.cvtColor(mask_copy, cv2.COLOR_GRAY2RGB)
        skel_obj, skel_hier = _cv2_findcontours(bin_img=skel_img)
        cv2.drawContours(tip_plot, skel_obj, -1, (150, 150, 150), params.line_thickness,
                         lineType=8, hierarchy=skel_hier)

    # Initialize list of tip data points
    tip_list = []
    tip_labels = []
    for i, tip in enumerate(tip_objects):
        x, y = tip.ravel()[:2]
        coord = (int(x), int(y))
        tip_list.append(coord)
        tip_labels.append(i)
        cv2.circle(tip_plot, (x, y), params.line_thickness, (0, 255, 0), -1)

    # Reset debug mode
    params.debug = debug

    return tip_img, tip_list, tip_labels


def _hough_circle(gray_img, mindist, candec, accthresh, minradius, maxradius, maxfound=None):
    """
    Hough Circle Detection

    Keyword inputs:
    gray_img = gray image (np.ndarray)
    mindist = minimum distance between detected circles
    candec = higher threshold of canny edge detector
    accthresh = accumulator threshold for the circl centers
    minradius = minimum circle radius
    maxradius = maximum circle radius
    maxfound = maximum number of circles to find

    :param gray_img: np.ndarray
    :param mindist: int
    :param candec: int
    :param accthresh: int
    :param minradius: int
    :param maxradius: int
    :param maxfound: None or int
    :return dataframe: pandas dataframe
    :return img: np.ndarray
    """
    # Store debug
    debug = params.debug
    params.debug = None

    circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT,
                               dp=1, minDist=mindist,
                               param1=candec, param2=accthresh,
                               minRadius=minradius, maxRadius=maxradius)

    cimg = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
    x = []
    y = []
    radius = []
    if circles is None:
        fatal_error('number of circles found is None with these parameters')
    circles = np.uint16(np.around(circles))
    if maxfound is not None:
        if maxfound >= len(circles[0, :]):
            for i in circles[0, :]:
                # draw the outer circle
                cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0),
                           params.line_thickness)
                # draw the center of the circle
                cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255),
                           params.line_thickness)
                x.append(i[0])
                y.append(i[1])
                radius.append(i[2])
        else:
            for n, i in enumerate(circles[0, :]):
                if n <= (maxfound-1):
                    # draw the outer circle
                    cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0),
                               params.line_thickness)
                    # draw the center of the circle
                    cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255),
                               params.line_thickness)
                    x.append(i[0])
                    y.append(i[1])
                    radius.append(i[2])
            warn('Number of found circles is ' +
                 str(len(circles[0, :])) +
                 ' Change Parameters. Only drawing first '+str(maxfound))
    else:
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0),
                       params.line_thickness)
            # draw the center of the circle
            cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255),
                       params.line_thickness)
            x.append(i[0])
            y.append(i[1])
            radius.append(i[2])

    data = {'x': x, 'y': y, 'radius': radius}
    df = pd.DataFrame(data)

    # Reset debug mode
    params.debug = debug

    return df, cimg


def _cv2_findcontours(bin_img):
    """
    Helper function for OpenCV findContours.

    Reduces duplication of calls to findContours in the event the OpenCV function changes.

    Keyword inputs:
    bin_img = Binary image (np.ndarray)

    :param bin_img: np.ndarray
    :return contours: list
    :return hierarchy: np.array
    """
    contours, hierarchy = cv2.findContours(np.copy(bin_img), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

    return contours, hierarchy


def _roi_filter(img, roi, obj, hierarchy, roi_type="partial"):
    """
    Helper function to filter contours using a single ROI.

    Finds objects partially inside a region of interest or cuts objects to the ROI.

    Parameters
    ----------
    img : numpy.ndarray
        RGB, binary, or grayscale image data for shape.
    roi : plantcv.plantcv.classes.Objects
        Region of interest, an instance of the Object class output from a ROI function.
    obj : list
        Contours of objects, output from "_cv2_findcontours" function.
    hierarchy : numpy.ndarray
        Hierarchy of objects, output from "_cv2_findcontours" function.
    roi_type : str, optional
        Type of ROI filtering. Options are:
        - 'partial': Find objects partially inside the ROI (default).
        - 'cutto': Cut objects to the ROI.
        - 'largest': Keep only the largest contour.
        - 'within': Keep only objects fully within the ROI.

    Returns
    -------
    kept_cnt : list
        List of kept contours after filtering.
    kept_hier : numpy.ndarray
        Hierarchy of kept contours.
    mask : numpy.ndarray
        Mask image showing the filtered contours.

    Raises
    ------
    RuntimeError
        If an invalid `roi_type` is provided.

    Notes
    -----
    If a multi-ROI is provided, only the first ROI will be used. For multi-ROI processing, consider using a for loop.
    """
    # Store debug
    debug = params.debug
    params.debug = None

    if len(roi.contours) > 1:
        warn("received a multi-ROI but only the first ROI will be used. Consider using a for loop for multi-ROI")

    roi_contour = roi.contours[0]
    object_contour = obj
    obj_hierarchy = hierarchy

    # Create an empty grayscale (black) image the same dimensions as the input image
    mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
    cv2.drawContours(mask, object_contour, -1, (255), -1, lineType=8, hierarchy=obj_hierarchy)

    # Create a mask of the filled in ROI
    roi_mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
    roi_points = np.vstack(roi_contour[0])
    cv2.fillPoly(roi_mask, [roi_points], (255))

    # Allows user to find all objects that are completely inside or overlapping with ROI
    if roi_type.upper() in ('PARTIAL', 'LARGEST'):
        # Filter contours outside of the region of interest
        for c, _ in enumerate(object_contour):
            filtering_mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
            cv2.fillPoly(filtering_mask, [np.vstack(object_contour[c])], (255))
            overlap_img = _logical_operation(filtering_mask, roi_mask, 'and')
            # Delete contours that do not overlap at all with the ROI
            if np.sum(overlap_img) == 0:
                cv2.drawContours(mask, object_contour, c, (0), -1, lineType=8, hierarchy=obj_hierarchy)

        # Find the kept contours and area
        kept_cnt, kept_hierarchy = _cv2_findcontours(bin_img=mask)

        # Find the largest contour if roi_type is set to 'largest'
        if roi_type.upper() == 'LARGEST' and kept_cnt:
            index = np.argmax([cv2.contourArea(c) for c in kept_cnt])
            mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
            cv2.drawContours(mask, kept_cnt, contourIdx=index, color=(255), thickness=-1, hierarchy=kept_hierarchy, maxLevel=2)
            kept_cnt, kept_hierarchy = _cv2_findcontours(bin_img=mask)

    # Allows user to cut objects to the ROI (all objects completely outside ROI will not be kept)
    elif roi_type.upper() in ('CUTTO', 'WITHIN'):
        background1 = np.zeros(np.shape(img)[:2], dtype=np.uint8)
        background2 = np.zeros(np.shape(img)[:2], dtype=np.uint8)
        cv2.drawContours(background1, object_contour, -1, (255), -1, lineType=8, hierarchy=obj_hierarchy)
        roi_points = np.vstack(roi_contour[0])
        cv2.fillPoly(background2, [roi_points], (255))
        mask = cv2.multiply(background1, background2)
        kept_cnt, kept_hierarchy = _cv2_findcontours(bin_img=mask)

        # Filter out contours that touch the edge if roi_type is 'within'
        if roi_type.upper() == 'WITHIN' and kept_cnt:
            # make a mask with the outline of the ROI
            roi_outline_mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
            cv2.drawContours(image=roi_outline_mask, contours=roi_contour, contourIdx=-1,
                             color=255, thickness=1)
            # make empty mask to append to
            within_mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
            for c, _ in enumerate(kept_cnt):
                # for each contour make a mask with that contour filled
                filtering_mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
                cv2.fillPoly(filtering_mask, [np.vstack(kept_cnt[c])], (255))
                # check overlap with traced ROI
                overlap_img = _logical_operation(filtering_mask, roi_outline_mask, 'and')
                # check color in original mask, ie don't keep gaps that are 0s.
                # append contours fully within ROI to the within_mask
                if not overlap_img.any() and kept_hierarchy[0][c][3] == -1:
                    cv2.drawContours(within_mask, kept_cnt, c,
                                     int(img[kept_cnt[c][0][0][1], kept_cnt[c][0][0][0]]),
                                     -1, lineType=8, hierarchy=kept_hierarchy)
            mask = within_mask
            kept_cnt, kept_hierarchy = _cv2_findcontours(bin_img=mask)
    else:
        # Reset debug mode
        params.debug = debug
        fatal_error('ROI Type ' + str(roi_type) + ' is not "cutto", "largest", "within" or "partial"!')

    # Reset debug mode
    params.debug = debug

    return kept_cnt, kept_hierarchy, mask


def _iterate_analysis(img, labeled_mask, n_labels, label, function, **kwargs):
    """Iterate over labels and apply an analysis function.
    Inputs:
    img      = image to be used for visualization
    mask     = labeled mask
    n_labels = number of expected labels
    label    = label parameter, modifies the variable name of observations recorded
    function = analysis function to apply to each submask
    kwargs   = additional keyword arguments to pass to the analysis function

    :param img: np.ndarray
    :param mask: np.ndarray
    :param n_labels: int
    :param label: str
    :param function: function
    :param kwargs: dict
    """
    # Set labels to label
    labels = label
    # If label is a string, make a list of labels
    if isinstance(label, str):
        labels = [label] * n_labels
    # If the length of the labels list is not equal to the number of labels, raise an error
    if len(labels) != n_labels:
        fatal_error(f"Number of labels ({len(labels)}) does not match number of objects ({n_labels})")
    mask_copy = np.copy(labeled_mask)
    if len(np.unique(mask_copy)) == 2 and np.max(mask_copy) == 255:
        mask_copy = np.where(mask_copy == 255, 1, 0).astype(np.uint8)
    for i in range(1, n_labels + 1):
        submask = np.where(mask_copy == i, 255, 0).astype(np.uint8)
        img = function(img=img, mask=submask, label=f"{labels[i - 1]}_{i}", **kwargs)
    return img


def _object_composition(contours, hierarchy):
    """
    Groups objects into a single object, usually done after object filtering.

    Inputs:
    contours  = Contour tuple
    hierarchy = Contour hierarchy NumPy array

    Returns:
    group    = grouped contours list

    :param contours: tuple
    :param hierarchy: numpy.ndarray
    :return group: numpy.ndarray
    """
    stack = np.zeros((len(contours), 1))

    for c, _ in enumerate(contours):
        if hierarchy[0][c][2] == -1 and hierarchy[0][c][3] > -1:
            stack[c] = 0
        else:
            stack[c] = 1

    ids = np.where(stack == 1)[0]
    group = np.array([], dtype=np.int32)
    if len(ids) > 0:
        contour_list = [contours[i] for i in ids]
        group = np.vstack(contour_list)

    return group


def _grayscale_to_rgb(img):
    """
    Convert a grayscale image to an RGB image.

    Inputs:
    img = Grayscale or RGB image data

    Returns:
    img = RGB image data

    :param img: np.ndarray
    :return img: np.ndarray
    """
    if len(np.shape(img)) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    return img


def _rgb2lab(rgb_img, channel):
    """Convert image from RGB colorspace to LAB colorspace. Returns the specified subchannel as a gray image.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        RGB image data
    channel : str
        color subchannel (l = lightness, a = green-magenta, b = blue-yellow)

    Returns
    -------
    numpy.ndarray
        grayscale image from one LAB color channel
    """
    # The allowable channel inputs are l, a or b
    channel = channel.lower()
    if channel not in ["l", "a", "b"]:
        fatal_error("Channel " + str(channel) + " is not l, a or b!")

    # Convert the input BGR image to LAB colorspace
    lab = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2LAB)
    # Split LAB channels
    l, a, b = cv2.split(lab)
    # Create a channel dictionaries for lookups by a channel name index
    channels = {"l": l, "a": a, "b": b}
    return channels[channel]


def _rgb2hsv(rgb_img, channel):
    """Convert image from RGB colorspace to HSV colorspace. Returns the specified subchannel as a gray image.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        RGB image data
    channel : str
        color subchannel (h = hue, s = saturation, v = value/intensity/brightness)

    Returns
    -------
    numpy.ndarray
        grayscale image from one HSV color channel
    """
    # The allowable channel inputs are h, s or v
    channel = channel.lower()
    if channel not in ["h", "s", "v"]:
        fatal_error("Channel " + str(channel) + " is not h, s or v!")

    # Convert the input BGR image to HSV colorspace
    hsv = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2HSV)
    # Split HSV channels
    h, s, v = cv2.split(hsv)
    # Create a channel dictionaries for lookups by a channel name index
    channels = {"h": h, "s": s, "v": v}

    return channels[channel]


def _rgb2cmyk(rgb_img, channel):
    """Convert image from RGB colorspace to CMYK colorspace. Returns the specified subchannel as a gray image.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        RGB image data
    channel : str
        color subchannel (c = cyan, m = magenta, y = yellow, k=black)

    Returns
    -------
    numpy.ndarray
        grayscale image from one CMYK color channel
    """
    # Set NumPy to ignore divide by zero errors
    _ = np.seterr(divide='ignore', invalid='ignore')
    # The allowable channel inputs are c, m , y or k
    channel = channel.lower()
    if channel not in ["c", "m", "y", "k"]:
        fatal_error("Channel " + str(channel) + " is not c, m, y or k!")

    # Create float
    bgr = rgb_img.astype(float)/255.

    # K channel
    k = 1 - np.max(bgr, axis=2)

    # C Channel
    c = (1 - bgr[..., 2] - k) / (1 - k)

    # M Channel
    m = (1 - bgr[..., 1] - k) / (1 - k)

    # Y Channel
    y = (1 - bgr[..., 0] - k) / (1 - k)

    # Convert the input BGR image to LAB colorspace
    cmyk = (np.dstack((c, m, y, k)) * 255).astype(np.uint8)
    # Split CMYK channels
    y, m, c, k = cv2.split(cmyk)
    # Create a channel dictionaries for lookups by a channel name index
    channels = {"c": c, "m": m, "y": y, "k": k}

    return channels[channel]


def _rgb2gray(rgb_img):
    """Convert image from RGB colorspace to Gray.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        RGB image data

    Returns
    -------
    numpy.ndarray
        grayscale image
    """
    gray = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)

    return gray


def _logical_operation(bin_img1, bin_img2, operation):
    """Perform a logical operation on two binary images.

    Parameters
    ----------
    bin_img1 : numpy.ndarray
        First binary image
    bin_img2 : numpy.ndarray
        Second binary image
    operation : str
        Logical operation to perform ('and', 'or', or 'xor')

    Returns
    -------
    numpy.ndarray
        Resulting binary image after the logical operation
    """
    # Dictionary of operations
    operations = {
        'and': cv2.bitwise_and,
        'or': cv2.bitwise_or,
        'xor': cv2.bitwise_xor
    }
    # Check if the operation is valid
    if operation.lower() not in operations:
        fatal_error(f"Operation '{operation}' is not supported. Use 'and', 'or', or 'xor'.")
    # Perform the logical operation
    mask = operations[operation.lower()](bin_img1, bin_img2)
    return mask


def _scale_size(value, trait_type="linear"):
    """Convert size measurements to known scale parameter

    Parameters
    ----------
    value : float, list
        unscaled size value(s)
    trait_type : str
        type of size measurement, either "linear" (default) or "area"

    Returns
    -------
    float, list
        scaled trait value(s)
    """
    # Set the linear conversion rate
    conversion_rate = params.px_width
    # Update conversion rate if trait is per unit ^ 2
    if trait_type == "area":
        conversion_rate = params.px_width * params.px_height
    # Simple multiplication for size scaling a single value
    if type(value) is not list:
        return value * conversion_rate
    # Multiplication with list comprehension for lists of values
    return [x*conversion_rate for x in value]


def _identity(x, **kwargs):
    """Identity function for use in _rect_filter
    This may be useful if there are several outputs from a function passed to _rect_filter
    which would otherwise be difficult to manage
    Parameters
    ----------
    x : any
      An object
    **kwargs
      Other keyword arguments, ignored.
    """
    return x


def _rect_filter(img, roi=None, function=None, **kwargs):
    """Subset a rectangular section of image to apply function to
    Parameters
    ----------
    img : numpy.ndarray
        An image
    roi : plantcv Objects class
        A rectangular ROI as returned by plantcv.roi.rectangle
    function : function
        analysis function to apply to each submask
    **kwargs
        Other keyword arguments to pass to the analysis function.
    Returns
    -------
    any
        Return value depends on the function that is called. If no function is called then this is a numpy.ndarray.
    """
    if roi is None:
        xstart = 0
        ystart = 0
        xend = np.shape(img)[1]
        yend = np.shape(img)[0]
    else:
        xstart = roi.contours[0][0][0][0][0].astype("int32")
        ystart = roi.contours[0][0][0][0][1].astype("int32")
        xend = roi.contours[0][0][2][0][0].astype("int32")
        yend = roi.contours[0][0][2][0][1].astype("int32")
    # slice image to subset rectangle
    sub_img = img[ystart:yend, xstart:xend]
    # apply function
    if function is None:
        function = _identity

    return function(sub_img, **kwargs)


def _rect_replace(img, sub_img, roi):
    """
    Parameters
    ----------
    img : numpy.ndarray
        Full sized image
    sub_img : numpy.ndarray
        output from _rect_filter
    roi : plantcv Objects class
        A rectangular ROI as returned by plantcv.roi.rectangle
    Returns
    -------
    numpy.ndarray
    """
    if roi is None:
        # if no ROI then no subsetting was done, just return sub_img
        return sub_img

    # if subsetting was done then get coordinates, slice into main image, and return
    xstart = roi.contours[0][0][0][0][0].astype("int32")
    ystart = roi.contours[0][0][0][0][1].astype("int32")
    xend = roi.contours[0][0][2][0][0].astype("int32")
    yend = roi.contours[0][0][2][0][1].astype("int32")
    full_img = np.copy(img)
    full_img[ystart:yend, xstart:xend] = sub_img
    return full_img
