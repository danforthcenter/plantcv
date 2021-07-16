# Debugging module
from plantcv.plantcv import params
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image


def _debug(visual, filename=None, **kwargs):
    """
    Save or display a visual for debugging.

    Inputs:
    visual   - An image or plot to display for debugging
    filename - An optional filename to save the visual to (default: None)
    kwargs - key-value arguments to xarray.plot method

    :param visual: numpy.ndarray
    :param filename: str
    :param kwargs: dict
    """
    # Auto-increment the device counter
    params.device += 1

    if params.debug == "print":
        # If debug is print, save the image to a file
        print_image(img=visual, filename=filename, **kwargs)
    elif params.debug == "plot":
        # If debug is plot, print to the plotting device
        plot_image(img=visual, **kwargs)


def _show_dataarray(img, **kwargs):
    """
    Determine how to show data array

    Inputs:
    img     - dataarray to display
    kwargs  - key-value arguments to xarray.plot method

    :param img: xr.core.dataarray.DataArray
    :param kwargs: dict of arguments recognized by xarray.plot.plot
    """
    # check for kwargs col and row. col and row are removed from kwargs!
    # the default for col and row are None
    col = kwargs.pop('col', None)
    row = kwargs.pop('row', None)

    # if x and y exist assume we want to see the image
    # need to force pcolormesh() for case when dim in col or row has length 1  https://github.com/pydata/xarray/issues/620
    contains_xy = all([True for dim in ['x', 'y'] if dim in img.dims])
    col_or_row_given = col is not None or row is not None
    if contains_xy and col_or_row_given:
        img.plot.pcolormesh(col=col, row=row, **kwargs)
    else:
        img.plot(col=col, row=row, **kwargs)
