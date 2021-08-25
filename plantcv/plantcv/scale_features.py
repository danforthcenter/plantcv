# Function to return feature scaled points

import os
import cv2
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params


def scale_features(obj, mask, points, line_position):
    """
    scale_features: returns feature scaled points

    This is a function to transform the coordinates of landmark points onto a common scale (0 - 1.0).

    Inputs:
    obj           = a contour of the plant object (this should be output from the object_composition.py fxn)
    mask          = this is a binary image. The object should be white and the background should be black
    points        = the points to scale
    line_position = A vertical coordinate that denotes the height of the plant pot, the coordinates of this reference
                    point is also rescaled

    :param obj: ndarray
    :param mask: ndarray
    :param points: ndarray
    :param line_position: int
    :return rescaled: list
    :return centroid_scaled: tuple
    :return boundary_line_scaled: tuple
    """
    # Get the dimensions of the image from the binary thresholded object (mask)
    if not np.any(mask) or not np.any(obj):
        rescaled = ('NA', 'NA')
        centroid_scaled = ('NA', 'NA')
        boundary_line_scaled = ('NA', 'NA')
        return rescaled, centroid_scaled, boundary_line_scaled
    iy, ix = np.shape(mask)
    x, y, width, height = cv2.boundingRect(obj)
    m = cv2.moments(mask, binaryImage=True)
    cmx, cmy = (m['m10'] / m['m00'], m['m01'] / m['m00'])
    # Convert the boundary line position (top of the pot) into a coordinate on the image
    if line_position != 'NA':
        line_pos = int(iy) - int(line_position)
        bly = line_pos
    else:
        bly = cmy
    blx = cmx
    # Maximum and minimum values of the object
    ymax = y
    ymin = y + height
    xmin = x
    xmax = x + width
    # Scale the coordinates of each of the feature locations
    rescaled = []
    for p in points:
        xval = float(p[0, 0] - xmin) / float(xmax - xmin)
        yval = float(p[0, 1] - ymin) / float(ymax - ymin)
        scaled_point = (xval, yval)
        rescaled.append(scaled_point)
    # Lets rescale the centroid
    cmx_scaled = float(cmx - xmin) / float(xmax - xmin)
    cmy_scaled = float(cmy - ymin) / float(ymax - ymin)
    centroid_scaled = (cmx_scaled, cmy_scaled)
    # Lets rescale the boundary_line
    blx_scaled = float(blx - xmin) / float(xmax - xmin)
    bly_scaled = float(bly - ymin) / float(ymax - ymin)
    boundary_line_scaled = (blx_scaled, bly_scaled)

    # Make a decent size blank image regardless of debug
    scaled_img = np.zeros((1500, 1500, 3), np.uint8)

    # If debug is 'True' plot an image of the scaled points on a black background
    if params.debug is not None:
        plotter = np.array(rescaled)
        # Multiple the values between 0 - 1.0 by 1000 so you can plot on the black image
        plotter = plotter * 1000
        # For each of the coordinates plot a circle where the point is
        # (+250 helps center the object in the middle of the blank image)
        for i in plotter:
            x, y = i.ravel()
            cv2.circle(scaled_img, (int(x) + 250, int(y) + 250), params.line_thickness, (255, 255, 255), -1)
        cv2.circle(scaled_img, (int(cmx_scaled * 1000) + 250, int(cmy_scaled * 1000) + 250), params.line_thickness,
                   (255, 0, 255), -1)
        cv2.circle(scaled_img, (int(blx_scaled * 1000) + 250, int(bly_scaled * 1000) + 250), params.line_thickness,
                   (0, 255, 0), -1)
        # Because the coordinates inc as you go down and right on the img you need to flip the object around the x-axis
        flipped_scaled = cv2.flip(scaled_img, 0)
    else:
        flipped_scaled = scaled_img  # for _debug

    # keep outside if statement to avoid new tests
    _debug(visual=flipped_scaled,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_feature_scaled.png'))

    # Return the transformed points
    return rescaled, centroid_scaled, boundary_line_scaled
