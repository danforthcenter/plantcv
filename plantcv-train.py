#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import argparse
import datetime
from scipy import stats
import numpy as np
import cv2


# Parse command-line arguments
###########################################
def options():
    """Parse command line options.

    :return args: object -- parsed arguments
    :raises: IOError, KeyError
    """

    # Job start time
    start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    print("Starting run " + start_time + '\n', file=sys.stderr)

    methods = ["naive_bayes"]

    parser = argparse.ArgumentParser(description='PlantCV machine learning training script.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--imgdir", help='Input directory containing images.', required=True)
    parser.add_argument("-b", "--maskdir", help="Input directory containing black/white masks.", required=True)
    parser.add_argument("-m", "--method", help="Learning method. Available methods: " + ", ".join(map(str, methods)),
                        required=True)
    parser.add_argument("-o", "--outfile", help="Trained classifier output filename.", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.imgdir):
        raise IOError("Directory does not exist: {0}".format(args.imgdir))
    if not os.path.exists(args.maskdir):
        raise IOError("Directory does not exist: {0}".format(args.maskdir))
    if args.method not in methods:
        raise KeyError("Method is not supported: {0}".format(args.method))

    return args


###########################################


# Main
###########################################
def main():
    """Main program.

    """

    # Parse command-line options
    args = options()

    if args.method == "naive_bayes":
        naive_bayes(args.imgdir, args.maskdir, args.outfile)


###########################################


# Naive Bayes
###########################################
def naive_bayes(imgdir, maskdir, outfile):
    """Naive Bayes training function

    :param imgdir: str
    :param maskdir: str
    :param outfile: str
    :return:
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
                        fg, bg = split_plant_background_signal(channels[channel], mask)

                        # Randomly sample from the plant class (sample 10% of the pixels)
                        fg = fg[np.random.random_integers(0, len(fg) - 1, len(fg) / 10)]
                        # Randomly sample from the background class the same n as the plant class
                        bg = bg[np.random.random_integers(0, len(bg) - 1, len(fg))]
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
        plot_pdf(channel, plant_pdf, bg_pdf)

        # Add the second moment (variance) distribution for each channel
        # print("Calculating PDF for the " + channel + "^2 channel...")
        # plant2_kde = stats.gaussian_kde(plant[channel].astype(np.int32) ** 2)
        # bg2_kde = stats.gaussian_kde(background[channel].astype(np.int32) ** 2)
        # plant2_pdf = plant2_kde([x ** 2 for x in range(0, 256)])
        # out.write("plant\t" + channel + "2\t" + "\t".join(map(str, plant2_pdf)) + "\n")
        # bg2_pdf = bg2_kde([x ** 2 for x in range(0, 256)])
        # out.write("background\t" + channel + "2\t" + "\t".join(map(str, bg2_pdf)) + "\n")
        # plot_pdf(channel + "2", plant2_pdf, bg2_pdf)

    out.close()


def split_plant_background_signal(channel, mask):
    """Split a single-channel image by foreground and background using a mask

    :param channel: ndarray
    :param mask: ndarray
    :return plant: ndarray
    :return background: ndarray
    """
    plant = channel[np.where(mask == 255)]
    background = channel[np.where(mask == 0)]

    return plant, background


def plot_pdf(channel, plant, background):
    """Plot the plant and background probability density functions for the given channel

    :param channel: str
    :param plant: ndarray
    :param background: ndarray
    """
    from matplotlib import pyplot as plt
    plt.plot(plant, label="plant-" + str(channel))
    plt.plot(background, label="background-" + str(channel))
    plt.legend(loc="best")
    plt.savefig(str(channel) + "_pdf.png")
    plt.close()


if __name__ == '__main__':
    main()
