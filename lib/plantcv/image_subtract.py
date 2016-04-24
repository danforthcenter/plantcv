# Image subtraction

from . import print_image


def image_subtract(img1, img2, device, debug=False):
    """This is a function used to subtract one image from another image (img1 - img2). The numpy subtraction function
       '-' is used. This is a modulo operation rather than the cv2.subtract fxn which is a saturation operation.
       ddepth = -1 specifies that the dimensions of output image will be the same as the input image.

    Inputs:
    img1      = input image
    img2      = input image used to subtract from img1
    device    = device number. Used to count steps in the pipeline
    debug     = True/False. If True; print output image

    Returns:
    device    = device number
    subed_img = subtracted image

    :param img1: numpy array
    :param img2: numpy array
    :param device: int
    :param debug: bool
    :return device: int
    :return subed_img: numpy array
    """

    subed_img = img1 - img2
    device += 1
    if debug:
        print_image(subed_img, str(device) + '_subtracted' + '.png')
    return device, subed_img
