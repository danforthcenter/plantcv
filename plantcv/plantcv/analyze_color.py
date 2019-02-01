# Analyze Color of Object

# import os
import cv2
import numpy as np
import pandas as pd
# from plantcv.plantcv import print_image
# from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
# from plantcv.plantcv import plot_colorbar
from plantcv.plantcv import params


# def _pseudocolored_image(histogram, bins, img, mask, background, channel, filename, analysis_images):
#     """Pseudocolor image.

#     Inputs:
#     histogram       = a normalized histogram of color values from one color channel
#     bins            = number of color bins the channel is divided into
#     img             = input image
#     mask            = binary mask image
#     background      = what background image?: channel image (img) or white
#     channel         = color channel name
#     filename        = input image filename
#     analysis_images = list of analysis image filenames

#     Returns:
#     analysis_images = list of analysis image filenames

#     :param histogram: list
#     :param bins: int
#     :param img: numpy array
#     :param mask: numpy array
#     :param background: str
#     :param channel: str
#     :param filename: str
#     :param analysis_images: list
#     :return analysis_images: list
#     """
#     mask_inv = cv2.bitwise_not(mask)

#     cplant = cv2.applyColorMap(histogram, colormap=2)
#     cplant1 = cv2.bitwise_and(cplant, cplant, mask=mask)

#     output_imgs = {"pseudo_on_img": {"background": "img", "img": None},
#                    "pseudo_on_white": {"background": "white", "img": None}}

#     if background == 'img' or background == 'both':
#         # mask the background and color the plant with color scheme 'jet'
#         img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#         img_back = cv2.bitwise_and(img_gray, img_gray, mask=mask_inv)
#         img_back3 = np.dstack((img_back, img_back, img_back))

#         output_imgs["pseudo_on_img"]["img"] = cv2.add(cplant1, img_back3)

#     if background == 'white' or background == 'both':
#         ix, iy, iz = np.shape(img)
#         size = ix, iy
#         back = np.zeros(size, dtype=np.uint8)
#         w_back = back + 255
#         w_back3 = np.dstack((w_back, w_back, w_back))
#         img_back3 = cv2.bitwise_and(w_back3, w_back3, mask=mask_inv)
#         output_imgs["pseudo_on_white"]["img"] = cv2.add(cplant1, img_back3)

#     if filename:
#         for key in output_imgs:
#             if output_imgs[key]["img"] is not None:
#                 fig_name_pseudo = os.path.splitext(filename)[0] + '_' + str(channel) + '_pseudo_on_' + \
#                                   output_imgs[key]["background"] + '.jpg'
#                 path = os.path.dirname(filename)
#                 print_image(output_imgs[key]["img"], fig_name_pseudo)
#                 analysis_images.append(['IMAGE', 'pseudo', fig_name_pseudo])
#     else:
#         path = "."

#     if params.debug is not None:
#         if params.debug == 'print':
#             for key in output_imgs:
#                 if output_imgs[key]["img"] is not None:
#                     print_image(output_imgs[key]["img"], os.path.join(params.debug_outdir, str(params.device) +
#                                                                       "_" + output_imgs[key]["background"] +
#                                                                       '_pseudocolor.jpg'))
#             fig_name = 'VIS_pseudocolor_colorbar_' + str(channel) + '_channel.svg'
#             if not os.path.isfile(os.path.join(params.debug_outdir, fig_name)):
#                 plot_colorbar(path, fig_name, bins)
#         elif params.debug == 'plot':
#             for key in output_imgs:
#                 if output_imgs[key]["img"] is not None:
#                     plot_image(output_imgs[key]["img"])

#     return analysis_images


def analyze_color(rgb_img, mask, bins, hist_plot_type=None):
    """Analyze the color properties of an image object

    Inputs:
    rgb_img          = RGB image data
    mask             = Binary mask made from selected contours
    bins             = number of color bins the channel is divided into
    hist_plot_type   = 'None', 'all', 'rgb','lab' or 'hsv'

    Returns:
    hist_header      = color histogram data table headers
    hist_data        = color histogram data table values
    analysis_image   = histogram output

    :param rgb_img: numpy.ndarray
    :param mask: numpy.ndarray
    :param bins: int
    :param hist_plot_type: str
    :return hist_header: list
    :return hist_data: list
    :return analysis_images: list
    """
    import matplotlib
    matplotlib.use('Agg', warn=False)
    # from matplotlib import pyplot as plt
    from plotnine import ggplot, aes, geom_line, scale_x_continuous, scale_color_manual

    params.device += 1

    if len(np.shape(rgb_img)) < 3:
        fatal_error("rgb_img must be an RGB image")

    masked = cv2.bitwise_and(rgb_img, rgb_img, mask=mask)
    b, g, r = cv2.split(masked)
    lab = cv2.cvtColor(masked, cv2.COLOR_BGR2LAB)
    l, m, y = cv2.split(lab)
    hsv = cv2.cvtColor(masked, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # Color channel dictionary
    norm_channels = {"b": np.divide(b, (256 / bins)).astype(np.uint8),
                     "g": np.divide(g, (256 / bins)).astype(np.uint8),
                     "r": np.divide(r, (256 / bins)).astype(np.uint8),
                     "l": np.divide(l, (256 / bins)).astype(np.uint8),
                     "m": np.divide(m, (256 / bins)).astype(np.uint8),
                     "y": np.divide(y, (256 / bins)).astype(np.uint8),
                     "h": np.divide(h, (256 / bins)).astype(np.uint8),
                     "s": np.divide(s, (256 / bins)).astype(np.uint8),
                     "v": np.divide(v, (256 / bins)).astype(np.uint8)
                     }

    # Histogram plot types
    hist_types = {"all": ("b", "g", "r", "l", "m", "y", "h", "s", "v"),
                  "rgb": ("b", "g", "r"),
                  "lab": ("l", "m", "y"),
                  "hsv": ("h", "s", "v")}

    # # If the user-input pseudo_channel is not None and is not found in the list of accepted channels, exit
    # if pseudo_channel is not None and pseudo_channel not in norm_channels:
    #     fatal_error("Pseudocolor channel was " + str(pseudo_channel) +
    #                 ', but can only be one of the following: None, "l", "m", "y", "h", "s" or "v"!')
    # # If the user-input pseudocolored image background is not in the accepted input list, exit
    # if pseudo_bkg not in ["white", "img", "both"]:
    #     fatal_error("The pseudocolored image background was " + str(pseudo_bkg) +
    #                 ', but can only be one of the following: "white", "img", or "both"!')
    # # If the user-input histogram color-channel plot type is not in the list of accepted channels, exit
    if hist_plot_type is not None and hist_plot_type not in hist_types:
        fatal_error("The histogram plot type was " + str(hist_plot_type) +
                    ', but can only be one of the following: None, "all", "rgb", "lab", or "hsv"!')
    histograms = {
        "b": {"label": "blue", "graph_color": "blue",
              "hist": cv2.calcHist([norm_channels["b"]], [0], mask, [bins], [0, (bins - 1)])},
        "g": {"label": "green", "graph_color": "forestgreen",
              "hist": cv2.calcHist([norm_channels["g"]], [0], mask, [bins], [0, (bins - 1)])},
        "r": {"label": "red", "graph_color": "red",
              "hist": cv2.calcHist([norm_channels["r"]], [0], mask, [bins], [0, (bins - 1)])},
        "l": {"label": "lightness", "graph_color": "dimgray",
              "hist": cv2.calcHist([norm_channels["l"]], [0], mask, [bins], [0, (bins - 1)])},
        "m": {"label": "green-magenta", "graph_color": "magenta",
              "hist": cv2.calcHist([norm_channels["m"]], [0], mask, [bins], [0, (bins - 1)])},
        "y": {"label": "blue-yellow", "graph_color": "yellow",
              "hist": cv2.calcHist([norm_channels["y"]], [0], mask, [bins], [0, (bins - 1)])},
        "h": {"label": "hue", "graph_color": "blueviolet",
              "hist": cv2.calcHist([norm_channels["h"]], [0], mask, [bins], [0, (bins - 1)])},
        "s": {"label": "saturation", "graph_color": "cyan",
              "hist": cv2.calcHist([norm_channels["s"]], [0], mask, [bins], [0, (bins - 1)])},
        "v": {"label": "value", "graph_color": "orange",
              "hist": cv2.calcHist([norm_channels["v"]], [0], mask, [bins], [0, (bins - 1)])}
    }

    hist_data_b = [l[0] for l in histograms["b"]["hist"]]
    hist_data_g = [l[0] for l in histograms["g"]["hist"]]
    hist_data_r = [l[0] for l in histograms["r"]["hist"]]
    hist_data_l = [l[0] for l in histograms["l"]["hist"]]
    hist_data_m = [l[0] for l in histograms["m"]["hist"]]
    hist_data_y = [l[0] for l in histograms["y"]["hist"]]
    hist_data_h = [l[0] for l in histograms["h"]["hist"]]
    hist_data_s = [l[0] for l in histograms["s"]["hist"]]
    hist_data_v = [l[0] for l in histograms["v"]["hist"]]

    binval = np.arange(0, bins)
    bin_values = [l for l in binval]

    # Store Color Histogram Data
    hist_header = [
        'HEADER_HISTOGRAM',
        'bin-number',
        'bin-values',
        'blue',
        'green',
        'red',
        'lightness',
        'green-magenta',
        'blue-yellow',
        'hue',
        'saturation',
        'value'
    ]

    hist_data = [
        'HISTOGRAM_DATA',
        bins,
        bin_values,
        hist_data_b,
        hist_data_g,
        hist_data_r,
        hist_data_l,
        hist_data_m,
        hist_data_y,
        hist_data_h,
        hist_data_s,
        hist_data_v
    ]

    # if pseudo_channel is not None:
    #         analysis_images = _pseudocolored_image(norm_channels[pseudo_channel], bins, rgb_img, mask, pseudo_bkg,
    #                                                pseudo_channel, filename, analysis_images)
    analysis_image = []
    dataset = pd.DataFrame({'bins': binval, 'blue': hist_data_b,
                            'green': hist_data_g, 'red': hist_data_r,
                            'lightness': hist_data_l, 'green-magenta': hist_data_m,
                            'blue-yellow': hist_data_y, 'hue': hist_data_h,
                            'saturation': hist_data_s, 'value': hist_data_v})

    # Make the histogram figure using plotnine
    if hist_plot_type is not None:
        if hist_plot_type == 'rgb':
            df_rgb = pd.melt(dataset, id_vars=['bins'], value_vars=['blue', 'green', 'red'],
                             var_name='Color Channel', value_name='Pixels')
            hist_fig = (ggplot(df_rgb, aes(x='bins', y='Pixels', color='Color Channel'))
                        + geom_line()
                        + scale_x_continuous(breaks=list(range(0, bins, 25)))
                        + scale_color_manual(['blue', 'green', 'red'])
                        )
            analysis_image.append(hist_fig)

        elif hist_plot_type == 'lab':
            df_lab = pd.melt(dataset, id_vars=['bins'],
                             value_vars=['lightness', 'green-magenta', 'blue-yellow'],
                             var_name='Color Channel', value_name='Pixels')
            hist_fig = (ggplot(df_lab, aes(x='bins', y='Pixels', color='Color Channel'))
                        + geom_line()
                        + scale_x_continuous(breaks=list(range(0, bins, 25)))
                        + scale_color_manual(['yellow', 'magenta', 'dimgray'])
                        )
            analysis_image.append(hist_fig)

        elif hist_plot_type == 'hsv':
            df_hsv = pd.melt(dataset, id_vars=['bins'],
                             value_vars=['hue', 'saturation', 'value'],
                             var_name='Color Channel', value_name='Pixels')
            hist_fig = (ggplot(df_hsv, aes(x='bins', y='Pixels', color='Color Channel'))
                        + geom_line()
                        + scale_x_continuous(breaks=list(range(0, bins, 25)))
                        + scale_color_manual(['blueviolet', 'cyan', 'orange'])
                        )
            analysis_image.append(hist_fig)

        elif hist_plot_type == 'all':
            s = pd.Series(['blue', 'green', 'red', 'lightness', 'green-magenta',
                           'blue-yellow', 'hue', 'saturation', 'value'], dtype="category")
            color_channels = ['blue', 'yellow', 'green', 'magenta', 'blueviolet',
                              'dimgray', 'red', 'cyan', 'orange']
            df_all = pd.melt(dataset, id_vars=['bins'], value_vars=s, var_name='Color Channel',
                             value_name='Pixels')
            hist_fig = (ggplot(df_all, aes(x='bins', y='Pixels', color='Color Channel'))
                        + geom_line()
                        + scale_x_continuous(breaks=list(range(0, bins, 25)))
                        + scale_color_manual(color_channels)
                        )
            analysis_image.append(hist_fig)

            #     if hist_plot_type is not None:
            #         # Create Histogram Plot
            #         for channel in hist_types[hist_plot_type]:
            #             plt.plot(histograms[channel]["hist"], color=histograms[channel]["graph_color"],
            #                      label=histograms[channel]["label"])
            #             plt.xlim([0, bins - 1])
            #             plt.legend()
            #         # Print plot
            #         fig_name = (os.path.splitext(filename)[0] + '_' + str(hist_plot_type) + '_hist.svg')
            #         plt.savefig(fig_name)
            #         analysis_images.append(['IMAGE', 'hist', fig_name])
            #         if params.debug == 'print':
            #             fig_name = os.path.join(params.debug_outdir, str(params.device) + '_' + str(hist_plot_type)
            #                        + '_hist.svg')
            #             plt.savefig(fig_name)
            #         plt.clf()

    return hist_header, hist_data, analysis_image
