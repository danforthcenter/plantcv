# Plot colorbar for pseudocolored images

import os

def plot_colorbar(outdir, filename, bins):
    """Plot colorbar for pseudocolored images

    Inputs:
    outdir   = Output directory
    filename = Figure filename
    bins     = Number of bins for color mapping

    :param outdir: str
    :param filename: str
    :param bins: int
    :return:
    """
    import matplotlib
    matplotlib.use('Agg', warn=False)
    from matplotlib import pyplot as plt
    from matplotlib import colors as colors
    from matplotlib import colorbar as colorbar

    fig_name = os.path.join(outdir, filename)
    fig = plt.figure()
    ax1 = fig.add_axes([0.05, 0.80, 0.9, 0.15])
    valmin = -0
    valmax = (bins - 1)
    norm = colors.Normalize(vmin=valmin, vmax=valmax)
    colorbar.ColorbarBase(ax1, cmap="viridis", norm=norm, orientation='horizontal')
    fig.savefig(fig_name, bbox_inches='tight')
    fig.clf()
