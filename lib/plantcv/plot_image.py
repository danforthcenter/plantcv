# Plot image to screen
from matplotlib import pyplot as plt


def plot_image(img):
    """Plot an image to the screen.

    :param img: numpy array
    :return:
    """

    plt.imshow(img)
    plt.show()
