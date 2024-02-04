# Plot segment ID numbers

import os
import cv2
from plantcv.plantcv import color_palette
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def segment_id(skel_img, objects, mask=None):
    """Plot segment IDs.

    Inputs:
    skel_img      = Skeletonized image
    objects       = List of contours
    mask          = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.

    Returns:
    segmented_img = Segmented image
    labeled_img   = Labeled image

    :param skel_img: numpy.ndarray
    :param objects: list
    :param mask: numpy.ndarray
    :return segmented_img: numpy.ndarray
    :return labeled_img: numpy.ndarray
    """
    label_coord_x = []
    label_coord_y = []

    if mask is None:
        segmented_img = skel_img.copy()
    else:
        segmented_img = mask.copy()

    segmented_img = cv2.cvtColor(segmented_img, cv2.COLOR_GRAY2RGB)

    # Create a color scale, use a previously stored scale if available
    rand_color = color_palette(num=len(objects), saved=True)

    # Plot all segment contours
    for i, cnt in enumerate(objects):
        cv2.drawContours(segmented_img, cnt, -1, rand_color[i], params.line_thickness, lineType=8)
        # Store coordinates for labels
        label_coord_x.append(objects[i][0][0][0])
        label_coord_y.append(objects[i][0][0][1])

    labeled_img = segmented_img.copy()

    for i, cnt in enumerate(objects):
        # Label slope lines
        w = label_coord_x[i]
        h = label_coord_y[i]
        text = f"ID:{i}"
        cv2.putText(img=labeled_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=params.text_size, color=rand_color[i], thickness=params.text_thickness)

    _debug(visual=labeled_img, filename=os.path.join(params.debug_outdir, f"{params.device}_segmented_ids.png"))

    return segmented_img, labeled_img
