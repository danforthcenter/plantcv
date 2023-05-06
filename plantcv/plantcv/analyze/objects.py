# A function that analyzes the shape and size of objects and outputs data
from plantcv.plantcv._helpers import _iterate_analysis


def objects(labeled_mask, n_labels, label="default"):
    """A function that analyzes the shape and size of objects and outputs data.

    Inputs:
    labeled_mask = Labeled mask of objects (32-bit).
    n_labels     = Total number of labels in the image.
    label        = Optional label parameter, modifies the variable name of observations recorded.

    Returns:
    analysis_image = Diagnostic image showing measurements.

    :param labeled_mask: numpy.ndarray
    :param n_labels: int
    :param label: str
    :return analysis_image: numpy.ndarray
    """
    _iterate_analysis(labeled_mask=labeled_mask, n_labels=n_labels, function=_analyze_object, label=label)


def _analyze_object(mask, label):
    """Analyze individual objects.

    Inputs:
    mask  = Binary image data
    label = Label of object

    Returns:
    analysis_image = Diagnostic image showing measurements

    :param mask: numpy.ndarray
    :param label: int
    :return analysis_image: numpy.ndarray
    """
