# Image addition

from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image


def image_add(img1, img2, device, debug=None):
    """This is a function used to add images. The numpy addition function '+' is used. This is a modulo operation
       rather than the cv2.add fxn which is a saturation operation. ddepth = -1 specifies that the dimensions of output
       image will be the same as the input image.

    Inputs:
    img1      = input image
    img2      = second input image
    device    = device number. Used to count steps in the pipeline
    debug     = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device    = device number
    added_img = summed images

    :param img1: numpy array
    :param img2: numpy array
    :param device: int
    :param debug: str
    :return device: int
    :return added_img: numpy array
    """

    added_img = img1 + img2
    device += 1
    if debug == 'print':
        print_image(added_img, str(device) + '_added' + '.png')
    elif debug == 'plot':
        plot_image(added_img, cmap='gray')
    return device, added_img
