"""Reassign PSII frame labels based on induction curve"""
import numpy as np
from plantcv.plantcv import fatal_error
from plantcv.plantcv.classes import PSII_data
from plantcv.plantcv import params


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
    params.device += 1

    try:
        if ps_da.name not in ["ojip_light", "ojip_dark"]:
            fatal_error("You must provide a xarray DataArray with name ojip_light or ojip_dark")
    except AttributeError:
        if isinstance(ps_da, PSII_data):
            fatal_error("You need to provide the `ojip_dark` or `ojip_light` dataarray")
        else:
            fatal_error("You must provide a xarray DataArray with name ojip_light or ojip_dark")

    if mask.shape != ps_da.shape[:2] or len(np.unique(mask)) > 2:
        fatal_error(f"Mask needs to be binary and have shape {ps_da.shape[:2]}")

    # Prime is empty for Fv/Fm (dark- and light-adapted) and p for Fq'/Fm'
    datasets = {
        "ojip_light": {
            "prime": "p",
            "label": "PSL",
            "F": "Fp"
        },
        "ojip_dark": {
            "prime": "",
            "label": "PSD",
            "F": "F0"
        }
    }

    # Get the number of frame labels
    ind_size = ps_da.frame_label.size
    # Create a new frame label array populated with the current labels
    idx = ps_da.frame_label.values
    # Find the frame corresponding to the first frame after F0/Fp
    f = idx.tolist().index(datasets[ps_da.name.lower()]['F']) + 1
    # Reset the frame labels after F0/Fp
    for i in range(f, ind_size):
        idx[i] = f"{datasets[ps_da.name.lower()]['label']}{i}"
    # get plant mean for each frame based on mask
    exp_mask = np.copy(mask)[..., None, None]
    fluor_values = ps_da.where(exp_mask > 0).mean(['x', 'y', 'measurement'])
    # find frame with max mean after the control and F/F' frames
    max_ind = np.argmax(fluor_values.data[f:])
    # assign max frame label
    idx[max_ind + f] = f"Fm{datasets[ps_da.name.lower()]['prime']}"
    # assign new labels back to dataarray
    ps_da = ps_da.assign_coords({'frame_label': ('frame_label', idx)})

    return ps_da
