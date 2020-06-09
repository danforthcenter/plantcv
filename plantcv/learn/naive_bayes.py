# Naive Bayes

import os
import cv2
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt


def naive_bayes(imgdir, maskdir, outfile, mkplots=False):
    """Naive Bayes training function

    Inputs:
    imgdir  = Path to a directory of original 8-bit RGB images.
    maskdir = Path to a directory of binary mask images. Mask images must have the same name as their corresponding
              color images.
    outfile = Name of the output text file that will store the color channel probability density functions.
    mkplots = Make PDF plots (True or False).

    :param imgdir: str
    :param maskdir: str
    :param outfile: str
    :param mkplots: bool
    """
    # Initialize color channel ndarrays for plant (foreground) and background
    plant = {"hue": np.array([], dtype=np.uint8), "saturation": np.array([], dtype=np.uint8),
             "value": np.array([], dtype=np.uint8)}
    background = {"hue": np.array([], dtype=np.uint8), "saturation": np.array([], dtype=np.uint8),
                  "value": np.array([], dtype=np.uint8)}

    # Walk through the image directory
    print("Reading images...")
    for (dirpath, dirnames, filenames) in os.walk(imgdir):
        for filename in filenames:
            # Is this an image type we can work with?
            if filename[-3:] in ['png', 'jpg', 'jpeg']:
                # Does the mask exist?
                if os.path.exists(os.path.join(maskdir, filename)):
                    # Read the image as BGR
                    img = cv2.imread(os.path.join(dirpath, filename), 1)
                    # Read the mask as grayscale
                    mask = cv2.imread(os.path.join(maskdir, filename), 0)

                    # Convert the image to HSV and split into component channels
                    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                    hue, saturation, value = cv2.split(hsv)

                    # Store channels in a dictionary
                    channels = {"hue": hue, "saturation": saturation, "value": value}

                    # Split channels into plant and non-plant signal
                    for channel in channels.keys():
                        fg, bg = _split_plant_background_signal(channels[channel], mask)

                        # Randomly sample from the plant class (sample 10% of the pixels)
                        fg = fg[np.random.randint(0, len(fg) - 1, int(len(fg) / 10))]
                        # Randomly sample from the background class the same n as the plant class
                        bg = bg[np.random.randint(0, len(bg) - 1, len(fg))]
                        plant[channel] = np.append(plant[channel], fg)
                        background[channel] = np.append(background[channel], bg)

    # Calculate a probability density function for each channel using a Gaussian kernel density estimator
    # Create an output file for the PDFs
    out = open(outfile, "w")
    out.write("class\tchannel\t" + "\t".join(map(str, range(0, 256))) + "\n")
    for channel in plant.keys():
        print("Calculating PDF for the " + channel + " channel...")
        plant_kde = stats.gaussian_kde(plant[channel])
        bg_kde = stats.gaussian_kde(background[channel])
        # Calculate p from the PDFs for each 8-bit intensity value and save to outfile
        plant_pdf = plant_kde(range(0, 256))
        out.write("plant\t" + channel + "\t" + "\t".join(map(str, plant_pdf)) + "\n")
        bg_pdf = bg_kde(range(0, 256))
        out.write("background\t" + channel + "\t" + "\t".join(map(str, bg_pdf)) + "\n")
        if mkplots:
            # If mkplots is True, make the PDF charts
            _plot_pdf(channel, os.path.dirname(outfile), plant=plant_pdf, background=bg_pdf)

    out.close()


def naive_bayes_multiclass(samples_file, outfile, mkplots=False):
    """Naive Bayes training function for two or more classes from sampled pixel RGB values.

    Inputs:
    samples_file = Input text file containing sampled pixel RGB values for each training class. The file should be a
                   tab-delimited table with one training class per column. The required first row must contain header
                   labels for each class. The row values for each class must be comma-delimited RGB values.
                   You must have at least 2 classes. See the file plantcv/tests/data/sampled_rgb_points.txt for
                   an example.
    outfile      = Name of the output text file that will store the color channel probability density functions.
    mkplots      = Make PDF plots (True or False).

    :param samples_file: str
    :param outfile: str
    :param mkplots: bool
    """
    # Initialize a dictionary to store sampled RGB pixel values for each input class
    sample_points = {}
    # Open the sampled points text file
    f = open(samples_file, "r")
    # Read the first line and use the column headers as class labels
    header = f.readline()
    header = header.rstrip("\n")
    class_list = header.split("\t")
    # Initialize a dictionary for the red, green, and blue channels for each class
    for cls in class_list:
        sample_points[cls] = {"red": [], "green": [], "blue": []}
    # Loop over the rest of the data in the input file
    for row in f:
        # Remove newlines and quotes
        row = row.rstrip("\n")
        row = row.replace('"', '')
        # If this is not a blank line, parse the data
        if len(row) > 0:
            # Split the row into a list of points per class
            points = row.split("\t")
            # For each point per class
            for i, point in enumerate(points):
                if len(point) > 0:
                    # Split the point into red, green, and blue integer values
                    red, green, blue = map(int, point.split(","))
                    # Append each intensity value into the appropriate class list
                    sample_points[class_list[i]]["red"].append(red)
                    sample_points[class_list[i]]["green"].append(green)
                    sample_points[class_list[i]]["blue"].append(blue)
    f.close()
    # Initialize a dictionary to store probability density functions per color channel in HSV colorspace
    pdfs = {"hue": {}, "saturation": {}, "value": {}}
    # For each class
    for cls in class_list:
        # Create a blue, green, red-formatted image ndarray with the class RGB values
        bgr_img = cv2.merge((np.asarray(sample_points[cls]["blue"], dtype=np.uint8),
                             np.asarray(sample_points[cls]["green"], dtype=np.uint8),
                             np.asarray(sample_points[cls]["red"], dtype=np.uint8)))
        # Convert the BGR ndarray to an HSV ndarray
        hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
        # Split the HSV ndarray into the component HSV channels
        hue, saturation, value = cv2.split(hsv_img)
        # Create an HSV channel dictionary that stores the channels as lists (horizontally stacked ndarrays)
        channels = {"hue": np.hstack(hue), "saturation": np.hstack(saturation), "value": np.hstack(value)}
        # For each channel
        for channel in channels.keys():
            # Create a kernel density estimator for the channel values (Gaussian kernel)
            kde = stats.gaussian_kde(channels[channel])
            # Use the KDE to calculate a probability density function for the channel
            # Sample at each of the possible 8-bit values
            pdfs[channel][cls] = kde(range(0, 256))
    if mkplots:
        # If mkplots is True, generate a density curve plot per channel for each class
        for channel, cls in pdfs.items():
            _plot_pdf(channel, os.path.dirname(outfile), **cls)
    # Write the PDFs to a text file
    out = open(outfile, "w")
    # Write the column labels
    out.write("class\tchannel\t" + "\t".join(map(str, range(0, 256))) + "\n")
    # For each channel
    for channel, cls in pdfs.items():
        # For each class
        for class_name, pdf in cls.items():
            # Each row is the PDF for the given class and color channel
            out.write(class_name + "\t" + channel + "\t" + "\t".join(map(str, pdf)) + "\n")


def _split_plant_background_signal(channel, mask):
    """Split a single-channel image by foreground and background using a mask

    :param channel: ndarray
    :param mask: ndarray
    :return plant: ndarray
    :return background: ndarray
    """
    plant = channel[np.where(mask == 255)]
    background = channel[np.where(mask == 0)]

    return plant, background


def _plot_pdf(channel, outdir, **kwargs):
    """Plot the probability density function of one or more classes for the given channel

    :param channel: str
    :param outdir: str
    :param kwargs: dict
    """

    for class_name, pdf in kwargs.items():
        plt.plot(pdf, label=class_name)
    plt.legend(loc="best")
    plt.savefig(os.path.join(outdir, str(channel) + "_pdf.svg"))
    plt.close()
