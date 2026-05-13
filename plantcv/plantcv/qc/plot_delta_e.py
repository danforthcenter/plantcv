"""Visualize delta E values for color checker chips in an image"""

import os
import math
import numpy as np
import pandas as pd
import altair as alt
from plantcv.plantcv._globals import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv.transform.color_correction import std_color_matrix, astro_color_matrix


def _bin_deltaE(v):
    """Helper for discretizing delta E
    Parameters
    ----------
    v = float, delta E value

    Returns
    -------
    label = str, discretized bin for delta E value per standard interpretation ranges
    """
    if v < 1:
        return "<1"
    if v < 2:
        return "<2"
    if v < 10:
        return "<10"
    if v < 49:
        return "<49"
    return ">49"


def plot_deltaE(deltaE_matrix):
    """
    Plot a bar chart of deltaE values for color checker chips.

    Parameters
    ----------
    deltaE_matrix = numpy.ndarray,
        4x6 (macbeth) or 3x5 (astrobotany) array of per-chip deltaE values

    Returns
    -------
    chart = altair.vegalite.v5.api.LayerChart
        Altair layered chart with bars colored by deltaE category, reference lines,
        and standard chip color swatches below the x-axis
    """
    n_chips = math.prod(np.shape(deltaE_matrix))
    # chip color swatches below x-axis
    std_mat = std_color_matrix(pos=3)
    if n_chips == 15:
        # astrobotany stuff
        std_mat = astro_color_matrix()

    params.device += 1

    chip_nos = np.arange(1, n_chips + 1)
    delta_vals = deltaE_matrix.flatten(order="C")
    df = pd.DataFrame({
        "chip_no": chip_nos,
        "deltaE": delta_vals,
        "xmin": chip_nos - 0.4,
        "xmax": chip_nos + 0.4,
        "discrete_deltaE": pd.Categorical(
            [_bin_deltaE(v) for v in delta_vals],
            categories=["<1", "<2", "<10", "<49", ">49"],
            ordered=True,
        ),
    })

    y_max = float(df["deltaE"].max()) * 1.1
    y_min = -1 * (y_max / 10)

    color_domain = ["<1", "<2", "<10", "<49", ">49"]
    color_range = ["#5AB45A", "#85BF40", "#C8C040", "#CC8800", "#CC5555"]

    bars = alt.Chart(df).mark_rect().encode(
        x=alt.X("xmin:Q", title="Color Chip",
                scale=alt.Scale(domain=[0.5, n_chips + 0.5]),
                axis=alt.Axis(values=list(range(1, n_chips + 1)))),
        x2="xmax:Q",
        y=alt.Y("deltaE:Q", scale=alt.Scale(domain=[y_min, y_max], nice=False), title="Delta E"),
        y2=alt.datum(0),
        color=alt.Color(
            "discrete_deltaE:O",
            scale=alt.Scale(domain=color_domain, range=color_range),
            title="Delta E",
        ),
        tooltip=["chip_no:Q", "deltaE:Q", "discrete_deltaE:O"],
    )
    hline_df = pd.DataFrame({
        "y": [1.0, 2.0, 10.0, 49.0],
        "stroke": ["#3D8C3D", "#5A9E28", "#A09000", "#CC7700"],
    })
    hlines = alt.Chart(hline_df).mark_rule(strokeDash=[8, 4]).encode(
        y="y:Q",
        color=alt.Color("stroke:N", scale=None),
    )
    swatch_chip_nos = (std_mat[:, 0] / 10).astype(int)
    swatch_hex = [
        f"{int(r * 255):02X}{int(g * 255):02X}{int(b * 255):02X}"
        for r, g, b in std_mat[:, 1:4]
    ]
    swatch_df = pd.DataFrame({
        "xmin": swatch_chip_nos - 0.5,
        "xmax": swatch_chip_nos + 0.5,
        "color": swatch_hex,
    })
    swatches = alt.Chart(swatch_df).mark_rect().encode(
        x=alt.X("xmin:Q", scale=alt.Scale(domain=[0.5, n_chips + 0.5])),
        x2="xmax:Q",
        y=alt.datum(y_min),
        y2=alt.datum(0),
        color=alt.Color("color:N", scale=None),
    )

    chart = (swatches + bars + hlines).properties(
        title="Delta E by Color Chip"
    ).resolve_scale(color="independent")

    _debug(
        visual=chart,
        filename=os.path.join(params.debug_outdir, str(params.device) + "_deltaE.png"),
    )
    return chart.interactive()
