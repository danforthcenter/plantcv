# A function that analyzes the shape and size of objects and outputs data
from plantcv.plantcv._helpers import _iterate_analysis, _cv2_findcontours


def objects(img, labeled_mask, n_labels, label="default"):
    """A function that analyzes the shape and size of objects and outputs data.

    Inputs:
    img          = RGB or grayscale image data for plotting
    labeled_mask = Labeled mask of objects (32-bit).
    n_labels     = Total number of labels in the image.
    label        = Optional label parameter, modifies the variable name of observations recorded.

    Returns:
    analysis_image = Diagnostic image showing measurements.

    :param img: numpy.ndarray
    :param labeled_mask: numpy.ndarray
    :param n_labels: int
    :param label: str
    :return analysis_image: numpy.ndarray
    """
    _iterate_analysis(img=img, labeled_mask=labeled_mask, n_labels=n_labels, label=label, function=_analyze_object)


def _analyze_object(img, mask, label):
    """Analyze individual objects.

    Inputs:
    img   = RGB or grayscale image data for plotting
    mask  = Binary image data
    label = Label of object

    Returns:
    analysis_image = Diagnostic image showing measurements

    :param mask: numpy.ndarray
    :param label: int
    :return analysis_image: numpy.ndarray
    """
