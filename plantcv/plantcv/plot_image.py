# Plot image to screen
import os
import cv2
import numpy


def plot_image(img, cmap=None):
    """Plot an image to the screen.

    :param img: numpy.ndarray
    :param cmap: str
    :return:
    """
    from matplotlib import pyplot as plt

    image_type = type(img)

    dimensions = numpy.shape(img)

    if image_type == numpy.ndarray:
        # If the image is color then OpenCV stores it as BGR, we plot it as RGB
        if len(dimensions) == 3:
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            plt.show()

        elif cmap is None and len(dimensions) == 2:
            plt.imshow(img, cmap="gray")
            plt.show()

        elif cmap is not None and len(dimensions) == 2:
            plt.imshow(img, cmap=cmap)
            plt.show()

    # Plot if the image is a plotnine ggplot image
    elif str(image_type) == "<class 'plotnine.ggplot.ggplot'>":
        print(img)
