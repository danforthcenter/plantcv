# Visualize a scatter plot representation of color correction

import numpy as np
from matplotlib import pyplot as plt
from plantcv.plantcv._helpers import _rgb2gray


def color_correction_plot(color_matrix, std_matrix, corrected_matrix=None):
    """
    Plot 4 panels showing the difference in observed vs expected colors and optionally
    the calibrated colors in a color card.
    The color of each dot is given by the RGB value either of the original image, known color card, or corrected image.

    Parameters
    ----------
    color_matrix : tuple of numpy.ndarrays
                   Output from pcv.transform.get_color_matrix
    std_matrix   : numpy.ndarray
                   Output from pcv.transform.std_color_matrix
    corrected_matrix: tuple of numpy.ndarrays
                   Output from pcv.transform.get_color_matrix on a corrected image

    Returns
    -------
    matplotlib pyplot Figure object of the visualization
         Scatterplot of points
    matplotlib pyplot Axes object of the visualization
         Labels and axes
    """
    # default is that there is no corrected matrix
    use_corrected = False
    if corrected_matrix is not None:
        use_corrected = True
    # set up plot margins and labels
    fig, axs = plt.subplots(2, 2)
    panels = [[0, 0], [0, 1], [1, 0], [1, 1]]
    panel_titles = ["Red", "Green", "Blue", "Grayscale"]
    fig.suptitle("Standard vs Observed Color Card")
    # for each panel, make a plot
    for p in range(0, len(panels) - 1, 1):
        c = p + 1
        for i in range(0, len(std_matrix), 1):
            axs[*panels[p]].plot(
                [255 * std_matrix[i, c], 255 * std_matrix[i, c]],
                [255 * std_matrix[i, c], 255 * color_matrix[1][i, c]],
                linestyle="--",
                linewidth=0.5,
                c="#666666",
            )
        axs[*panels[p]].plot(
            [0, 255], [0, 255], c="#666666", linewidth=1, linestyle="--"
        )
        axs[*panels[p]].scatter(
            255 * std_matrix[:, c],
            255 * color_matrix[1][:, c],
            c=color_matrix[1][:, 1:4],
            edgecolors=color_matrix[1][:, 1:4],
            s=8,
        )
        if use_corrected:
            axs[*panels[p]].scatter(
                255 * std_matrix[:, c],
                255 * corrected_matrix[1][:, c],
                c=corrected_matrix[1][:, 1:4],
                edgecolors=corrected_matrix[1][:, 1:4],
                s=8,
                marker="*",
            )
        axs[*panels[p]].scatter(
            255 * std_matrix[:, c],
            255 * std_matrix[:, c],
            c=std_matrix[:, 1:4],
            s=8,
        )
        axs[*panels[p]].set(xlabel="Expected", ylabel="Observed")
        axs[*panels[p]].set_title(panel_titles[p])
    # grayscale panel
    graystd = _rgb2gray(
        np.transpose(
            np.array(
                [[std_matrix[:, 1]], [std_matrix[:, 2]], [std_matrix[:, 3]]]
            ).astype("float32")
        )
    )
    graymat = _rgb2gray(
        np.transpose(
            np.array(
                [
                    [color_matrix[1][:, 1]],
                    [color_matrix[1][:, 2]],
                    [color_matrix[1][:, 3]],
                ]
            ).astype("float32")
        )
    )
    graycc = _rgb2gray(
        np.transpose(
            np.array(
                [
                    [corrected_matrix[1][:, 1]],
                    [corrected_matrix[1][:, 2]],
                    [corrected_matrix[1][:, 3]],
                ]
            ).astype("float32")
        )
    )
    for i in range(0, len(graystd), 1):
        axs[*panels[3]].plot(
            [255 * graystd[i], 255 * graystd[i]],
            [255 * graystd[i], 255 * graymat[i]],
            linestyle="--",
            linewidth=0.5,
            c="#666666",
        )
        axs[*panels[3]].plot(
            [0, 255], [0, 255], c="#666666", linewidth=1, linestyle="--"
        )
        axs[*panels[3]].scatter(
            255 * graystd,
            255 * graymat,
            c=color_matrix[1][:, 1:4],
            edgecolors=color_matrix[1][:, 1:4],
            s=8,
        )
        if use_corrected:
            axs[*panels[3]].scatter(
                255 * graystd,
                255 * graycc,
                c=corrected_matrix[1][:, 1:4],
                edgecolors=corrected_matrix[1][:, 1:4],
                s=8,
                marker="*",
            )
        axs[*panels[3]].scatter(255 * graystd, 255 * graystd, c=std_matrix[:, 1:4], s=8)
        axs[*panels[3]].set(xlabel="Expected", ylabel="Observed")
        axs[*panels[3]].set_title(panel_titles[3])
    # layout panels
    fig.tight_layout()

    return fig, axs
