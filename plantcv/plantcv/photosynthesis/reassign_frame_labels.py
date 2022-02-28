import numpy as np
import os
import pandas as pd
from skimage.util import img_as_bool
from plantcv.plantcv import fatal_error
from plantcv.plantcv.classes import PSII_data
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plotnine import ggplot, aes, geom_line, geom_point, labs


def reassign_frame_labels(ps_da, mask):
    """
    Analyze fluorescence induction curve and assign Fm or Fmp frame labels.

    Designed for cropreporter data. Analyze fluorescence frames to find max mean fluorescence and assign Fm or Fmp.
    Use this if you want to assign Fm/Fmp based on observed values rather than CropReporter metadata.

    Inputs:
    ps_da       = photosynthesis xarray DataArray
    mask        = mask of plant (binary, single channel)

    Returns:
    ps_da       = dataarray with updated frame_label coordinate
    ind_fig     = ggplot induction curve of fluorescence
    ind_df      = data frame of mean fluorescence in the masked region at each timepoint

    :param ps_da: xarray.core.dataarray.DataArray
    :param mask: numpy.ndarray
    :return ps_da: xarray.core.dataarray.DataArray
    :return ind_fig: ggplot figure
    :return ind_df: pandas.core.frame.DataFrame
    """

    try:
        if ps_da.name != "lightadapted" and ps_da.name != "darkadapted":
            fatal_error("You must provide a xarray DataArray with name lightadapted or darkadapted")
    except AttributeError:
        if isinstance(ps_da, PSII_data):
            fatal_error("You need to provide the `darkadapted` or `lightadapted` dataarray")
        else:
            fatal_error("You must provide a xarray DataArray with name lightadapted or darkadapted")

    if mask.shape != ps_da.shape[:2] or len(np.unique(mask)) > 2:
        fatal_error(f"Mask needs to be binary and have shape {ps_da.shape[:2]}")

    # Prime is empty for Fv/Fm (dark- and light-adapted) and p for Fq'/Fm'
    datasets = {
        "lightadapted": {
            "prime": "p",
            "label": "PSL"
        },
        "darkadapted": {
            "prime": "",
            "label": "PSD"
        }
    }

    # Get the number of frame labels
    ind_size = ps_da.frame_label.size
    # Create a new frame label array populated with the current labels
    idx = ps_da.frame_label.values
    # Reset the frame labels after F0/Fp
    for i in range(2, ind_size):
        idx[i] = f"{datasets[ps_da.name.lower()]['label']}{i}"
    # get plant mean for each frame based on mask
    fluor_values = ps_da.where(img_as_bool(mask)[..., None, None]).mean(['x', 'y', 'measurement'])
    # find frame with max mean
    max_ind = np.argmax(fluor_values.data)
    # assign max frame label
    idx[max_ind] = f"Fm{datasets[ps_da.name.lower()]['prime']}"
    # assign new labels back to dataarray
    ps_da = ps_da.assign_coords({'frame_label': ('frame_label', idx)})

    # save induction curve data to dataframe
    ind_df = pd.DataFrame({"Timepoints": range(0, ind_size), "Fluorescence": fluor_values})  # "Measurement": meas})

    # Make the histogram figure using plotnine
    ind_fig = (ggplot(data=ind_df, mapping=aes(x='Timepoints', y='Fluorescence'))
               + geom_line(show_legend=True, color="green")
               + geom_point()
               + labs(title=f"{ps_da.name} fluorescence")
               )

    # Plot/Print out the histograms
    _debug(visual=ind_fig,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_fluor_histogram.png"))

    return ps_da, ind_fig, ind_df
