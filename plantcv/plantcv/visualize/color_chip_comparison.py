# Visualize a scatter plot representation of color correction

import pandas as pd
from altair as alt


def color_chip_comparison(std_matrix, **kwargs):
    """
    Plot 4 panels showing the difference in observed vs expected colors and optionally
    the calibrated colors in a color card.
    The color of each dot is given by the RGB value either of the original image, known color card, or corrected image.

    Parameters
    ----------
    std_matrix   : numpy.ndarray
                   Output from pcv.transform.std_color_matrix
    **kwargs: list of numpy.ndarrays
                   Output from pcv.transform.get_color_matrix

    Returns
    -------
    altair.vegalite.v5.api.VConcatChart of color chip greenness ranks between observed and expected values.
    """
    # make standard color matrix into a rescaled dataframe
    stddf = pd.DataFrame(stdmat)
    stddf.columns = ['chip', 'R', 'G', 'B']
    stddf["card"] = "std"
    stddf["std_R"] = stddf["R"] * 255
    stddf["std_G"] = stddf["G"] * 255
    stddf["std_B"] = stddf["B"] * 255
    # initialize a list of like dataframes
    df_list = [stddf]
    # format and append all kwargs into list of dataframes
    for i, mat in enumerate(**kwargs):
        df = pd.DataFrame(mat)
        df.columns = ['chip', 'R', 'G', 'B']
        df["card"] = f"card {i + 1}"
        df["std_R"] = stddf["std_R"]
        df["std_G"] = stddf["std_G"]
        df["std_B"] = stddf["std_B"]
        df_list.append(df)
    # rbind all dataframes from list
    fulldf = pd.concat(*[df_list], ignore_index = True)
    # rescale rgb values to 0-255
    fulldf["R"] = fulldf["R"] * 255
    fulldf["G"] = fulldf["G"] * 255
    fulldf["B"] = fulldf["B"] * 255
    # calculate greenness, in the future maybe a named metric.
    fulldf["greenness"] = fulldf["G"] / (fulldf["R"] + fulldf["G"] + fulldf["B"])
    # rank greenness, chips should have same order in any "healthy" card
    fulldf["greenness_rank"] = fulldf.groupby("card")["greenness"].rank(method="first",
                                                                        ascending=False)
    # make standard greenness and rank it
    fulldf["std_greenness"] = fulldf["std_G"] / (fulldf["std_R"] +
                                                 fulldf["std_G"] +
                                                 fulldf["std_B"])
    fulldf["std_greenness_rank"] = fulldf.groupby("card")["std_greenness"].rank(method="first",
                                                                                ascending=False)
    # label chips 1 to 24
    fulldf["chip"] = fulldf["chip"] / 10
    # initiate base of upper color chip chart
    base = alt.Chart(fulldf).encode(
        alt.X("card:O",
              axis = alt.Axis(grid=False, ticks=False,
                              domain = False, labels = False, title = None)
              ).scale(paddingInner=0),
        alt.Y("greenness_rank:O", title = "Greenness Rank").scale(paddingInner=0),
    ).properties(
        height=300,
        width=500
    )
    # make rect layer of observed colors
    tiles1 = base.mark_rect(width = alt.RelativeBandSize(0.6), align = "left").encode(
        color=alt.value(alt.ExprRef(alt.expr.rgb(alt.datum.R, alt.datum.G, alt.datum.B))),
    )
    # make rect layer of standard colors
    tiles2 = base.mark_rect(width = alt.RelativeBandSize(0.3), align = "right").encode(
        color=alt.value(alt.ExprRef(alt.expr.rgb(alt.datum.std_R,
                                                 alt.datum.std_G,
                                                 alt.datum.std_B))),
    )
    # make text layer to label chip numbers
    text = base.mark_text(baseline="middle", align = "center").encode(
        text="chip:Q",
        color=alt.value("white")
    )
    # combine rect and text layers
    upper = tiles1 + tiles2 + text
    # initialize list of margin plots
    margin_plots = []
    # for each kwarg matrix and std matrix make a margin plot of residual ranks
    for i in range(0, len(**kwargs) + 1):
        # select card
        whichcard = f"card {i + 1}"
        if i + 1 > len(**kwargs):
            whichcard = "std"
        sub1 = fulldf[fulldf["card"] == whichcard]
        # initialize plot
        subbase = alt.Chart(sub1).encode(
            alt.X("std_greenness_rank:Q"),
            alt.Y("std_greenness_rank:Q")
        ).properties(
            height= 500 / (10/9 * len(obs_matrices) + 1),
            width = 500 / (10/9 * len(obs_matrices) + 1),
            title = whichcard
        )
        # make line+points layer of observed vs expected ranks
        subpoints = subbase.mark_line(point = True, strokeWidth = 1.25, strokeDash = [5, 5]).encode(
            x = alt.X("greenness_rank:Q",
                      axis = alt.Axis(grid=False, ticks=False, domain = False, labels = False, title = None)),
            y = alt.Y("std_greenness_rank:Q",
                      axis = alt.Axis(grid=False, ticks=False, domain = False, labels = False, title = None))
        )
        # draw expected line with slope 1
        sublinear = subbase.mark_line(color = "black", strokeWidth = 0.5).encode(
            x = alt.X("std_greenness_rank:Q",
                      axis = alt.Axis(grid=False, ticks=False, domain = False, labels = False, title = None)),
            y = alt.Y("std_greenness_rank:Q",
                      axis = alt.Axis(grid=False, ticks=False, domain = False, labels = False, title = None))
        )
        # combine layers
        iterchart = subpoints + sublinear
        # add to list of margin plots for combination
        margin_plots.append(iterchart)
    # combine tile plot and margin plots
    out = alt.vconcat(upper, alt.hconcat(*margin_plots, spacing = 5))
