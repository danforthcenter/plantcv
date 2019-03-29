# ROI functions

import os
import cv2
import numpy as np
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


# Create an ROI from a binary mask
def from_binary_image(img, bin_img):
    """Create an ROI from a binary image

    Inputs:
    img           = An RGB or grayscale image to plot the ROI on.
    bin_img       = Binary image to extract an ROI contour from.

    Outputs:
    roi_contour   = An ROI set of points (contour).
    roi_hierarchy = The hierarchy of ROI contour(s).

    :param img: numpy.ndarray
    :param bin_img: numpy.ndarray
    :return roi_contour: list
    :return roi_hierarchy: numpy.ndarray
    """
    # Autoincrement the device counter
    params.device += 1
    # Make sure the input bin_img is binary
    if len(np.unique(bin_img)) != 2:
        fatal_error("Input image is not binary!")
    # Use the binary image to create an ROI contour
    roi_contour, roi_hierarchy = cv2.findContours(np.copy(bin_img), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    # Draw the ROI if requested
    if params.debug is not None:
        _draw_roi(img=img, roi_contour=roi_contour)

    return roi_contour, roi_hierarchy


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
    roi_contour   = An ROI set of points (contour).
    roi_hierarchy = The hierarchy of ROI contour(s).

    :param img: numpy.ndarray
    :param x: int
    :param y: int
    :param h: int
    :param w: int
    :return roi_contour: list
    :return roi_hierarchy: numpy.ndarray
    """
    # Autoincrement the device counter
    params.device += 1

    # Get the height and width of the reference image
    height, width = np.shape(img)[:2]

    # Check whether the ROI is correctly bounded inside the image
    if x < 0 or y < 0 or x + w > width or y + h > height:
        fatal_error("The ROI extends outside of the image!")

    # Create the rectangle contour vertices
    pt1 = [x, y]
    pt2 = [x, y + h - 1]
    pt3 = [x + w - 1, y + h - 1]
    pt4 = [x + w - 1, y]

    # Create the ROI contour
    roi_contour = [np.array([[pt1], [pt2], [pt3], [pt4]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)

    # Draw the ROI if requested
    if params.debug is not None:
        _draw_roi(img=img, roi_contour=roi_contour)

    return roi_contour, roi_hierarchy


# Create a circular ROI
def circle(img, x, y, r):
    """Create a circular ROI.

    Inputs:
    img           = An RGB or grayscale image to plot the ROI on in debug mode.
    x             = The x-coordinate of the center of the circle.
    y             = The y-coordinate of the center of the circle.
    r             = The radius of the circle.

    Outputs:
    roi_contour   = An ROI set of points (contour).
    roi_hierarchy = The hierarchy of ROI contour(s).

    :param img: numpy.ndarray
    :param x: int
    :param y: int
    :param r: int
    :return roi_contour: list
    :return roi_hierarchy: numpy.ndarray
    """
    # Autoincrement the device counter
    params.device += 1

    # Get the height and width of the reference image
    height, width = np.shape(img)[:2]

    # Check whether the ROI is correctly bounded inside the image
    if x - r < 0 or x + r > width or y - r < 0 or y + r > height:
        fatal_error("The ROI extends outside of the image!")

    # Initialize a binary image of the circle
    bin_img = np.zeros((height, width), dtype=np.uint8)
    # Draw the circle on the binary image
    cv2.circle(bin_img, (x, y), r, 255, -1)

    # Use the binary image to create an ROI contour
    roi_contour, roi_hierarchy = cv2.findContours(np.copy(bin_img), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

    # Draw the ROI if requested
    if params.debug is not None:
        _draw_roi(img=img, roi_contour=roi_contour)

    return roi_contour, roi_hierarchy


# Create an elliptical ROI
def ellipse(img, x, y, r1, r2, angle):
    """Create an elliptical ROI.

    Inputs:
    img           = An RGB or grayscale image to plot the ROI on in debug mode.
    x             = The x-coordinate of the center of the ellipse.
    y             = The y-coordinate of the center of the ellipse.
    r1            = The radius of the major axis.
    r2            = The radius of the minor axis.
    angle         = The angle of rotation in degrees of the major axis.

    Outputs:
    roi_contour   = An ROI set of points (contour).
    roi_hierarchy = The hierarchy of ROI contour(s).

    :param img: numpy.ndarray
    :param x: int
    :param y: int
    :param r1: int
    :param r2: int
    :param angle: double
    :return roi_contour: list
    :return roi_hierarchy: numpy.ndarray
    """
    # Autoincrement the device counter
    params.device += 1

    # Get the height and width of the reference image
    height, width = np.shape(img)[:2]

    # Initialize a binary image of the ellipse
    bin_img = np.zeros((height, width), dtype=np.uint8)
    # Draw the ellipse on the binary image
    cv2.ellipse(bin_img, (x, y), (r1, r2), angle, 0, 360, 255, -1)

    if np.sum(bin_img[0, :]) + np.sum(bin_img[-1, :]) + np.sum(bin_img[:, 0]) + np.sum(bin_img[:, -1]) > 0:
        fatal_error("The ROI extends outside of the image!")

    # Use the binary image to create an ROI contour
    roi_contour, roi_hierarchy = cv2.findContours(np.copy(bin_img), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

    # Draw the ROI if requested
    if params.debug is not None:
        _draw_roi(img=img, roi_contour=roi_contour)

    return roi_contour, roi_hierarchy


# Draw the ROI on a reference image
def _draw_roi(img, roi_contour):
    """Draw an ROI

    :param img: numpy.ndarray
    :param roi_contour: list
    """
    # Make a copy of the reference image
    ref_img = np.copy(img)
    # If the reference image is grayscale convert it to color
    if len(np.shape(ref_img)) == 2:
        ref_img = cv2.cvtColor(ref_img, cv2.COLOR_GRAY2BGR)
    # Draw the contour on the reference image
    cv2.drawContours(ref_img, roi_contour, -1, (255, 0, 0), params.line_thickness)
    if params.debug == "print":
        # If debug is print, save the image to a file
        print_image(ref_img, os.path.join(params.debug_outdir, str(params.device) + "_roi.png"))
    elif params.debug == "plot":
        # If debug is plot, print to the plotting device
        plot_image(ref_img)


def multi(img, coord, radius, spacing=None, nrows=None, ncols=None):
    """Create multiple circular ROIs on a single image
    Inputs
    img            = Input image data.
    coord          = Two-element tuple of the center of the top left object (x,y) or a list of tuples identifying the center of each roi [(x1,y1),(x2,y2)]
    radius         = A single radius for all ROIs.
    spacing        = Two-element tuple of the horizontal and vertical spacing between ROIs, (x,y). Ignored if `coord` is a list and `rows` and `cols` are None.
    nrows          = Number of rows in ROI layout. Should be missing or None if each center coordinate pair is listed.
    ncols          = Number of columns in ROI layout. Should be missing or None if each center coordinate pair is listed.

    Returns:
    roi_contour           = list of roi contours
    roi_hierarchy         = list of roi hierarchies

    :param img: numpy.ndarray
    :param coord: tuple, list
    :param radius: int
    :param spacing: tuple
    :param nrows: int
    :param ncols: int
    :return mask: numpy.ndarray
    """

    # Autoincrement the device counter
    params.device += 1

    # Initialize ROI list
    rois = []

    # Store user debug
    debug = params.debug

    # Temporarily disable debug
    params.debug = None

    # Get the height and width of the reference image
    height, width = np.shape(img)[:2]

    # Initialize a binary image of the circle
    bin_img = np.zeros((height, width), dtype=np.uint8)
    roi_contour = []
    roi_hierarchy = []
    # Grid of ROIs
    if (type(coord) == tuple) and ((nrows and ncols) is not None):
        # Loop over each row
        for i in range(0, nrows):
            # The upper left corner is the y starting coordinate + the ROI offset * the vertical spacing
            y = coord[1] + i * spacing[1]
            # Loop over each column
            for j in range(0, ncols):
                # The upper left corner is the x starting coordinate + the ROI offset * the
                # horizontal spacing between chips
                x = coord[0] + j * spacing[0]
                # Create a chip ROI
                rois.append(circle(img=img, x=x, y=y, r=radius))
                # Draw the circle on the binary image
                cv2.circle(bin_img, (x, y), radius, 255, -1)
                # Make a list of contours and hierarchies
                roi_contour.append(cv2.findContours(np.copy(bin_img), cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_NONE)[-2:][0])
                roi_hierarchy.append(cv2.findContours(np.copy(bin_img), cv2.RETR_EXTERNAL,
                                                      cv2.CHAIN_APPROX_NONE)[-2:][1])
                # Create an array of contours and list of hierarchy for when debug is set to 'plot'
                roi_contour1, roi_hierarchy1 = cv2.findContours(np.copy(bin_img), cv2.RETR_TREE,
                                                                cv2.CHAIN_APPROX_NONE)[-2:]

    # User specified ROI centers
    elif (type(coord) == list) and ((nrows and ncols) is None):
        for i in range(0, len(coord)):
            y = coord[i][1]
            x = coord[i][0]
            rois.append(circle(img=img, x=x, y=y, r=radius))
            # Draw the circle on the binary image
            cv2.circle(bin_img, (x, y), radius, 255, -1)
            #  Make a list of contours and hierarchies
            roi_contour.append(cv2.findContours(np.copy(bin_img), cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_NONE)[-2:][0])
            roi_hierarchy.append(cv2.findContours(np.copy(bin_img), cv2.RETR_EXTERNAL,
                                                  cv2.CHAIN_APPROX_NONE)[-2:][1])
            # Create an array of contours and list of hierarchy for when debug is set to 'plot'
            roi_contour1, roi_hierarchy1 = cv2.findContours(np.copy(bin_img), cv2.RETR_TREE,
                                                            cv2.CHAIN_APPROX_NONE)[-2:]

    else:
        fatal_error("Function can either make a grid of ROIs (user must provide nrows, ncols, spacing, and coord) "
                    "or take custom ROI coordinates (user must provide a list of tuples to 'coord' parameter)")
    # Reset debug
    params.debug = debug

    # Draw the ROIs if requested
    if params.debug is not None:
        _draw_roi(img=img, roi_contour=roi_contour1)

    return roi_contour, roi_hierarchy
