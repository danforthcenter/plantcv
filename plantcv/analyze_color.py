# Analyze Color of Object

import os
import cv2
import numpy as np
from . import print_image
from . import plot_image
from . import fatal_error
from . import plot_colorbar


def _pseudocolored_image(device, histogram, bins, img, mask, background, channel, filename, resolution,
                         analysis_images, debug):
    """Pseudocolor image.

    Inputs:
    histogram       = a normalized histogram of color values from one color channel
    bins            = number of color bins the channel is divided into
    img             = input image
    mask            = binary mask image
    background      = what background image?: channel image (img) or white
    channel         = color channel name
    filename        = input image filename
    resolution      = output image resolution
    analysis_images = list of analysis image filenames
    debug           = print or plot. Print = save to file, Plot = print to screen.

    Returns:
    analysis_images = list of analysis image filenames

    :param histogram: list
    :param bins: int
    :param img: numpy array
    :param mask: numpy array
    :param background: str
    :param channel: str
    :param filename: str
    :param resolution: int
    :param analysis_images: list
    :return analysis_images: list
    """
    mask_inv = cv2.bitwise_not(mask)

    cplant = cv2.applyColorMap(histogram, colormap=2)
    cplant1 = cv2.bitwise_and(cplant, cplant, mask=mask)

    output_imgs = {"pseudo_on_img": {"background": "img", "img": None},
                   "pseudo_on_white": {"background": "white", "img": None}}

    if background == 'img' or background == 'both':
        # mask the background and color the plant with color scheme 'jet'
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img_back = cv2.bitwise_and(img_gray, img_gray, mask=mask_inv)
        img_back3 = np.dstack((img_back, img_back, img_back))

        output_imgs["pseudo_on_img"]["img"] = cv2.add(cplant1, img_back3)

    if background == 'white' or background == 'both':
        # Get the image size
        if np.shape(img)[2] == 3:
            ix, iy, iz = np.shape(img)
        else:
            ix, iy = np.shape(img)
        size = ix, iy
        back = np.zeros(size, dtype=np.uint8)
        w_back = back + 255
        w_back3 = np.dstack((w_back, w_back, w_back))
        img_back3 = cv2.bitwise_and(w_back3, w_back3, mask=mask_inv)
        output_imgs["pseudo_on_white"]["img"] = cv2.add(cplant1, img_back3)

    if filename:
        for key in output_imgs:
            if output_imgs[key]["img"] is not None:
                fig_name_pseudo = str(filename[0:-4]) + '_' + str(channel) + '_pseudo_on_' + \
                                  output_imgs[key]["background"] + '.jpg'
                path = os.path.dirname(filename)
                print_image(output_imgs[key]["img"], fig_name_pseudo)
                analysis_images.append(['IMAGE', 'pseudo', fig_name_pseudo])
    else:
        path = "."
        
    if debug is not None:
        if debug == 'print':
            for key in output_imgs:
                if output_imgs[key]["img"] is not None:
                    print_image(output_imgs[key]["img"], (str(device) + "_" + output_imgs[key]["background"] +
                                                          '_pseudocolor.jpg'))
            fig_name = 'VIS_pseudocolor_colorbar_' + str(channel) + '_channel.svg'
            if not os.path.isfile(path + '/' + fig_name):
                plot_colorbar(path, fig_name, bins)
        elif debug == 'plot':
            for key in output_imgs:
                if output_imgs[key]["img"] is not None:
                    plot_image(output_imgs[key]["img"])

    return analysis_images


def analyze_color(img, imgname, mask, bins, device, debug=None, hist_plot_type=None, pseudo_channel='v',
                  pseudo_bkg='img', resolution=300, filename=False):
    """Analyze the color properties of an image object

    Inputs:
    img              = image
    imgname          = name of input image
    mask             = mask made from selected contours
    device           = device number. Used to count steps in the pipeline
    debug            = None, print, or plot. Print = save to file, Plot = print to screen.
    hist_plot_type   = 'None', 'all', 'rgb','lab' or 'hsv'
    color_slice_type = 'None', 'rgb', 'hsv' or 'lab'
    pseudo_channel   = 'None', 'l', 'm' (green-magenta), 'y' (blue-yellow), h','s', or 'v', creates pseduocolored image
                       based on the specified channel
    pseudo_bkg       = 'img' => channel image, 'white' => white background image, 'both' => both img and white options
    filename         = False or image name. If defined print image

    Returns:
    device           = device number
    hist_header      = color histogram data table headers
    hist_data        = color histogram data table values
    analysis_images  = list of output images

    :param img: numpy array
    :param imgname: str
    :param mask: numpy array
    :param bins: int
    :param device: int
    :param debug: str
    :param hist_plot_type: str
    :param pseudo_channel: str
    :param pseudo_bkg: str
    :param resolution: int
    :param filename: str
    :return device: int
    :return hist_header: list
    :return hist_data: list
    :return analysis_images: list
    """
    device += 1

    masked = cv2.bitwise_and(img, img, mask=mask)
    b, g, r = cv2.split(masked)
    lab = cv2.cvtColor(masked, cv2.COLOR_BGR2LAB)
    l, m, y = cv2.split(lab)
    hsv = cv2.cvtColor(masked, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    graph_color = ('blue', 'forestgreen', 'red', 'dimgray', 'magenta', 'yellow', 'blueviolet', 'cyan', 'orange')
    label = ('blue', 'green', 'red', 'lightness', 'green-magenta', 'blue-yellow', 'hue', 'saturation', 'value')

    # Create Color Histogram Data
    norm_channels = {"b": b / (256 / bins),
                     "g": g / (256 / bins),
                     "r": r / (256 / bins),
                     "l": l / (256 / bins),
                     "m": m / (256 / bins),
                     "y": y / (256 / bins),
                     "h": h / (256 / bins),
                     "s": s / (256 / bins),
                     "v": v / (256 / bins)
                     }

    if pseudo_channel is not None and pseudo_channel not in norm_channels:
        fatal_error("Pseudocolor channel was " + str(pseudo_channel) +
                    ', but can only be one of the following: None, "l", "m", "y", "h", "s" or "v"!')
    if pseudo_bkg not in ["white", "img", "both"]:
        fatal_error("The pseudocolored image background was " + str(pseudo_bkg) +
                    ', but can only be one of the following: "white", "img", or "both"!')

    hist_b = cv2.calcHist([norm_channels["b"]], [0], mask, [bins], [0, (bins - 1)])
    hist_g = cv2.calcHist([norm_channels["g"]], [0], mask, [bins], [0, (bins - 1)])
    hist_r = cv2.calcHist([norm_channels["r"]], [0], mask, [bins], [0, (bins - 1)])
    hist_l = cv2.calcHist([norm_channels["l"]], [0], mask, [bins], [0, (bins - 1)])
    hist_m = cv2.calcHist([norm_channels["m"]], [0], mask, [bins], [0, (bins - 1)])
    hist_y = cv2.calcHist([norm_channels["y"]], [0], mask, [bins], [0, (bins - 1)])
    hist_h = cv2.calcHist([norm_channels["h"]], [0], mask, [bins], [0, (bins - 1)])
    hist_s = cv2.calcHist([norm_channels["s"]], [0], mask, [bins], [0, (bins - 1)])
    hist_v = cv2.calcHist([norm_channels["v"]], [0], mask, [bins], [0, (bins - 1)])

    hist_data_b = [l[0] for l in hist_b]
    hist_data_g = [l[0] for l in hist_g]
    hist_data_r = [l[0] for l in hist_r]
    hist_data_l = [l[0] for l in hist_l]
    hist_data_m = [l[0] for l in hist_m]
    hist_data_y = [l[0] for l in hist_y]
    hist_data_h = [l[0] for l in hist_h]
    hist_data_s = [l[0] for l in hist_s]
    hist_data_v = [l[0] for l in hist_v]

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

    analysis_images = []

    if pseudo_channel is not None:
        analysis_images = _pseudocolored_image(device, norm_channels[pseudo_channel], bins, img, mask, pseudo_bkg,
                                               pseudo_channel, filename, resolution, analysis_images, debug)

    if hist_plot_type is not None:
        import matplotlib
        matplotlib.use('Agg')
        from matplotlib import pyplot as plt

        # Create Histogram Plot
        if filename:
            if hist_plot_type == 'all':
                plt.plot(hist_b, color=graph_color[0], label=label[0])
                plt.plot(hist_g, color=graph_color[1], label=label[1])
                plt.plot(hist_r, color=graph_color[2], label=label[2])
                plt.plot(hist_l, color=graph_color[3], label=label[3])
                plt.plot(hist_m, color=graph_color[4], label=label[4])
                plt.plot(hist_y, color=graph_color[5], label=label[5])
                plt.plot(hist_h, color=graph_color[6], label=label[6])
                plt.plot(hist_s, color=graph_color[7], label=label[7])
                plt.plot(hist_v, color=graph_color[8], label=label[8])
                plt.xlim([0, (bins - 1)])
                plt.legend()
            elif hist_plot_type == 'rgb':
                plt.plot(hist_b, color=graph_color[0], label=label[0])
                plt.plot(hist_g, color=graph_color[1], label=label[1])
                plt.plot(hist_r, color=graph_color[2], label=label[2])
                plt.xlim([0, (bins - 1)])
                plt.legend()
            elif hist_plot_type == 'lab':
                plt.plot(hist_l, color=graph_color[3], label=label[3])
                plt.plot(hist_m, color=graph_color[4], label=label[4])
                plt.plot(hist_y, color=graph_color[5], label=label[5])
                plt.xlim([0, (bins - 1)])
                plt.legend()
            elif hist_plot_type == 'hsv':
                plt.plot(hist_h, color=graph_color[6], label=label[6])
                plt.plot(hist_s, color=graph_color[7], label=label[7])
                plt.plot(hist_v, color=graph_color[8], label=label[8])
                plt.xlim([0, (bins - 1)])
                plt.legend()
            elif hist_plot_type == None:
                pass
            else:
                fatal_error(
                    'Histogram Plot Type' + str(hist_plot_type) + ' is not "none", "all","rgb", "lab" or "hsv"!')

            # Print plot
            fig_name = (str(filename[0:-4]) + '_' + str(hist_plot_type) + '_hist.svg')
            plt.savefig(fig_name)
            analysis_images.append(['IMAGE', 'hist', fig_name])
            if debug == 'print':
                fig_name = (str(device) + '_' + str(hist_plot_type) + '_hist.svg')
                plt.savefig(fig_name)
            plt.clf()

    return device, hist_header, hist_data, analysis_images
