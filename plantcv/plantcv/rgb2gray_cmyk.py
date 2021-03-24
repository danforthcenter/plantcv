# RGB -> CMYK -> Gray

import cv2
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
import numpy as np


def rgb2gray_cmyk(rgb_img, channel):
    """Convert image from RGB colorspace to CMYK colorspace. Returns the specified subchannel as a gray image.

    Inputs:
    rgb_img   = RGB image data
    channel   = color subchannel (c = cyan, m = magenta, y = yellow, k=black)

    Returns:
    c | m | y | k = grayscale image from one CMYK color channel

    :param rgb_img: numpy.ndarray
    :param channel: str
    :return channel: numpy.ndarray
    """
    # Auto-increment the device counter
    params.device += 1
    # The allowable channel inputs are c, m , y or k
    names = {"c": "cyan", "m": "magenta", "y": "yellow", "k": "black"}
    channel = channel.lower()
    if channel not in names:
        fatal_error("Channel " + str(channel) + " is not c, m, y or k!")

    B = rgb_img[:, :, 0].astype(float) # float conversion
    G = rgb_img[:, :, 1].astype(float) #
    R = rgb_img[:, :, 2].astype(float) #

    B_ = np.copy(B) 
    G_ = np.copy(G)
    R_ = np.copy(R)

    K = np.zeros_like(B) 
    C = np.zeros_like(B) 
    M = np.zeros_like(B) 
    Y = np.zeros_like(B) 

    for i in range(B.shape[0]):
        for j in range(B.shape[1]):
            B_[i, j] = B[i, j]/255
            G_[i, j] = G[i, j]/255
            R_[i, j] = R[i, j]/255

            K[i, j] = 1 - max(B_[i, j], G_[i, j], R_[i, j])
            if (B_[i, j] == 0) and (G_[i, j] == 0) and (R_[i, j] == 0):
            # black
                  C[i, j] = 0
                  M[i, j] = 0  
                  Y[i, j] = 0
            else:

                C[i, j] = (1 - R_[i, j] - K[i, j])/float((1 - K[i, j]))
                M[i, j] = (1 - G_[i, j] - K[i, j])/float((1 - K[i, j]))
                Y[i, j] = (1 - B_[i, j] - K[i, j])/float((1 - K[i, j]))


    # Convert the input BGR image to LAB colorspace
    CMYK = (np.dstack((C,M,Y,K)) * 255).astype(np.uint8)
    #Split CMYK channels
    C, M, Y, K = cv2.split(CMYK)
    # Create a channel dictionaries for lookups by a channel name index
    channels = {"c": C, "m": M, "y": Y, "k": K}

    if params.debug == "print":
        print_image(channels[channel], os.path.join(params.debug_outdir,
                                                    str(params.device) + "_cmyk_" + names[channel] + ".png"))
    elif params.debug == "plot":
        plot_image(channels[channel], cmap="gray")

    return channels[channel]
