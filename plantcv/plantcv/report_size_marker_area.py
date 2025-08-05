"""Analyzes an object and outputs numeric properties."""
import cv2
import numpy as np
import os
from plantcv.plantcv import params, outputs, fatal_error, apply_mask, warn, deprecation_warning
from plantcv.plantcv.threshold import binary as binary_threshold
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _cv2_findcontours, _object_composition, _roi_filter, _rgb2hsv


def report_size_marker_area(img, roi, marker='define', objcolor='dark', thresh_channel=None,
                            thresh=None, label=None):
    """
    Detects a size marker in a specified region and reports its size and eccentricity

    Inputs:
    img             = An RGB or grayscale image to plot the marker object on
    roi             = A region of interest (e.g. output from pcv.roi.rectangle or other methods)
    marker          = 'define' or 'detect'. If define it means you set an area, if detect it means you want to
                      detect within an area
    objcolor        = Object color is 'dark' or 'light' (is the marker darker or lighter than the background)
    thresh_channel  = 'h', 's', or 'v' for hue, saturation or value
    thresh          = Binary threshold value (integer)
    label           = Optional label parameter, modifies the variable name of
                      observations recorded (default = pcv.params.sample_label).

    Returns:
    analysis_images = List of output images

    :param img: numpy.ndarray
    :param roi: plantcv.plantcv.classes.Objects
    :param marker: str
    :param objcolor: str
    :param thresh_channel: str
    :param thresh: int
    :param label: str
    :return: analysis_images: list
    """
    deprecation_warning(
        "the 'label' parameter is no longer utilized, since size marker is now metadata. "
        "It will be removed in PlantCV 5.0."
        )

    # Store debug
    debug = params.debug
    params.debug = None
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    params.device += 1
    # Make a copy of the reference image
    ref_img = np.copy(img)
    # If the reference image is grayscale convert it to color
    if len(np.shape(ref_img)) == 2:
        ref_img = cv2.cvtColor(ref_img, cv2.COLOR_GRAY2BGR)

    # Marker components
    # If the marker type is "defined" then the marker_mask and marker_contours are equal to the input ROI
    # Initialize a binary image
    roi_mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
    # Draw the filled ROI on the mask
    cv2.drawContours(roi_mask, roi.contours[0], -1, (255), -1)
    # Marker mask
    marker_mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)

    # If the marker type is "detect" then we will use the ROI to isolate marker contours from the input image
    if marker.upper() == 'DETECT':
        # We need to convert the input image into an one of the HSV channels and then threshold it
        if thresh_channel is not None and thresh is not None:
            # Mask the input image
            masked = apply_mask(img=ref_img, mask=roi_mask, mask_color="black")
            # Convert the masked image to hue, saturation, or value
            marker_hsv = _rgb2hsv(rgb_img=masked, channel=thresh_channel)
            # Threshold the HSV image
            marker_bin = binary_threshold(gray_img=marker_hsv, threshold=thresh, object_type=objcolor)
            # Identify contours in the masked image
            contours, hierarchy = _cv2_findcontours(bin_img=marker_bin)

            # Filter marker contours using the input ROI
            kept_contours, kept_hierarchy, _ = _roi_filter(img=marker_bin, roi=roi, obj=contours,
                                                           hierarchy=hierarchy, roi_type="partial")
            # If there are more than one contour detected, combine them into one
            marker_contour = _object_composition(contours=kept_contours, hierarchy=kept_hierarchy)
            cv2.drawContours(marker_mask, kept_contours, -1, (255), -1, hierarchy=kept_hierarchy)
        else:
            # Reset debug mode
            params.debug = debug
            fatal_error('thresh_channel and thresh must be defined in detect mode')
    elif marker.upper() == "DEFINE":
        marker_mask = roi_mask
    else:
        # Reset debug mode
        params.debug = debug
        fatal_error(f"marker must be either 'define' or 'detect' but {marker} was provided.")

    # Calculate the moments of the defined marker region
    m = cv2.moments(marker_mask, binaryImage=True)
    cnt, h = _cv2_findcontours(bin_img=marker_mask)
    marker_contour = _object_composition(contours=cnt, hierarchy=h)

    # Calculate the marker area
    marker_area = m['m00']

    if len(marker_contour) > 5:
        # Fit a bounding ellipse to the marker
        _, axes, _ = cv2.fitEllipse(marker_contour)
        major_axis = np.argmax(axes)
        minor_axis = 1 - major_axis
        major_axis_length = axes[major_axis]
        minor_axis_length = axes[minor_axis]
        # Calculate the bounding ellipse eccentricity
        eccentricity = np.sqrt(1 - (axes[minor_axis] / axes[major_axis]) ** 2)

        cv2.drawContours(ref_img, marker_contour, -1, (255, 0, 0), 5)
        analysis_image = ref_img

        # Reset debug mode
        params.debug = debug

        _debug(visual=ref_img,
               filename=os.path.join(params.debug_outdir, str(params.device) + '_marker_shape.png'))

        # Store size marker values as metadata
        outputs.add_metadata(term="marker_area", datatype=int, value=marker_area)
        outputs.add_metadata(term="marker_ellipse_major_axis", datatype=int, value=major_axis_length)
        outputs.add_metadata(term="marker_ellipse_minor_axis", datatype=int, value=minor_axis_length)
        outputs.add_metadata(term="marker_ellipse_eccentricity", datatype=float, value=eccentricity)

        return analysis_image

    # Store size marker values as metadata
    outputs.add_metadata(term="marker_area", datatype=str, value='none')
    outputs.add_metadata(term="marker_ellipse_major_axis", datatype=str, value='none')
    outputs.add_metadata(term="marker_ellipse_minor_axis", datatype=str, value='none')
    outputs.add_metadata(term="marker_ellipse_eccentricity", datatype=str, value='none')

    warn("Size marker is not detectable.")

    return None
