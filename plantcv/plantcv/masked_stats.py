import numpy as np


def mean(array, mask):
    """Compute mean for plant area only
    Inputs:
    array       = numpy array, e.g. an image
    mask        = binary image 
    
    Returns:
    mean = mean of array only for pixels in mask with values > 0

    :param array: numpy.ndarray
    :param mask: numpy.ndarray
    :return mean: float
    """

    return(np.mean(array[np.where(mask > 0)]))


def std(array, mask):
    """Compute standard deviation for plant area only
    Inputs:
    array       = numpy array, e.g. an image
    mask        = binary image 

    Returns:
    standard deviation = standard deviation of array only for pixels in mask with values > 0

    :param array: numpy.ndarray
    :param mask: numpy.ndarray
    :return standard deviation: float
    """

    return(np.std(array[np.where(mask > 0)]))


def median(array, mask):
    """Compute median for plant area only
    Inputs:
    array       = numpy array, e.g. an image
    mask        = binary image 

    Returns:
    median = median of array only for pixels in mask with values > 0

    :param array: numpy.ndarray
    :param mask: numpy.ndarray
    :return median: numeric
    """

    return(np.median(array[np.where(mask > 0)]))
