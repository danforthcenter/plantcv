# Crop

import os
import cv2
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import params



def crop(img, x, y, h, w):
    """Crop image.

       Inputs:
       img       = RGB, grayscale, or hyperspectral image data
       x         = X coordinate of starting point
       y         = Y coordinate of starting point
       h         = Height
       w         = Width

       Returns:
       cropped   = cropped image

       :param img: numpy.ndarray
       :param x: int
       :param y: int
       :param h: int
       :param w: int
       :return cropped: numpy.ndarray
       """

    cropped = img[y:y + h, x:x + w, :]

    # Create the rectangle contour vertices
    pt1 = (x, y)
    pt2 = (x, y + h - 1)
    pt3 = (x + w - 1, y + h - 1)
    pt4 = (x + w - 1, y)

    ref_img = cv2.rectangle(img=np.copy(img), pt1=pt1, pt2=pt3, color=(255, 0, 0),
                            thickness=params.line_thickness)

    if params.debug == "print":
        # If debug is print, save the image to a file
        print_image(ref_img, os.path.join(params.debug_outdir, str(params.device) + "_roi.png"))
    elif params.debug == "plot":
        # If debug is plot, print to the plotting device
        plot_image(ref_img)

    return ref_img
