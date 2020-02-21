# Plot graph with a histogram of pixel intensity frequency for two sample ROIs

import os
import cv2
import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_line, scale_x_continuous
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv.threshold import binary as binary_threshold
from plantcv.plantcv import params
from plantcv.plantcv import outputs



def sample_pixel_intensity(gray_img, foreground_pt, background_pt, radius):
    """This function calculates the intensity of each pixel associated with the plant and writes the values out to
       a file. It can also print out a histogram plot of pixel intensity and a pseudocolor image of the plant.

    Inputs:
    gray_img     = 8- or 16-bit grayscale image data
    mask         = Binary mask made from selected contours
    bins         = number of classes to divide spectrum into
    histplot     = if True plots histogram of intensity values

    Returns:
    analysis_images = NIR histogram image

    :param gray_img: numpy array
    :param mask: numpy array
    :param bins: int
    :param histplot: bool
    :return analysis_images: plotnine ggplot
    """

    # Calculate histogram
    hist_nir = [float(l[0]) for l in cv2.calcHist([gray_img], [0], mask, [bins], [0, maxval])]