# Plot image to screen
import cv2

def plot_image(img, cmap=None):
    """Plot an image to the screen.

    :param cmap: str
    :param img: numpy array
    :return:
    """
    from matplotlib import pyplot as plt
    
    if cmap==None:
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()
    else:
        plt.imshow(img, cmap=cmap)
        plt.show()
