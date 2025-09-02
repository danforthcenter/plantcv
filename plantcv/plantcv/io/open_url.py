"""Open an image from a URL."""
import imageio.v3 as iio
import cv2
from plantcv.plantcv import fatal_error
from plantcv.plantcv._debug import _debug


def open_url(url):
    """Open an image from a URL and return it as a numpy array.

    Parameters
    ----------
    url : str
        URL of the image to be opened.

    Returns
    -------
    numpy.ndarray
        Image data as a numpy array.
    """
    # Read the image from the URL using imageio
    image = iio.imread(url)

    # Check if the image is grayscale or RGB
    if len(image.shape) not in [2, 3]:
        fatal_error("Image is not RGB or grayscale.")

    if image.shape[-1] == 3:
        # Convert the image to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Debugging visualization
    _debug(visual=image, filename="url_image.png")

    return image
