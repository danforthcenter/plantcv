"""Visualize delta E values for color checker chips in an image or set of images"""

import os
import math
import numpy as np
import pandas as pd
import altair as alt
from plantcv.plantcv._globals import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv.readimage import readimage
from plantcv.plantcv.transform.detect_color_card import deltaE
from plantcv.plantcv.transform.standard_matrices import std_color_matrix, astro_color_matrix


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


def plot_deltaE(source, n=20, ext="png", **kwargs):
    """Make a boxplot of deltaE per color chip across a set of images

    Parameters
    ----------
    source : numpy.ndarray, str, or list
        A numpy.ndarray will be treated as deltaE values from one image and a barplot will be made.
        Source for images, either an str filepath to a directory of images/subdirectories with images
        or a list of file paths to individual images, in these cases a boxplot will be made.
    n : int,
        Max number of images to read if source is an str filepath
    ext : str,
        File extension of images
    **kwargs : Further arguments passed to plantcv.plantcv.transform.deltaE
        Valid Keyword arguments:
        color_chip_size (None)
        roi (None)
        adaptive_method: 0 (mean) or 1 (Gaussian) (default = 1)
        block_size: int (default = 51)
        radius: int (default = 20)
        min_size: int (default = 1000)
        aspect_ratio: float (default = 1.27)
        solidity: float (default = 0.8)

    Returns
    -------
    chart = altair.vegalite.v5.api.LayerChart
        Altair layered chart with boxes for a dataset input or
        bars for a single image's deltaE values
        colored by deltaE category, reference lines,
        and standard chip color swatches below the x-axis
    """
    if isinstance(source, np.ndarray):
        chart = _plot_single_deltaE(source)
    else:
        chart = _plot_dataset_deltaE(source, n, ext, **kwargs)
    return chart.interactive()


def _plot_dataset_deltaE(source, n=20, ext="png", **kwargs):
    """Make a boxplot of deltaE per color chip across a set of images

    Parameters
    ----------
    source : str or list
        Source for images, either an str filepath to a directory of images/subdirectories with images
        or a list of file paths to individual images
    n : int,
        Max number of images to read if source is an str filepath
    ext : str,
        File extension of images
    **kwargs : Further arguments passed to plantcv.plantcv.transform.deltaE
        Valid Keyword arguments:
        color_chip_size (None)
        roi (None)
        adaptive_method: 0 (mean) or 1 (Gaussian) (default = 1)
        block_size: int (default = 51)
        radius: int (default = 20)
        min_size: int (default = 1000)
        aspect_ratio: float (default = 1.27)
        solidity: float (default = 0.8)

    Returns
    -------
    chart = altair.vegalite.v5.api.LayerChart
        Altair layered chart with boxes colored by deltaE category, reference lines,
        and standard chip color swatches below the x-axis
    """
    paths_to_imgs = source
    if isinstance(source, str):
        paths_to_imgs = []
        for root, _, files in os.walk(source):
            for file in files:
                if file.lower().endswith(ext) and len(paths_to_imgs) < n:
                    paths_to_imgs.append(os.path.join(root, file))
                    # store debug mode
    debug = params.debug
    params.debug = None
    # load and plot the set of images sequentially
    image_dfs = []
    for p in paths_to_imgs:
        img, _, _ = readimage(filename=p)
        de = deltaE(img, **kwargs)
        delta_vals = de.flatten(order="C")
        chip_nos = np.arange(1, len(delta_vals) + 1)
        iter_df = pd.DataFrame({
            "chip_no": chip_nos,
            "deltaE": delta_vals,
            "xmin": chip_nos - 0.4,
            "xmax": chip_nos + 0.4,
            "path": p,
            "discrete_deltaE": pd.Categorical(
                [_bin_deltaE(v) for v in delta_vals],
                categories=["<1", "<2", "<10", "<49", ">49"],
                ordered=True,
            ),
        })
        image_dfs.append(iter_df)
    df = pd.concat(image_dfs, ignore_index=True)
    n_chips = df["chip_no"].max()
    y_max = float(df["deltaE"].max()) * 1.1
    y_min = -1 * (y_max / 10)

    color_domain = ["<1", "<2", "<10", "<49", ">49"]
    color_range = ["#5AB45A", "#85BF40", "#C8C040", "#CC8800", "#CC5555"]

    x_scale = alt.Scale(domain=[0.5, n_chips + 0.5])
    x_axis = alt.Axis(values=list(range(1, n_chips + 1)), title="Color Chip")
    y_scale = alt.Scale(domain=[y_min, y_max], nice=False)

    boxes = alt.Chart(df).mark_boxplot(outliers=False, size=10).encode(
        x=alt.X("chip_no:Q", scale=x_scale, axis=x_axis),
        y=alt.Y("deltaE:Q", scale=y_scale, title="Delta E"),
    )
    points = alt.Chart(df).transform_calculate(
        jitter="datum.chip_no + (random() - 0.5) * 0.5"
    ).mark_circle(opacity=0.4, size=20).encode(
        x=alt.X("jitter:Q", scale=x_scale, axis=x_axis),
        y=alt.Y("deltaE:Q", scale=y_scale),
        color=alt.Color(
            "discrete_deltaE:O",
            scale=alt.Scale(domain=color_domain, range=color_range),
            title="Delta E",
        ),
        tooltip=[alt.Tooltip("path:N", title="Image"),
                 alt.Tooltip("chip_no:Q", title="Chip"),
                 alt.Tooltip("deltaE:Q", title="Delta E")],
    )
    hline_df = pd.DataFrame({
        "y": [1.0, 2.0, 10.0, 49.0],
        "stroke": ["#3D8C3D", "#5A9E28", "#A09000", "#CC7700"],
    })
    hline_df = hline_df.loc[hline_df['y'] <= max([1, df["deltaE"].max()])]
    hlines = alt.Chart(hline_df).mark_rule(strokeDash=[8, 4]).encode(
        y="y:Q",
        color=alt.Color("stroke:N", scale=None),
    )
    std_mat = std_color_matrix(pos=3)
    if n_chips == 15:
        std_mat = astro_color_matrix()
    swatch_chip_nos = (std_mat[:, 0] / 10).astype(int)
    swatch_hex = [
        f"#{int(r * 255):02X}{int(g * 255):02X}{int(b * 255):02X}"
        for r, g, b in std_mat[:, 1:4]
    ]
    swatch_df = pd.DataFrame({
        "xmin": swatch_chip_nos - 0.5,
        "xmax": swatch_chip_nos + 0.5,
        "color": swatch_hex,
    })
    swatches = alt.Chart(swatch_df).mark_rect().encode(
        x=alt.X("xmin:Q", scale=x_scale),
        x2="xmax:Q",
        y=alt.datum(y_min),
        y2=alt.datum(0),
        color=alt.Color("color:N", scale=None),
    )
    plot = (swatches + boxes + points + hlines).properties(
        title="Delta E by Color Chip"
    ).resolve_scale(color="independent")
    # reset debug
    params.debug = debug
    return plot


def _plot_single_deltaE(deltaE_matrix):
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
    hline_df = hline_df.loc[hline_df['y'] <= max([1, df["deltaE"].max()])]
    hlines = alt.Chart(hline_df).mark_rule(strokeDash=[8, 4]).encode(
        y="y:Q",
        color=alt.Color("stroke:N", scale=None),
    )
    swatch_chip_nos = (std_mat[:, 0] / 10).astype(int)
    swatch_hex = [
        f"#{int(r * 255):02X}{int(g * 255):02X}{int(b * 255):02X}"
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
    return chart
