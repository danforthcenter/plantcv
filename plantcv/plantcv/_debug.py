# Debugging module
from plantcv.plantcv._globals import params
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image


def _debug(visual, filename=None, verbosity_level=0, **kwargs):
    """Save or display a visual for debugging.

    Parameters
    ----------
    visual          = numpy.ndarray, An image or plot to display for debugging
    filename        = str, An optional filename to save the visual to (default: None)
    verbosity level = int, threshold for params.verbose to make debug image.
                          Defaults to 0, which essentially ignores params.verbose
    kwargs          = dict, key-value arguments to xarray.plot method

    Returns
    -------
    No returns
    """
    # if verbose from params is at least to the verbosity level, make debug images
    if params.verbose >= verbosity_level:
        # Auto-increment the device counter
        params.device += 1

        if params.debug == "print":
            # If debug is print, save the image to a file
            print_image(img=visual, filename=filename, **kwargs)
        elif params.debug == "plot":
            # If debug is plot, print to the plotting device
            plot_image(img=visual, **kwargs)
