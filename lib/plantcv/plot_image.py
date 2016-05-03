# Plot image to screen


def plot_image(img, cmap=None):
    """Plot an image to the screen.

    :param cmap: str
    :param img: numpy array
    :return:
    """
    from matplotlib import pyplot as plt

    plt.imshow(img, cmap=cmap)
    plt.show()
