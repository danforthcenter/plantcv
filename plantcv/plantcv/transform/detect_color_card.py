"""Automatically detect color cards.

Algorithm written by mtwatso2-eng (github). Updated and implemented into PlantCV by Haley Schuhl.
"""
import os
import cv2
import math
import numpy as np
from plantcv.plantcv import params, outputs, fatal_error, deprecation_warning
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rgb2gray, _rgb2hsv, _cv2_findcontours, _object_composition


def _is_square(contour, min_size, aspect_ratio=1.27, solidity=.8):
    """Determine if a contour is square or not.

    Parameters
    ----------
    contour : list
        OpenCV contour.
    min_size : int
        Minimum object size to be considered
    aspect_ratio : float
         below a given aspect ratio
    solidity : float
        Filter contours below a given solidity

    Returns
    -------
    bool
        True if the contour is square, False otherwise.
    """
    return (cv2.contourArea(contour) > min_size and
            # Test that the Aspect Ratio (default 1.27) 
            ## ratio between the width and height of minAreaRect 
            ## (which is like a bounding box but will consider rotation) ^
            max(cv2.minAreaRect(contour)[1]) / min(cv2.minAreaRect(contour)[1]) < aspect_ratio and
            # Test that the Solidity (default 0.8) 
            ## Compare minAreaRect area to the actual contour area, a chip should be mostly solid 
            (cv2.contourArea(contour) / np.prod(cv2.minAreaRect(contour)[1])) > solidity)


def _get_contour_sizes(contours):
    """Get the shape and size of all contours.

    Parameters
    ----------
    contours : list
        List of OpenCV contours.

    Returns
    -------
    list
        Contour areas, widths, and heights.
    """
    # Initialize chip shape lists
    marea, mwidth, mheight = [], [], []
    # Loop over our contours and size data about them
    for cnt in contours:
        marea.append(cv2.contourArea(cnt))
        _, wh, _ = cv2.minAreaRect(cnt)  # Rotated rectangle
        mwidth.append(wh[0])
        mheight.append(wh[1])
    return marea, mwidth, mheight


def _draw_color_chips(rgb_img, new_centers, radius, color=(255, 255, 0)):
    """Create labeled mask and debug image of color chips.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    new_centers : numpy.array
        Chip centers after transformation.
    radius : int
        Radius of circles to draw on the color chips.

    Returns
    -------
    list
        Labeled mask and debug image.
    """
    # Create blank img for drawing the labeled color card mask
    labeled_mask = np.zeros(rgb_img.shape[0:2])
    debug_img = np.copy(rgb_img)

    # Loop over the new chip centers and draw them on the RGB image and labeled mask
    for i, pt in enumerate(new_centers):
        cv2.circle(labeled_mask, new_centers[i], radius, (i + 1) * 10, -1)
        cv2.circle(debug_img, new_centers[i], radius, color, -1)
        cv2.putText(debug_img, text=str(i), org=pt, fontScale=params.text_size, color=(0, 0, 0),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, thickness=params.text_thickness)
    return labeled_mask, debug_img


def _scale_contour(cnt, scale):
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    cnt_norm = cnt - [cx, cy]
    cnt_scaled = cnt_norm * scale
    cnt_scaled = cnt_scaled + [cx, cy]
    cnt_scaled = cnt_scaled.astype(np.int32)

    return cnt_scaled


def _color_card_detection(rgb_img, **kwargs):
    """Algorithm to automatically detect a color card.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    label : str, optional
        modifies the variable name of observations recorded (default = pcv.params.sample_label).
    **kwargs
        Other keyword arguments passed to cv2.adaptiveThreshold and cv2.circle.

        Valid keyword arguments:
        adaptive_method: 0 (mean) or 1 (Gaussian) (default = 1)
        block_size: int (default = 51)
        radius: int (default = 20)
        min_size: int (default = 1000)
        aspect_ratio: countour squareness filters (default 1.27)
        solidity: contour squareness filters (default 0.8) 
        verbose_debug = bool (default = False)
    
    Returns
    -------
    list
        Labeled mask of chips, debug img, detected chip areas, chip heights, chip widths, bounding box mask
    """
    # Get keyword arguments and set defaults if not set
    min_size = kwargs.get("min_size", 1000)  # Minimum size for _is_square chip filtering
    radius = kwargs.get("radius", 20)  # Radius of circles to draw on the color chips
    adaptive_method = kwargs.get("adaptive_method", 1)  # cv2.adaptiveThreshold method
    block_size = kwargs.get("block_size", 51)  # cv2.adaptiveThreshold block size
    aspect_ratio = kwargs.get("aspect_ratio", 1.27)  # _is_square aspect-ratio filtering
    solidity = kwargs.get("solidity", 0.8)  # _is_square solidity filtering
    verbose_debug = kwargs.get("verbose_debug", False)  # _is_square solidity filtering

    # Throw a fatal error if block_size is not odd or greater than 1
    if not (block_size % 2 == 1 and block_size > 1):
        fatal_error('block_size parameter must be an odd int greater than 1.')

    # Hard code since we don't currently support other color cards
    nrows = 6
    ncols = 4

    # Convert to grayscale, threshold, and findContours
    imgray = _rgb2hsv(rgb_img=rgb_img, channel="v")
    gaussian = cv2.GaussianBlur(imgray, (11, 11), 0)
    thresh = cv2.adaptiveThreshold(gaussian, 255, adaptive_method,
                                   cv2.THRESH_BINARY_INV, block_size, 2)
    print("auto_threshold results:")
    _debug(visual=thresh, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours, keep only square-shaped ones
    filtered_contours = [contour for contour in contours if _is_square(contour, min_size, aspect_ratio, solidity)]
    debug_img = np.copy(rgb_img)
    print("square-like contours:")
    cv2.drawContours(debug_img, filtered_contours, -1, color=(255, 50, 250), thickness=params.line_thickness)
    _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))
    debug_img = np.copy(rgb_img)
    # Calculate median area of square contours
    target_square_area = np.median([cv2.contourArea(cnt) for cnt in filtered_contours])
    # Filter contours again, keep only those within 20% of median area
    filtered_contours = [contour for contour in filtered_contours if
                         (0.8 < (cv2.contourArea(contour) / target_square_area) < 1.2)]
    
    # Draw detected corners on debug img
    corners_debug_img = np.copy(rgb_img)

    # Throw a fatal error if no color card found
    if len(filtered_contours) == 0:
        if verbose_debug:
            print("Objects found through edge detection (parameterizes with adaptive_method and block_size)")
            cv2.drawContours(debug_img, contours, -1, color=(255, 50, 250), thickness=params.line_thickness)
            _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))
        fatal_error('No color card found')

    # Initialize chip size & dimension lists
    marea, mwidth, mheight = _get_contour_sizes(filtered_contours)
    boundind_mask = np.zeros(rgb_img.shape[0:2])

    # Concatenate all detected centers into one array (minimum area rectangle used to find chip centers)
    square_centroids = np.concatenate([[np.array(cv2.minAreaRect(i)[0]).astype(int)] for i in filtered_contours])

    # Increment amount is arbitrary, cell distances rescaled during perspective transform
    increment = 100
    centers = [[int(0 + i * increment), int(0 + j * increment)] for j in range(nrows) for i in range(ncols)]

    # Find the minimum area rectangle of the hypothetical labeled mask
    new_rect = cv2.minAreaRect(np.array(centers))
    # Get the corners of the rectangle
    box_points = cv2.boxPoints(new_rect).astype("float32")
    box_points_int = np.int_(box_points)

    ### This is where the algorithm *might* split ###
    #########################################################################################################
    ## Plot the centers of each detected chip contour 
    rect = cv2.minAreaRect(square_centroids) ########## handles rotation but not skew 
    
    # Get the corners of the rectangle
    corners = np.array(np.intp(cv2.boxPoints(rect)))
    ## Find white chip and reorder 
    # Determine which corner most likely contains the white chip
    white_index = np.argmin([np.mean(math.dist(rgb_img[corner[1], corner[0], :], (255, 255, 255))) for corner in corners])
    # Sort color chips based on detected card orientation
    corners = corners[np.argsort([math.dist(corner, corners[white_index]) for corner in corners])[[0, 1, 3, 2]]]
    
    # Draw the corners as WHITE contour
    print("boundingRect outline:")
    _, debug_img = _draw_color_chips(debug_img, corners, radius)
    cv2.drawContours(debug_img, [corners], -1, (255, 255, 255), params.line_thickness + 3)
    _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))
    debug_img = np.copy(rgb_img)
    
    # Calculate the perspective transform matrix from the minimum area rectangle
    m_transform = cv2.getPerspectiveTransform(box_points, corners.astype("float32"))
    # Transform the chip centers using the perspective transform matrix
    new_centers = cv2.transform(np.array([centers]), m_transform)[0][:, 0:2]
    _, corners_debug_img = _draw_color_chips(corners_debug_img, corners, 3, (255,255,255))
    
    # Draw detected and utilized contours
    cv2.drawContours(debug_img, filtered_contours, -1, color=(255, 50, 250), thickness=params.line_thickness)
    # Plot box points
    cv2.drawContours(debug_img, [corners], -1, (255, 0, 0), params.line_thickness)
    labeled_mask, debug_img = _draw_color_chips(debug_img, new_centers, radius)
    print("boundingRect algorithm results:")
    _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))
    debug_img = np.copy(rgb_img)
    #########################################################################################################
    # Find four-sided polygon to describe the skewed color card 
    corners = cv2.approxPolyN(curve=square_centroids, nsides=4, ensure_convex=True) ## gets centers of corner chips
    corners = cv2.approxPolyN(curve=np.concatenate(filtered_contours), nsides=4, ensure_convex=True) ## gets centers of corner chips
    
    # Perspective warp the color card to unskew and un-rotate
    pt_A, pt_B, pt_C, pt_D = corners[0]

    input_pts = np.float32([pt_A, pt_B, pt_C, pt_D])
    width_AD = np.sqrt(((pt_A[0] - pt_D[0]) ** 2) + ((pt_A[1] - pt_D[1]) ** 2))
    width_BC = np.sqrt(((pt_B[0] - pt_C[0]) ** 2) + ((pt_B[1] - pt_C[1]) ** 2))
    maxWidth = max(int(width_AD), int(width_BC))
    
    
    height_AB = np.sqrt(((pt_A[0] - pt_B[0]) ** 2) + ((pt_A[1] - pt_B[1]) ** 2))
    height_CD = np.sqrt(((pt_C[0] - pt_D[0]) ** 2) + ((pt_C[1] - pt_D[1]) ** 2))
    maxHeight = max(int(height_AB), int(height_CD))

    output_pts = np.float32([[0, 0],
                            [0, maxHeight - 1],
                            [maxWidth - 1, maxHeight - 1],
                            [maxWidth - 1, 0]])
    
    M = cv2.getPerspectiveTransform(input_pts,output_pts)
    out = cv2.warpPerspective(rgb_img, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)
    print("warpPerspective result on color card")
    _debug(visual=out, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))
    increment = int((maxWidth + maxHeight) / 10.1)
    radius = int(increment / 7) + 1
    start = int(increment / 2) + 1
    new_centers = [[int(start + i * increment), int(start + j * increment)] for j in range(nrows) for i in range(ncols)]
    
    _, debug_img = _draw_color_chips(out, new_centers, radius)
    print("New approach (labeled mask debug)")
    _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))

    # Draw the approximated polygon (quadrilateral) in GREEN 
    cv2.drawContours(debug_img, [corners], -1, (0, 255, 0), params.line_thickness + 3)
    # Shrink the polygon
    #corners = _scale_contour(corners, .85)
    corners = corners[0]
    if verbose_debug:
        print("Identified color card corners)")
        _, debug_img = _draw_color_chips(debug_img, corners, radius)
        _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))
        debug_img = np.copy(rgb_img)
    # Determine which corner most likely contains the white chip
    white_index = np.argmin([np.mean(math.dist(rgb_img[corner[1], corner[0], :], (255, 255, 255))) for corner in corners])
    corners = corners[np.argsort([math.dist(corner, corners[white_index]) for corner in corners])[[0, 1, 3, 2]]]
    
    # Draw the corners as BLUE contour 
    print("approxPolyN outline:")
    _, debug_img = _draw_color_chips(debug_img, corners, radius)
    cv2.drawContours(debug_img, [corners], -1, (255, 0, 0), params.line_thickness + 3)
    _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))
    debug_img = np.copy(rgb_img)
    
    # Calculate the perspective transform matrix from the minimum area rectangle
    m_transform = cv2.getPerspectiveTransform(box_points, corners.astype("float32"))
    # Transform the chip centers using the perspective transform matrix
    new_centers = cv2.transform(np.array([centers]), m_transform)[0][:, 0:2]
    # Plot and compare corners used in both algorithms
    _, corners_debug_img = _draw_color_chips(corners_debug_img, corners, 2)
    print("Corners used (white for rectangle method, blue for polygon method)")
    _debug(visual=corners_debug_img, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))

    # Create labeled mask and debug image of color chips
    debug_img = np.copy(rgb_img)
    # Plot box points
    cv2.drawContours(debug_img, [corners], -1, (255, 0, 0), params.line_thickness)
    cv2.drawContours(debug_img, [box_points_int], -1, (255, 0, 0), params.line_thickness + 5)
    _, debug_img = _draw_color_chips(debug_img, corners, radius)
    _, debug_img = _draw_color_chips(debug_img, box_points_int, int(radius*1.6))
    debug_img = np.copy(rgb_img)
    # Draw detected and utilized contours
    cv2.drawContours(debug_img, filtered_contours, -1, color=(255, 50, 250), thickness=params.line_thickness)
    # Draw the polygon used to calculate transformation
    cv2.drawContours(debug_img, [corners], -1, (255, 0, 0), params.line_thickness + 3)
    #labeled_mask, debug_img = _draw_color_chips(debug_img, centers, radius)
    labeled_mask, debug_img = _draw_color_chips(debug_img, new_centers, radius)
    print("approxPolyN algorithm results:")

    return labeled_mask, debug_img, marea, mheight, mwidth, boundind_mask


def _set_size_scale_from_chip(color_chip_width, color_chip_height, color_chip_size):
    """Set the size scaling factors in Params from the known size of a given color card target.

    Parameters
    ----------
    color_chip_width : float
        Width in pixels of the detected color chips
    color_chip_height : float
        Height in pixels of the detected color chips
    color_chip_size : str, tuple
        Type of supported color card target ("classic", "passport", or "cameratrax"), or a tuple of
        (width, height) of the color card chip real-world dimensions in milimeters.
    """
    # Define known color chip dimensions, all in milimeters
    card_types = {
        "CLASSIC": {
            "chip_width": 40,
            "chip_height": 40
        },
        "PASSPORT": {
            "chip_width": 12,
            "chip_height": 12
        },
        "CAMERATRAX": {
            "chip_width": 11,
            "chip_height": 11
        }
    }

    # Check if user provided a valid color card type
    if type(color_chip_size) is str and color_chip_size.upper() in card_types:
        # Set size scaling parameters
        params.px_width = card_types[color_chip_size.upper()]["chip_width"] / color_chip_width
        params.px_height = card_types[color_chip_size.upper()]["chip_height"] / color_chip_height
    # If not, check to make sure custom dimensions provided are numeric
    else:
        try:
            # Set size scaling parameters
            params.px_width = float(color_chip_size[0]) / color_chip_width
            params.px_height = float(color_chip_size[1]) / color_chip_height
        # Fail if provided color_chip_size is not supported
        except ValueError:
            fatal_error(f"Invalid input '{color_chip_size}'. Choose from {list(card_types.keys())}\
            or provide your color card chip dimensions explicitly")
        # Fail if provided color_chip_size is integer rather than tuple
        except TypeError:
            fatal_error(f"Invalid input '{color_chip_size}'. Choose from {list(card_types.keys())}\
            or provide your color card chip dimensions explicitly as a tuple e.g. color_chip_size=(10,10).")
    # If size scaling successful, set units to millimeters
    params.unit = "mm"


def mask_color_card(rgb_img, **kwargs):
    """Automatically detect a color card and create bounding box mask of the chips detected.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    **kwargs
        Other keyword arguments passed to cv2.adaptiveThreshold and cv2.circle.

        Valid keyword arguments:
        adaptive_method: 0 (mean) or 1 (Gaussian) (default = 1)
        block_size: int (default = 51)
        radius: int (default = 20)
        min_size: int (default = 1000)

    Returns
    -------

    numpy.ndarray
        Binary bounding box mask of the detected color card chips
    """
    _, _, _, _, _, bounding_mask = _color_card_detection(rgb_img, **kwargs)

    if params.debug is not None:
        # Find contours
        cnt, cnt_str = _cv2_findcontours(bin_img=bounding_mask)

        # Consolidate contours
        obj = _object_composition(contours=cnt, hierarchy=cnt_str)
        bb_debug = cv2.drawContours(np.copy(rgb_img), [obj], -1, (255, 0, 255), params.line_thickness)

        # Debug image handling
        _debug(visual=bb_debug, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))

    return bounding_mask


def detect_color_card(rgb_img, label=None, color_chip_size=None, **kwargs):
    """Automatically detect a Macbeth ColorChecker style color card.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    label : str, optional
        modifies the variable name of observations recorded (default = pcv.params.sample_label).
    color_chip_size: str, tuple, optional
        "passport", "classic", "cameratrax"; or tuple formatted (width, height)
        in millimeters (default = None)
    **kwargs
        Other keyword arguments passed to cv2.adaptiveThreshold and cv2.circle.

        Valid keyword arguments:
        adaptive_method: 0 (mean) or 1 (Gaussian) (default = 1)
        block_size: int (default = 51)
        radius: int (default = 20)
        min_size: int (default = 1000)
        aspect_ratio: float (default = 1.27)
        solidity: float (default = 0.8)
        verbose_debug = bool (default = False)

    Returns
    -------
    numpy.ndarray
        Labeled mask of chips.
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label
    deprecation_warning(
        "The 'label' parameter is no longer utilized, since color chip size is now metadata. "
        "It will be removed in PlantCV v5.0."
        )

    labeled_mask, debug_img, marea, mheight, mwidth, _ = _color_card_detection(rgb_img, **kwargs)
    # Create dataframe for easy summary stats
    chip_size = np.median(marea)
    chip_height = np.median(mheight)
    chip_width = np.median(mwidth)

    # Save out chip size for pixel to mm standardization
    outputs.add_metadata(term="median_color_chip_size", datatype=float, value=chip_size)
    outputs.add_metadata(term="median_color_chip_width", datatype=float, value=chip_width)
    outputs.add_metadata(term="median_color_chip_height", datatype=float, value=chip_height)

    # Set size scaling factor if card type is provided
    if color_chip_size:
        _set_size_scale_from_chip(color_chip_height=chip_height, color_chip_width=chip_width, color_chip_size=color_chip_size)

    # Debugging
    _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))

    return labeled_mask
