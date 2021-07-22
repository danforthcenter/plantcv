from plantcv.plantcv import fatal_error


def _show_dataarray(img, **kwargs):
    """
    Plot facetted images from xarray dataarray

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

    col_or_row_given = col is not None or row is not None
    if not col_or_row_given:
        fatal_error('You need to specify `col` or `row` with which to facet the xarray images. '
                    'We only support xarray facetted image plots using pcolormesh() in pcv functions. '
                    'For other types of plots please use xarray plotting methods and matplotlib directly.')

    contains_xy = len([dim for dim in ['x', 'y'] if dim in img.dims]) == 2
    if not contains_xy:
        fatal_error('You are missing x and y dimensions. '
                    'We only support xarray facetted image plots using pcolormesh() in pcv functions. '
                    'For other types of plots please use xarray plotting methods and matplotlib directly.')

    try:
        # need to force pcolormesh() for case when dim in col or row has length 1
        # https://github.com/pydata/xarray/issues/620
        fig_handle = img.plot.pcolormesh(col=col, row=row, **kwargs)
    except ValueError as err:
        raise ValueError(f'You are trying to plot shape {img.shape} but you should have exactly 2 dimensions in '
                         'addition those specified by `col` and `row`.') from err

    return fig_handle
