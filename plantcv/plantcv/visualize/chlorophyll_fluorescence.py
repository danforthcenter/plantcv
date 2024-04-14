import os
import altair as alt
import pandas as pd
import numpy as np
from plantcv.plantcv import params, fatal_error, PSII_data
from plantcv.plantcv._debug import _debug


def chlorophyll_fluorescence(ps_da, labeled_mask, n_labels=1, label="object"):
    """Plot the chlorophyll fluorescence induction curve for each object.

    Inputs:
    ps_da            = photosynthesis xarray DataArray
    labeled_mask     = Labeled mask of objects (32-bit).
    n_labels         = Total number expected individual objects (default = 1).
    label            = optional label parameter, modifies the prefix of the group plotting label

    Returns:
    chart            = Plot of the chlorophyll fluorescence induction curve for each object

    :param ps_da: xarray.DataArray
    :param labeled_mask: numpy.ndarray
    :param n_labels: int
    :param label: str
    :return chart: altair.Chart
    """
    # Increment function counter
    params.device += 1

    # Check that the dataarray is valid
    try:
        if ps_da.name not in ["ojip_light", "ojip_dark"]:
            fatal_error("You must provide a xarray DataArray with name ojip_light or ojip_dark")
    except AttributeError:
        if isinstance(ps_da, PSII_data):
            fatal_error("You need to provide the `ojip_dark` or `ojip_light` dataarray")
        else:
            fatal_error("You must provide a xarray DataArray with name ojip_light or ojip_dark")

    # Prime is empty for Fv/Fm (dark- and light-adapted) and p for Fq'/Fm'
    datasets = {
        "ojip_light": {
            "prime": "p",
            "label": "PSL"
        },
        "ojip_dark": {
            "prime": "",
            "label": "PSD"
        }
    }

    # Get the number of frame labels
    ind_size = ps_da.frame_label.size

    # Find the current Fm or Fm'
    idx = list(ps_da.frame_label.values).index(f"Fm{datasets[ps_da.name.lower()]['prime']}")

    # Initialize a dictionary to store the induction curve data
    data = {"Timepoints": [], "Fluorescence": [], "Labels": [], "Group": []}

    mask_copy = np.copy(labeled_mask)
    if len(np.unique(mask_copy)) == 2 and np.max(mask_copy) == 255:
        mask_copy = np.where(mask_copy == 255, 1, 0).astype(np.uint8)
    for i in range(1, n_labels + 1):
        # Create a boolean submask for each label
        submask = np.where(mask_copy == i, True, False).astype(bool)

        # Get plant mean for each frame based on mask
        fluor_values = ps_da.where(submask[..., None, None]).mean(['x', 'y', 'measurement']).values

        # Append fluorescence values to data dictionary
        data["Timepoints"].extend(range(0, ind_size))
        data["Fluorescence"].extend(list(fluor_values))
        data["Labels"].extend(list(ps_da.frame_label.values))
        data["Group"].extend([f"{label}{i}"] * ind_size)

    # Create a dataframe from the data dictionary
    df = pd.DataFrame(data)

    # Create a chart
    chart = (
        alt.Chart(df, title=f"{ps_da.name} induction curve")
        .mark_line(point=True)
        .encode(
            x="Timepoints:Q",
            y="Fluorescence:Q",
            color="Group:N",
            tooltip=["Group", "Timepoints", "Fluorescence"]).interactive()
        )
    # Create a vertical rule for the Fm or Fm' value
    rule = (
        alt.Chart(df)
        .mark_rule(strokeDash=[10, 10], color="gray")
        .encode(x=alt.datum(idx))
    )
    # Label the chart with the Fm or Fm' value
    text = (
        alt.Chart(df.query(f"Labels == 'Fm{datasets[ps_da.name.lower()]['prime']}'").iloc[[0]])
        .mark_text(dy=-15)
        .encode(x="Timepoints:Q", y="Fluorescence:Q", text="Labels:N")
    )

    # Plot debug image
    _debug(visual=chart + text + rule,
           filename=os.path.join(params.debug_outdir, f"{params.device}_fluorescence_plot.png"))

    return chart + text + rule
