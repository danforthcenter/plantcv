# Analyze Color of Object

import os
import cv2
import numpy as np
from . import print_image
from . import fatal_error


def _pseudocolored_image(histogram, bins, img, mask, background, channel, filename, resolution, analysis_images):
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

    # Get the image size
    if np.shape(img)[2] == 3:
        ix, iy, iz = np.shape(img)
    else:
        ix, iy = np.shape(img)
    size = ix, iy

    back = np.zeros(size, dtype=np.uint8)
    w_back = back + 255
    w_back3 = np.dstack((w_back, w_back, w_back))

    mask_inv = cv2.bitwise_not(mask)

    cplant = cv2.applyColorMap(histogram, colormap=2)
    cplant1 = cv2.bitwise_and(cplant, cplant, mask=mask)

    if background == 'img':
        # mask the background and color the plant with color scheme 'jet'
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img_back = cv2.bitwise_and(img_gray, img_gray, mask=mask_inv)
        img_back3 = np.dstack((img_back, img_back, img_back))

        cplant_back = cv2.add(cplant1, img_back3)

    if background == 'white':
        img_back3 = cv2.bitwise_and(w_back3, w_back3, mask=mask_inv)
        cplant_back = cv2.add(cplant1, img_back3)

    fig_name_pseudo = str(filename[0:-4]) + '_' + str(channel) + '_pseudo_on_' + str(background) + '.jpg'
    # fig_name_pseudo= str(filename[0:-4]) + '_' + str(channel) + '_pseudo_on_' + str(background) + '.png'
    print_image(cplant_back, fig_name_pseudo)
    analysis_images.append(['IMAGE', 'pseudo', fig_name_pseudo])

    return analysis_images


def analyze_color(img, imgname, mask, bins, device, debug=False, hist_plot_type=None, pseudo_channel='v',
                  pseudo_bkg='img', resolution=300, filename=False):
    """Analyze the color properties of an image object

    Inputs:
    img              = image
    imgname          = name of input image
    mask             = mask made from selected contours
    device           = device number. Used to count steps in the pipeline
    debug            = True/False. If True, print data and histograms
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
    :param debug: bool
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
    if len(np.shape(img)) == 3:
        ix, iy, iz = np.shape(img)
    else:
        ix, iy = np.shape(img)
    size = ix, iy
    background = np.zeros(size, dtype=np.uint8)
    w_back = background + 255
    ori_img = np.copy(img)

    masked = cv2.bitwise_and(img, img, mask=mask)
    b, g, r = cv2.split(masked)
    lab = cv2.cvtColor(masked, cv2.COLOR_BGR2LAB)
    l, m, y = cv2.split(lab)
    hsv = cv2.cvtColor(masked, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    channel = (b, g, r, l, m, y, h, s, v)
    graph_color = ('blue', 'forestgreen', 'red', 'dimgray', 'magenta', 'yellow', 'blueviolet', 'cyan', 'orange')
    label = ('blue', 'green', 'red', 'lightness', 'green-magenta', 'blue-yellow', 'hue', 'saturation', 'value')

    # Create Color Histogram Data
    b_bin = b / (256 / bins)
    g_bin = g / (256 / bins)
    r_bin = r / (256 / bins)
    l_bin = l / (256 / bins)
    m_bin = m / (256 / bins)
    y_bin = y / (256 / bins)
    h_bin = h / (256 / bins)
    s_bin = s / (256 / bins)
    v_bin = v / (256 / bins)

    hist_b = cv2.calcHist([b_bin], [0], mask, [bins], [0, (bins - 1)])
    hist_g = cv2.calcHist([g_bin], [0], mask, [bins], [0, (bins - 1)])
    hist_r = cv2.calcHist([r_bin], [0], mask, [bins], [0, (bins - 1)])
    hist_l = cv2.calcHist([l_bin], [0], mask, [bins], [0, (bins - 1)])
    hist_m = cv2.calcHist([m_bin], [0], mask, [bins], [0, (bins - 1)])
    hist_y = cv2.calcHist([y_bin], [0], mask, [bins], [0, (bins - 1)])
    hist_h = cv2.calcHist([h_bin], [0], mask, [bins], [0, (bins - 1)])
    hist_s = cv2.calcHist([s_bin], [0], mask, [bins], [0, (bins - 1)])
    hist_v = cv2.calcHist([v_bin], [0], mask, [bins], [0, (bins - 1)])

    hist_data_b = [l[0] for l in hist_b]
    hist_data_g = [l[0] for l in hist_g]
    hist_data_r = [l[0] for l in hist_r]
    hist_data_l = [l[0] for l in hist_l]
    hist_data_m = [l[0] for l in hist_m]
    hist_data_y = [l[0] for l in hist_y]
    hist_data_h = [l[0] for l in hist_h]
    hist_data_s = [l[0] for l in hist_s]
    hist_data_v = [l[0] for l in hist_v]

    # Store Color Histogram Data
    hist_header = (
        'HEADER_HISTOGRAM',
        'bin-number',
        'blue',
        'green',
        'red',
        'lightness',
        'green-magenta',
        'blue-yellow',
        'hue',
        'saturation',
        'value'
    )

    hist_data = (
        'HISTOGRAM_DATA',
        bins,
        hist_data_b,
        hist_data_g,
        hist_data_r,
        hist_data_l,
        hist_data_m,
        hist_data_y,
        hist_data_h,
        hist_data_s,
        hist_data_v
    )

    analysis_images = []

    p_channel = pseudo_channel
    pseudocolor_img = 1

    if p_channel == None:
        pass
    elif filename == False:
        pass
    elif p_channel == 'h':
        if (pseudo_bkg == 'white' or pseudo_bkg == 'both'):
            analysis_images = _pseudocolored_image(h_bin, bins, img, mask, 'white', p_channel, filename, resolution,
                                                   analysis_images)

        if (pseudo_bkg == 'img' or pseudo_bkg == 'both'):
            analysis_images = _pseudocolored_image(h_bin, bins, img, mask, 'img', p_channel, filename, resolution,
                                                   analysis_images)

    elif p_channel == 's':
        if (pseudo_bkg == 'white' or pseudo_bkg == 'both'):
            analysis_images = _pseudocolored_image(s_bin, bins, img, mask, 'white', p_channel, filename, resolution,
                                                   analysis_images)

        if (pseudo_bkg == 'img' or pseudo_bkg == 'both'):
            analysis_images = _pseudocolored_image(s_bin, bins, img, mask, 'img', p_channel, filename, resolution,
                                                   analysis_images)

    elif p_channel == 'v':
        if (pseudo_bkg == 'white' or pseudo_bkg == 'both'):
            analysis_images = _pseudocolored_image(v_bin, bins, img, mask, 'white', p_channel, filename, resolution,
                                                   analysis_images)

        if (pseudo_bkg == 'img' or pseudo_bkg == 'both'):
            analysis_images = _pseudocolored_image(v_bin, bins, img, mask, 'img', p_channel, filename, resolution,
                                                   analysis_images)

    elif p_channel == 'l':
        if (pseudo_bkg == 'white' or pseudo_bkg == 'both'):
            analysis_images = _pseudocolored_image(l_bin, bins, img, mask, 'white', p_channel, filename, resolution,
                                                   analysis_images)

        if (pseudo_bkg == 'img' or pseudo_bkg == 'both'):
            analysis_images = _pseudocolored_image(l_bin, bins, img, mask, 'img', p_channel, filename, resolution,
                                                   analysis_images)

    elif p_channel == 'm':
        if (pseudo_bkg == 'white' or pseudo_bkg == 'both'):
            analysis_images = _pseudocolored_image(m_bin, bins, img, mask, 'white', p_channel, filename, resolution,
                                                   analysis_images)

        if (pseudo_bkg == 'img' or pseudo_bkg == 'both'):
            analysis_images = _pseudocolored_image(m_bin, bins, img, mask, 'img', p_channel, filename, resolution,
                                                   analysis_images)

    elif p_channel == 'y':
        if (pseudo_bkg == 'white' or pseudo_bkg == 'both'):
            analysis_images = _pseudocolored_image(y_bin, bins, img, mask, 'white', p_channel, filename, resolution,
                                                   analysis_images)

        if (pseudo_bkg == 'img' or pseudo_bkg == 'both'):
            analysis_images = _pseudocolored_image(y_bin, bins, img, mask, 'img', p_channel, filename, resolution,
                                                   analysis_images)

    else:
        fatal_error('Pseudocolor Channel' + str(pseudo_channel) + ' is not "None", "l","m", "y", "h","s" or "v"!')

    if debug and p_channel != None:
        from matplotlib import pyplot as plt
        from matplotlib import cm as cm
        from matplotlib import colors as colors
        from matplotlib import colorbar as colorbar
        if os.path.isfile(('VIS_pseudocolor_colorbar_' + str(pseudo_channel) + '_channel.svg')):
            pass
        else:
            filename1 = str(filename)
            name_array = filename1.split("/")
            filename2 = "/".join(map(str, name_array[:-1]))
            fig = plt.figure()
            ax1 = fig.add_axes([0.05, 0.80, 0.9, 0.15])
            valmin = -0
            valmax = (bins - 1)
            norm = colors.Normalize(vmin=valmin, vmax=valmax)
            cb1 = colorbar.ColorbarBase(ax1, cmap=cm.jet, norm=norm, orientation='horizontal')
            fig_name = 'VIS_pseudocolor_colorbar_' + str(pseudo_channel) + '_channel.svg'
            fig.savefig(fig_name, bbox_inches='tight')
            fig.clf()

    if hist_plot_type != None:
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
            if debug:
                fig_name = (str(device) + '_' + str(hist_plot_type) + '_hist.svg')
                plt.savefig(fig_name)
            plt.clf()

    return device, hist_header, hist_data, analysis_images
