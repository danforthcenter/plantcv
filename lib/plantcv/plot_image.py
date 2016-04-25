# Plot image to screen
from matplotlib import pyplot as plt


def plot_image(img, cmap=None):
    """Plot an image to the screen.

    :param img: numpy array
    :return:
    """

    plt.imshow(img, cmap=cmap)
    plt.show()
