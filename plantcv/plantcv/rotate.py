from plantcv.plantcv.transform import rotate as rotate_new
import sys


def rotate(img, rotation_deg, crop):
    """Rotate image, sometimes it is necessary to rotate image, especially when clustering for
       multiple plants is needed.

    Inputs:
    img          = RGB or grayscale image data
    rotation_deg = rotation angle in degrees, can be a negative number,
                   positive values move counter clockwise.
    crop         = either true or false, if true, dimensions of rotated image will be same as original image.

    Returns:
    rotated_img  = rotated image

    :param img: numpy.ndarray
    :param rotation_deg: double
    :param crop: bool
    :return rotated_img: numpy.ndarray
    """
    print("""Deprecation Warning:
    plantcv.rotate has moved to plantcv.transform.rotate. 
    plantcv.rotate will be removed in a future version""", file=sys.stderr)
    rotated_img = rotate_new(img, rotation_deg, crop)
    return rotated_img
