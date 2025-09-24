# ROI functions

import os
import cv2
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
from skimage.measure import label
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import color_palette
from plantcv.plantcv._helpers import _cv2_findcontours
from plantcv.plantcv._helpers import _roi_filter
from plantcv.plantcv._helpers import _hough_circle
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from plantcv.plantcv import fatal_error, warn, params, Objects


# Create an ROI from a binary mask
def from_binary_image(img, bin_img):
    """Create an ROI from a binary image

    Inputs:
    img           = An RGB or grayscale image to plot the ROI on.
    bin_img       = Binary image to extract an ROI contour from.

    Outputs:
    roi

    :param img: numpy.ndarray
    :param bin_img: numpy.ndarray
    :return roi: plantcv.plantcv.classes.Objects
    """
    # Make sure the input bin_img is binary
    if len(np.unique(bin_img)) != 2:
        fatal_error("Input image is not binary!")
    # Use the binary image to create an ROI contour
    roi_contour, roi_hierarchy = _cv2_findcontours(bin_img=bin_img)
    roi = Objects(contours=[roi_contour], hierarchy=[roi_hierarchy])
    # Draw the ROI if requested
    _draw_roi(img=img, roi_contour=roi)

    return roi


# Create a rectangular ROI
def rectangle(img, x, y, h, w):
    """Create a rectangular ROI.

    Inputs:
    img           = An RGB or grayscale image to plot the ROI on in debug mode.
    x             = The x-coordinate of the upper left corner of the rectangle.
    y             = The y-coordinate of the upper left corner of the rectangle.
    h             = The height of the rectangle.
    w             = The width of the rectangle.

    Outputs:
    roi

    :param img: numpy.ndarray
    :param x: int
    :param y: int
    :param h: int
    :param w: int
    :return roi: plantcv.plantcv.classes.Objects
    """
    # Get the height and width of the reference image
    height, width = np.shape(img)[:2]

    # Create the rectangle contour vertices
    pt1 = [x, y]
    pt2 = [x, y + h - 1]
    pt3 = [x + w - 1, y + h - 1]
    pt4 = [x + w - 1, y]

    # Create the ROI contour
    roi_contour = [np.array([[pt1], [pt2], [pt3], [pt4]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_contour], hierarchy=[roi_hierarchy])

    # Draw the ROI if requested
    _draw_roi(img=img, roi_contour=roi)

    # Check whether the ROI is correctly bounded inside the image
    if x < 0 or y < 0 or x + w > width or y + h > height:
        fatal_error("The ROI extends outside of the image!")

    return roi


# Create a circular ROI
def circle(img, x, y, r):
    """Create a circular ROI.

    Inputs:
    img           = An RGB or grayscale image to plot the ROI on in debug mode.
    x             = The x-coordinate of the center of the circle.
    y             = The y-coordinate of the center of the circle.
    r             = The radius of the circle.

    Outputs:
    roi           = A dataclass with the roi object and hierarchy.

    :param img: numpy.ndarray
    :param x: int
    :param y: int
    :param r: int
    :return roi: plantcv.plantcv.classes.Objects
    """
    # Get the height and width of the reference image
    height, width = np.shape(img)[:2]

    # Initialize a binary image of the circle
    bin_img = np.zeros((height, width), dtype=np.uint8)
    # Draw the circle on the binary image
    cv2.circle(bin_img, (x, y), r, 255, -1)

    # Use the binary image to create an ROI contour
    roi_contour, roi_hierarchy = _cv2_findcontours(bin_img=bin_img)
    roi = Objects(contours=[roi_contour], hierarchy=[roi_hierarchy])

    # Draw the ROI if requested
    _draw_roi(img=img, roi_contour=roi)

    # Check whether the ROI is correctly bounded inside the image
    if x - r < 0 or x + r > width or y - r < 0 or y + r > height:
        fatal_error("The ROI extends outside of the image!")

    return roi


# Create an elliptical ROI
def ellipse(img, x, y, r1, r2, angle):
    """Create an elliptical ROI.

    Inputs:
    img           = An RGB or grayscale image to plot the ROI on in debug mode.
    x             = The x-coordinate of the center of the ellipse.
    y             = The y-coordinate of the center of the ellipse.
    r1            = The radius of the minor axis.
    r2            = The radius of the major axis.
    angle         = The angle of rotation in degrees of the major axis.

    Outputs:
    roi           = a dataclass with the roi object and hierarchy

    :param img: numpy.ndarray
    :param x: int
    :param y: int
    :param r1: int
    :param r2: int
    :param angle: double
    :return roi: plantcv.plantcv.classes.Objects
    """
    # Get the height and width of the reference image
    height, width = np.shape(img)[:2]

    # Initialize a binary image of the ellipse
    bin_img = np.zeros((height, width), dtype=np.uint8)
    # Draw the ellipse on the binary image
    cv2.ellipse(bin_img, (x, y), (r1, r2), angle, 0, 360, 255, -1)

    # Use the binary image to create an ROI contour
    roi_contour, roi_hierarchy = _cv2_findcontours(bin_img=bin_img)
    roi = Objects(contours=[roi_contour], hierarchy=[roi_hierarchy])

    # Draw the ROI if requested
    _draw_roi(img=img, roi_contour=roi)

    # Checks ellipse goes outside the image by checking row and column sum of edges
    if (np.sum(bin_img[0, :]) + np.sum(bin_img[-1, :]) + np.sum(bin_img[:, 0]) + np.sum(bin_img[:, -1]) > 0) or \
            len(roi_contour) == 0:
        fatal_error("The ROI extends outside of the image, or ROI is not on the image!")

    return roi


# Draw the ROI on a reference image
def _draw_roi(img, roi_contour):
    """Draw an ROI

    Parameters
    ----------
    img : numpy.ndarray
        An RGB or grayscale image to plot the ROI on in debug mode.
    roi_contour : list
        A list of contours and hierarchies for the ROI.
    """
    # Make a copy of the reference image
    ref_img = np.copy(img)
    # If the reference image is grayscale convert it to color
    if len(np.shape(ref_img)) == 2:
        ref_img = cv2.cvtColor(ref_img, cv2.COLOR_GRAY2BGR)
    # Collect coordinates for debug numbering
    rand_color = color_palette(num=len(roi_contour.contours),
                               saved=False) if len(roi_contour.contours) > 1 else [params.line_color]
    label_coords = []
    for i, cnt in enumerate(roi_contour):
        M = cv2.moments(cnt.contours[0][0])
        if M['m00'] != 0:
            cxy = [int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])]
            label_coords.append(cxy)
            # Add number labels to debug
            cv2.putText(img=ref_img, text=f"{i+1}", org=(label_coords[i]),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=params.text_size, color=rand_color[i],
                        thickness=params.text_thickness)
        # Draw ROI outline regardless
        cv2.drawContours(ref_img, cnt.contours[0], -1, rand_color[i], params.line_thickness)

    _debug(visual=ref_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_roi.png"))


def _calculate_grid(mask, nrows, ncols):
    """Calculate the grid layout of ROIs

    Parameters
    ----------
    mask : numpy.ndarray
        A binary mask
    nrows : int
        Number of rows in ROI layout
    ncols : int
        Number of columns in ROI layout

    Returns
    -------
    tuple, tuple
        Two-element tuple of the center of the top left object (x,y) and Two-element tuple of the horizontal and vertical
        spacing between ROIs, (x,y)
    """
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    centers = []
    for c in contours:
        m = cv2.moments(c)
        if m['m00'] != 0:
            cmx, cmy = (float(m['m10'] / m['m00']), float(m['m01'] / m['m00']))
            centers.append((cmx, cmy))
    # cluster by x and y coordinates to get grid layout
    centers_x = np.array(np.array([i[0] for i in centers]).reshape(-1, 1))
    centers_y = np.array(np.array([i[1] for i in centers]).reshape(-1, 1))
    gm_x = GaussianMixture(n_components=ncols, random_state=0).fit(centers_x)
    gm_y = GaussianMixture(n_components=nrows, random_state=0).fit(centers_y)
    clusters_x = np.sort(gm_x.means_[:, 0])
    clusters_y = np.sort(gm_y.means_[:, 0])
    spacing_x = (clusters_x[ncols-1] - clusters_x[0])/(ncols-1) if ncols > 1 else 0
    spacing_y = (clusters_y[nrows-1] - clusters_y[0])/(nrows-1) if nrows > 1 else 0
    spacing = (round(spacing_x), round(spacing_y))
    coord = (round(clusters_x[0]), round(clusters_y[0]))
    return coord, spacing


def _adjust_radius_coord(height, width, coord, radius):
    """Adjust the radius of the ROI

    Parameters
    ----------
    height : int
        Height of the image
    width : int
        Width of the image
    coord : list
        List of tuples identifying the center of each roi [(x1,y1),(x2,y2)]
    radius : int
        Radius of the ROI

    Returns
    -------
    int
        Adjusted radius
    """
    x = [i[0] for i in coord]
    y = [i[1] for i in coord]
    return _adjust_radius_max_min(height, width, radius, max(x), min(x), max(y), min(y))


def _adjust_radius_grid(height, width, coord, radius, spacing, nrows, ncols):
    """Adjust the radius of the ROI

    Parameters
    ----------
    height : int
        Height of the image
    width : int
        Width of the image
    coord : tuple
        Two-element tuple of the center of the top left object (x,y)
    radius : int
        Radius of the ROI
    spacing : tuple
        Two-element tuple of the horizontal and vertical spacing between ROIs, (x,y)
    nrows : int
        Number of rows in ROI layout
    ncols : int
        Number of columns in ROI layout

    Returns
    -------
    int
        Adjusted radius
    """
    xmax = coord[0] + (ncols-1)*spacing[0]
    xmin = coord[0]
    ymax = coord[1] + (nrows-1)*spacing[1]
    ymin = coord[1]
    return _adjust_radius_max_min(height, width, radius, xmax, xmin, ymax, ymin)


def _adjust_radius_max_min(height, width, radius, xmax, xmin, ymax, ymin):
    """Adjust the radius of the ROI

    Parameters
    ----------
    height : int
        Height of the image
    width : int
        Width of the image
    radius : int
        Radius of the ROI
    xmax : int
        Maximum x coordinate of the ROI
    xmin : int
        Minimum x coordinate of the ROI
    ymax : int
        Maximum y coordinate of the ROI
    ymin : int
        Minimum y coordinate of the ROI

    Returns
    -------
    int
        Adjusted radius
    """
    if ((xmin < 0) or (xmax > width) or (ymin < 0) or (ymax > height)):
        fatal_error("An ROI extends outside of the image!")
    distances_to_edge = [xmin, width-xmax, ymin, height-ymax]
    min_distance = min(distances_to_edge)
    if min_distance < radius:
        warn('Shrinking radius to make ROIs fit in the image')
        radius = min_distance - 1
    return radius


def _rois_from_coordinates(img, coord=None, radius=None):
    """Create multiple circular ROIs on a single image from a list of coordinates

    Parameters
    ----------
    img : numpy.ndarray
        Input image data
    coord : list, optional
        List of tuples identifying the center of each roi [(x1,y1),(x2,y2)], by default None
    radius : int, optional
        A single radius for all ROIs, by default None

    Returns
    -------
    plantcv.plantcv.classes.Objects, numpy.ndarray
        A dataclass with roi objects and hierarchies, A binary image with overlapping ROIs
    """
    if radius is None:
        fatal_error("Specify a radius if creating rois from a list of coordinates")
    # Get the height and width of the reference image
    height, width = np.shape(img)[:2]
    radius = _adjust_radius_coord(height, width, coord, radius)
    overlap_img = np.zeros((height, width), dtype=np.uint8)
    roi_objects = Objects()
    for i in range(0, len(coord)):
        # Initialize a binary image for each circle
        bin_img = np.zeros((height, width), dtype=np.uint8)
        y = int(coord[i][1])
        x = int(coord[i][0])
        # Draw the circle on the binary image
        # Keep track of each roi individually to check overlapping
        circle_img = cv2.circle(bin_img, (x, y), radius, 255, -1)
        overlap_img = cv2.circle(overlap_img, (x, y), radius, 255, -1)
        # Make a list of contours and hierarchies
        rc, rh = cv2.findContours(circle_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]
        roi_objects.append(rc, rh)
    return roi_objects, overlap_img


def _rect_rois_from_coordinates(img, h, w, coord=None):
    """Create multiple circular ROIs on a single image from a list of coordinates

    Parameters
    ----------
    img : numpy.ndarray
        Input image data
    coord : list, optional
        List of tuples identifying the center of each roi [(x1,y1),(x2,y2)], by default None
    h : int
        Height of rectangular ROIs
    w : int
        Width of rectangular ROIs

    Returns
    -------
    plantcv.plantcv.classes.Objects, numpy.ndarray
        A dataclass with roi objects and hierarchies, A binary image with overlapping ROIs
    """
    # Get the height and width of the reference image
    height, width = np.shape(img)[:2]
    overlap_img = np.zeros((height, width), dtype=np.uint8)
    roi_objects = Objects()
    for i in range(0, len(coord)):
        y = int(coord[i][1])
        x = int(coord[i][0])
        # find corners of rectangle
        pt1 = [x, y]
        pt2 = [x, y + h - 1]
        pt3 = [x + w - 1, y + h - 1]
        pt4 = [x + w - 1, y]
        # Make a list of contours and hierarchies
        rc = [np.array([[pt1], [pt2], [pt3], [pt4]], dtype=np.int32)]
        rh = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
        # Keep track of each roi individually to check overlapping
        overlap_img = cv2.drawContours(overlap_img, rc, -1, 255, -1)
        roi_objects.append(rc, rh)
    return roi_objects, overlap_img


def _grid_roi(img, nrows, ncols, coord=None, radius=None, spacing=None):
    """Create a grid of ROIs

    Parameters
    ----------
    img : numpy.ndarray
        Input image data
    nrows : int
        Number of rows in ROI layout
    ncols : int
        Number of columns in ROI layout
    coord : tuple, optional
        Two-element tuple of the center of the top left object (x,y), by default None
    radius : int, optional
        Optional parameter to specify the radius of the circular rois, by default None
    spacing : tuple, optional
        Two-element tuple of the horizontal and vertical spacing between ROIs, (x,y), by default None

    Returns
    -------
    plantcv.plantcv.classes.Objects, numpy.ndarray
        A dataclass with roi objects and hierarchies, A binary image with overlapping ROIs
    """
    if radius is None:
        RADIUS_RATIO = 0.325
        if spacing[0] == 0:
            radius = round(RADIUS_RATIO*spacing[1])
        elif spacing[1] == 0:
            radius = round(RADIUS_RATIO*spacing[0])
        else:
            radius = round(RADIUS_RATIO*(spacing[0]+spacing[1])/2)
    # Get the height and width of the reference image
    height, width = np.shape(img)[:2]
    radius = _adjust_radius_grid(height, width, coord, radius, spacing, nrows, ncols)
    overlap_img = np.zeros((height, width), dtype=np.uint8)
    roi_objects = Objects()
    # Loop over each row
    for i in range(0, nrows):
        # The upper left corner is the y starting coordinate + the ROI offset * the vertical spacing
        y = coord[1] + i * spacing[1]
        # Loop over each column
        for j in range(0, ncols):
            # Initialize a binary image for each circle
            bin_img = np.zeros((height, width), dtype=np.uint8)
            # The upper left corner is the x starting coordinate + the ROI offset * the
            # horizontal spacing between chips
            x = coord[0] + j * spacing[0]
            # Draw the circle on the binary images
            # Keep track of each roi individually to check overlapping
            circle_img = cv2.circle(bin_img, (x, y), radius, 255, -1)
            # Draw the circle on the overall mask
            overlap_img = cv2.circle(overlap_img, (x, y), radius, 255, -1)
            # Make a list of contours and hierarchies
            rc, rh = cv2.findContours(circle_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]
            roi_objects.append(rc, rh)
    return roi_objects, overlap_img


def _grid_roi_rect(img, nrows, ncols, h, w, coord=None, spacing=None):
    """Create a grid of rectangular ROIs

    Parameters
    ----------
    img : numpy.ndarray
        Input image data
    nrows : int
        Number of rows in ROI layout
    ncols : int
        Number of columns in ROI layout
    coord : tuple, optional
        Two-element tuple of the center of the top left object (x,y), by default None
    h : int
        Height of each rectangle
    w : int
        Width of each rectangle
    spacing : tuple, optional
        Two-element tuple of the horizontal and vertical spacing between ROIs, (x,y), by default None

    Returns
    -------
    plantcv.plantcv.classes.Objects, numpy.ndarray
        A dataclass with roi objects and hierarchies, A binary image with overlapping ROIs
    """
    # Get the height and width of the reference image
    height, width = np.shape(img)[:2]
    overlap_img = np.zeros((height, width), dtype=np.uint8)
    roi_objects = Objects()
    # Loop over each row
    for i in range(0, nrows):
        # The upper left corner is the y starting coordinate + the ROI offset * the vertical spacing
        y = coord[1] + i * spacing[1]
        # Loop over each column
        for j in range(0, ncols):
            # The upper left corner is the x starting coordinate + the ROI offset * the
            # horizontal spacing between chips
            x = coord[0] + j * spacing[0]
            # calculate corners
            pt1 = [x, y]
            pt2 = [x, y + h - 1]
            pt3 = [x + w - 1, y + h - 1]
            pt4 = [x + w - 1, y]
            # Create the ROI contours and hierarchy
            rc = [np.array([[pt1], [pt2], [pt3], [pt4]], dtype=np.int32)]
            rh = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
            # Draw the rectangle on the overall mask
            overlap_img = cv2.drawContours(overlap_img, rc, -1, 255, -1)
            roi_objects.append(rc, rh)
    return roi_objects, overlap_img


def auto_grid(mask, nrows, ncols, radius=None, img=None):
    """Detect and create multiple circular ROIs on a single binary mask
    Inputs
    mask          = A binary mask.
    nrows         = Number of rows in ROI layout.
    ncols         = Number of columns in ROI layout.
    radius        = Optional parameter to specify the radius of the circular rois.
    img           = (Optional) Image from which the binary mask was created.

    Returns:
    roi_objects   = a dataclass with roi objects and hierarchies

    :param mask: numpy.ndarray
    :param nrows: int
    :param ncols: int
    :param radius: int
    :param img: numpy.ndarray
    :return roi_objects: plantcv.plantcv.classes.Objects
    """
    # Make sure the input bin_img is binary
    if len(np.unique(mask)) != 2:
        fatal_error("Input binary mask is not binary!")
    coord, spacing = _calculate_grid(mask, nrows, ncols)
    if img is None:
        img = mask
    roi_objects, overlap_img = _grid_roi(img, nrows, ncols, coord, radius, spacing)
    # Label the ROIs to check for overlap
    _, num_labels = label(overlap_img, return_num=True)
    # Check for overlapping ROIs where the number of labels is not equal to the number of expected ROIs
    if num_labels != nrows * ncols:
        warn("Two or more of the user defined regions of interest overlap! "
             "If you only see one ROI then they may overlap exactly.")
    # Draw the ROIs if requested
    # Create an array of contours and list of hierarchy for debug image
    _draw_roi(img=img, roi_contour=roi_objects)
    return roi_objects


def multi(img, coord, radius=None, spacing=None, nrows=None, ncols=None):
    """Create multiple circular ROIs on a single image

    Inputs
    img           = Input image data.
    coord         = Two-element tuple of the center of the top left object (x,y) or a list of tuples identifying
                    the center of each roi [(x1,y1),(x2,y2)]
    radius        = A single radius for all ROIs.
    spacing       = Two-element tuple of the horizontal and vertical spacing between ROIs, (x,y). Ignored if `coord`
                    is a list and `rows` and `cols` are None.
    nrows         = Number of rows in ROI layout. Should be missing or None if each center coordinate pair is listed.
    ncols         = Number of columns in ROI layout. Should be missing or None if each center coordinate pair is listed.

    Returns
    roi_objects   = a dataclass with roi objects and hierarchies

    :param img: numpy.ndarray
    :param coord: tuple, list
    :param radius: int
    :param spacing: tuple
    :param nrows: int
    :param ncols: int
    :return roi_objects: plantcv.plantcv.classes.Objects
    """
    # Grid of ROIs
    num_rois = 0
    if (isinstance(coord, tuple)) and ((nrows and ncols) is not None) and (isinstance(spacing, tuple)):
        roi_objects, overlap_img = _grid_roi(img, nrows, ncols, coord, radius, spacing)
        # The number of ROIs is the product of the number of rows and columns
        num_rois = nrows * ncols
    # User specified ROI centers
    elif (isinstance(coord, list)) and ((nrows and ncols) is None) and (spacing is None):
        roi_objects, overlap_img = _rois_from_coordinates(img=img, coord=coord, radius=radius)
        # The number of ROIs is the length of the list of coordinates
        num_rois = len(coord)
    else:
        fatal_error("Function can either make a grid of ROIs (user must provide nrows, ncols, spacing, and coord) "
                    "or take custom ROI coordinates (user must provide only a list of tuples to 'coord' parameter). "
                    "For automatic detection of a grid layout from just nrows, ncols, and a binary mask, use auto_grid")

    # Label the ROIs to check for overlap
    _, num_labels = label(overlap_img, return_num=True)
    # Check for overlapping ROIs where the number of labels is not equal to the number of expected ROIs
    if num_labels != num_rois:
        warn("Two or more of the user defined regions of interest overlap! "
             "If you only see one ROI then they may overlap exactly.")

    # Draw the ROIs if requested
    _draw_roi(img=img, roi_contour=roi_objects)
    return roi_objects


def multi_rect(img, coord, h=None, w=None, spacing=None, nrows=None, ncols=None):
    """Create multiple rectangular ROIs on a single image

    Parameters
    ----------
    img : numpy.ndarray
        Input image data.
    coord : tuple, list
        Two-element tuple of the center of the top left object (x,y) or a list of tuples identifying
        the top left corner of each roi [(x1,y1),(x2,y2), ...]
    h : int, optional
        The height of each rectangular ROI, by default None
    w : int, optional
        The width of each rectangular ROI, by default None
    spacing : tuple, optional
        Two-element tuple of the horizontal and vertical spacing between ROIs, (x,y). Ignored if `coord`
        is a list and `rows` and `cols` are None.
    nrows : int, optional
        Number of rows in ROI layout. Should be missing or None if each center coordinate pair is listed.
    ncols : int, optional
        Number of columns in ROI layout. Should be missing or None if each center coordinate pair is listed.

    Returns
    -------
    plantcv.plantcv.classes.Objects
        A dataclass with roi objects and hierarchies
    """
    # Grid of ROIs
    num_rois = 0
    if (isinstance(coord, tuple)) and ((nrows and ncols) is not None) and (isinstance(spacing, tuple)):
        roi_objects, overlap_img = _grid_roi_rect(img, nrows, ncols, h, w, coord, spacing)
        # The number of ROIs is the product of the number of rows and columns
        num_rois = nrows * ncols
    # User specified ROI centers
    elif (isinstance(coord, list)) and ((nrows and ncols) is None) and (spacing is None):
        roi_objects, overlap_img = _rect_rois_from_coordinates(img=img, h=h, w=w, coord=coord)
        # The number of ROIs is the length of the list of coordinates
        num_rois = len(coord)
    else:
        fatal_error("Function can either make a grid of ROIs (user must provide nrows, ncols, spacing, and coord) "
                    "or take custom ROI coordinates (user must provide only a list of tuples to 'coord' parameter). "
                    "For automatic detection of a grid layout from just nrows, ncols, and a binary mask, use auto_grid")

    # Label the ROIs to check for overlap
    _, num_labels = label(overlap_img, return_num=True)
    # Check for overlapping ROIs where the number of labels is not equal to the number of expected ROIs
    if num_labels != num_rois:
        warn("Two or more of the user defined regions of interest overlap! "
             "If you only see one ROI then they may overlap exactly.")

    # Draw the ROIs if requested
    _draw_roi(img=img, roi_contour=roi_objects)
    return roi_objects


def auto_wells(gray_img, mindist, candec, accthresh, minradius, maxradius, nrows, ncols, radiusadjust=None, roi=None):
    """Hough Circle Well Detection.

    Keyword inputs:
    gray_img = gray image (np.ndarray)
    mindist = minimum distance between detected circles
    candec = higher threshold of canny edge detector
    accthresh = accumulator threshold for the circle centers
    minradius = minimum circle radius
    maxradius = maximum circle radius
    nrows = expected number of rows
    ncols = expected number of columns
    radiusadjust = amount to adjust the average radius, this can be desirable
    if you want ROI to sit inside a well, for example (in that case you might
    set it to a negative value).
    roi = optional rectangular ROI to find wells within.

    :param gray_img: np.ndarray
    :param mindist: int
    :param candec: int
    :param accthresh: int
    :param minradius: int
    :param maxradius: int
    :param nrows = int
    :param ncols = int
    :param roi = plantcv.plantcv.classes.Objects
    :return roi: plantcv.plantcv.classes.Objects
    """
    # Use hough circle helper function
    maxfind = nrows * ncols
    df, sub_img = _rect_filter(gray_img, roi, _hough_circle,
                               **{"mindist": mindist, "candec": candec,
                                  "accthresh": accthresh, "minradius": minradius,
                                  "maxradius": maxradius, "maxfound": maxfind})
    # cast gray image to color
    cimg = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
    # slice ROI back into original image
    img = _rect_replace(cimg, sub_img, roi)
    # adjust data.frame x/y points to match full scale image if ROI was used
    if roi is not None:
        xstart = roi.contours[0][0][0][0][0].astype("int32")
        ystart = roi.contours[0][0][0][0][1].astype("int32")
        df['x'] = df['x'] + xstart
        df['y'] = df['y'] + ystart

    _debug(img, filename=os.path.join(params.debug_outdir, str(params.device) + '_roi_houghcircle.png'), cmap='gray')

    xlist = []
    centers_x = df['x'].values.reshape(-1, 1)
    centers_y = df['y'].values.reshape(-1, 1)
    gm_x = GaussianMixture(n_components=ncols, random_state=0).fit(centers_x)
    gm_y = GaussianMixture(n_components=nrows, random_state=0).fit(centers_y)
    clusters_x = gm_x.means_[:, 0]
    clusters_y = gm_y.means_[:, 0]

    sorted_indicesx = np.argsort(clusters_x)
    sorted_x = np.sort(clusters_x)
    xlist = list(range(len(clusters_x)))
    clusterxdf = {'clusters_x': sorted_x, 'sorted': sorted_indicesx,
                  'xindex': [0]*len(clusters_x)}
    xdf = pd.DataFrame(clusterxdf)
    xdf = xdf.sort_values(by='clusters_x', ascending=True)
    xdf['xindex'] = xlist

    sorted_indicesy = np.argsort(clusters_y)
    sorted_y = np.sort(clusters_y)
    ylist = list(range(len(clusters_y)))
    clusterydf = {'clusters_y': sorted_y, 'sorted': sorted_indicesy,
                  'yindex': [0]*len(clusters_y)}
    ydf = pd.DataFrame(clusterydf)
    ydf = ydf.sort_values(by='clusters_y', ascending=True)
    ydf['yindex'] = ylist

    df['column'] = gm_x.predict(centers_x)
    df['row'] = gm_y.predict(centers_y)

    df['row'] = df['row'].replace(list(ydf['sorted']), list(ydf['yindex']))
    df['column'] = df['column'].replace(list(xdf['sorted']), list(xdf['xindex']))

    df = df.sort_values(by=['row', 'column'], ascending=[True, True])
    df['xy'] = list(zip(df.x, df.y))

    radiusfinal = int(np.mean(list(df['radius'])))+radiusadjust

    rois = multi(gray_img, list(df['xy']), radius=radiusfinal)

    return rois


def custom(img, vertices):
    """Create an custom polygon ROI.

    Inputs:
    img = An RGB or grayscale image to plot the ROI on in debug mode.
    vertices = List of vertices of the desired polygon ROI

    Outputs:
    roi = a dataclass with the roi object and hierarchy

    :param img: numpy.ndarray
    :param vertices: list
    :return roi: plantcv.plantcv.classes.Objects
    """
    # Get the height and width of the reference image
    height, width = np.shape(img)[:2]

    # Check that the ROI doesn't go off the screen
    for i in vertices:
        (x, y) = i
        if x < 0 or x > width or y < 0 or y > height:
            fatal_error("An ROI extends outside of the image!")

    roi_contour = [np.array(vertices, dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    roi = Objects(contours=[roi_contour], hierarchy=[roi_hierarchy])

    # Draw the ROIs if requested
    _draw_roi(img=img, roi_contour=roi)

    return roi


# Filter a mask based on a region of interest
def filter(mask, roi, roi_type="partial"):
    """
    Filter a mask using a region of interest.

    Connected regions of non-zero pixels outside the ROI are set to zero.

    Parameters
    ----------
    mask : numpy.ndarray
        Binary image data to be filtered.
    roi : plantcv.plantcv.classes.Objects
        Region of interest, an instance of the Object class output from a ROI function.
    roi_type : str, optional
        Type of ROI filtering: 'cutto', 'partial' (default, for partially inside),
        'largest' (keep only the largest contour), or 'within'.

    Returns
    -------
    filtered_mask : numpy.ndarray
        Mask image after ROI filtering.
    """
    found_obj, found_hier = _cv2_findcontours(bin_img=mask)

    _, _, filtered_mask = _roi_filter(img=mask, roi=roi, obj=found_obj,
                                      hierarchy=found_hier, roi_type=roi_type)

    _debug(filtered_mask, filename=os.path.join(params.debug_outdir, str(params.device) + '_roi_filter.png'), cmap='gray')

    return filtered_mask
