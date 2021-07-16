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
        fig = img.plot.pcolormesh(col=col, row=row, **kwargs)
    else:
        fig = img.plot(col=col, row=row, **kwargs)

    return(fig)