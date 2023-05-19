import os

from plantcv.plantcv._helpers import _iterate_analysis, _cv2_findcontours, _object_composition, _grayscale_to_rgb


def bound_horizontal(img, labeled_mask, n_labels=1, line_position, label="default"):
    """A function that analyzes the shape and size of objects and outputs data.

    Inputs:
    img           = RGB or grayscale image data for plotting
    labeled_mask  = Labeled mask of objects (32-bit).
    n_labels      = Total number expected individual objects (default = 1).
    line_position = position of boundary line in pixels from top to bottom
                    (a value of 0 would draw the line through the top of the image)
    label         = Optional label parameter, modifies the variable name of
                    observations recorded (default = "default").

    Returns:
    analysis_image = Diagnostic image showing measurements.

    :param img: numpy.ndarray
    :param labeled_mask: numpy.ndarray
    :param n_labels: int
    :param line_position: int
    :param label: str
    :return analysis_image: numpy.ndarray
    """
    img = _iterate_analysis(img=img, labeled_mask=labeled_mask, n_labels=n_labels, label=label, function=_analyze_size)
    # Debugging
    _debug(visual=img, filename=os.path.join(params.debug_outdir, str(params.device) + '_boundary_on_img.png'))
    return img
