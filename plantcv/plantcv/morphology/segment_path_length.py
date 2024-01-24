"""Find geodesic lengths of skeleton segments."""
import os
import cv2
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv._debug import _debug


def segment_path_length(segmented_img, objects, label=None):
    """Use segments to calculate geodesic distance per segment.

    Inputs:
    segmented_img = Segmented image to plot lengths on
    objects       = List of contours
    label         = Optional label parameter, modifies the variable name of
                    observations recorded (default = pcv.params.sample_label).

    Returns:
    labeled_img        = Segmented debugging image with lengths labeled

    :param segmented_img: numpy.ndarray
    :param objects: list
    :param label: str
    :return labeled_img: numpy.ndarray
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    label_coord_x = []
    label_coord_y = []
    segment_lengths = []
    labeled_img = segmented_img.copy()

    for obj in objects:
        # Calculate geodesic distance, divide by two since cv2 seems to be taking the perimeter of the contour
        segment_lengths.append(float(cv2.arcLength(obj, False) / 2))
        # Store coordinates for labels
        label_coord_x.append(obj[0][0][0])
        label_coord_y.append(obj[0][0][1])

    segment_ids = []
    # Put labels of length
    for c, value in enumerate(segment_lengths):
        text = f"{value:0,.2f}"
        w = label_coord_x[c]
        h = label_coord_y[c]
        cv2.putText(img=labeled_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=params.text_size, color=(150, 150, 150), thickness=params.text_thickness)
        segment_ids.append(c)

    outputs.add_observation(sample=label, variable='segment_path_length', trait='segment path length',
                            method='plantcv.plantcv.morphology.segment_path_length', scale='pixels', datatype=list,
                            value=segment_lengths, label=segment_ids)

    _debug(visual=labeled_img, filename=os.path.join(params.debug_outdir, f"{params.device}_segment_path_lengths.png"))

    return labeled_img
