# Anthocyanin Analysis

import os
import numpy as np
from plotnine.labels import labs
from plantcv.plantcv import fatal_error
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv.visualize import histogram


def analyze_anth(ps, mask, bins=256, label="default"):
    """
    Calculate and analyze Anthocyanin Reflectance Index (ARI) from fluorescence image data.

    Inputs:
    ps                   = photosynthesis data in xarray DataArray format
    mask                 = mask of plant
    bins                 = number of bins for the histogram (1 to 256 for 8-bit; 1 to 65,536 for 16-bit; default is 256)
    label                = optional label parameter, modifies the entity name of observations recorded

    Returns:
    anth       = DataArray of ARI values
    hist_fig   = Histogram of ARI values

    :param ps: xarray.core.dataarray.DataArray
    :param mask: numpy.ndarray
    :param bins: int
    :return anth: xarray.core.dataarray.DataArray
    :return anth_hist: plotnine.ggplot.ggplot
    """

    # check mask shape
    if mask.shape != ps.anthocyanin.shape[:2]:
        fatal_error(f"Mask needs to have shape {ps.anthocyanin.shape[:2]}")

    if len(np.unique(mask)) > 2 or mask.dtype != 'uint8':
        fatal_error("Mask must have dtype uint8 and be binary")

    # calculate ARI from anthocyanin reflectance at 550 nm and a far-red reference at 700 nm
    r550 = ps.anthocyanin.sel(frame_label='Anth').where(mask > 0)
    r700 = ps.anthocyanin.sel(frame_label='Far-red').where(mask > 0)
    anth = (1 / r550) - (1 / r700)

    # compute observations to store in Outputs
    anth_median = anth.where(anth > 0).median(['x', 'y']).values
    anth_max = anth.where(anth > 0).max(['x', 'y']).values

    # create histogram
    hist_fig, hist_data = histogram(img=anth, mask=mask, bins=bins, lower_bound=0, upper_bound=4.5,
                                    title="ARI", hist_data=True)

    hist_fig = hist_fig + labs(x="ARI", y="Proportion of pixels (%)")

    # Plot/Print out the histograms
    _debug(visual=hist_fig,
           filename=os.path.join(params.debug_outdir, str(params.device) + f"_ARI_histogram.png"))

    # median value
    outputs.add_observation(sample=label, variable=f"anth_median", trait="median ARI value",
                            method='plantcv.plantcv.photosynthesis.analyze_anth', scale='none', datatype=float,
                            value=float(np.around(anth_median, decimals=4)), label='none')
    # max value
    outputs.add_observation(sample=label, variable=f"anth_max", trait="peak ARI value",
                            method='plantcv.plantcv.photosynthesis.analyze_anth', scale='none', datatype=float,
                            value=float(anth_max), label='none')
    # hist frequencies
    outputs.add_observation(sample=label, variable=f"anth_hist", trait="ARI frequencies",
                            method='plantcv.plantcv.photosynthesis.analyze_anth', scale='none', datatype=list,
                            value=hist_data['hist count'].values.tolist(),
                            label=np.around(hist_data['pixel intensity'].values.tolist(), decimals = 3).tolist())

    # Store images
    outputs.images.append(anth)

    return anth, hist_fig
