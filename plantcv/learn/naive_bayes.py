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
    for (dirpath, _, filenames) in os.walk(imgdir):
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
                    for channel in channels:
                        fg, bg = _split_plant_background_signal(channels[channel], mask)

                        # Randomly sample from the plant class (sample 10% of the pixels)
                        fg = fg[np.random.randint(0, len(fg) - 1, int(len(fg) / 10))]
                        # Randomly sample from the background class the same n as the plant class
                        bg = bg[np.random.randint(0, len(bg) - 1, len(fg))]
                        plant[channel] = np.append(plant[channel], fg)
                        background[channel] = np.append(background[channel], bg)

    # Calculate a probability density function for each channel using a Gaussian kernel density estimator
    # Create an output file for the PDFs
    with open(outfile, "w") as out:
        out.write("class\tchannel\t" + "\t".join(map(str, range(0, 256))) + "\n")
        for channel in plant:
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
    with open(samples_file, "r") as f:
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
        for channel in channels:
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
    with open(outfile, "w") as out:
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


    """Converter functions."""


def tabulate_bayes_classes(input_file, output_file):
    """Tabulate pixel RGB values into a table for naive Bayes training.
    Inputs:
    input_file   = Input text file of class names and RGB values
    output_file  = Output file for storing the tab-delimited naive Bayes training data

    The input file should have class names preceded by the "#" character. RGB values can be pasted
    directly from ImageJ without reformatting. E.g.:

    #plant
    96,154,72	95,153,72	91,155,71	91,160,70	90,155,67	92,152,66	92,157,70
    54,104,39	56,104,38	59,106,41	57,105,43	54,104,40	54,103,35	56,101,39	58,99,41	59,99,41
    #background
    114,127,121	117,135,125	120,137,131	132,145,138	142,154,148	151,166,158	160,182,172
    115,125,121	118,131,123	122,132,135	133,142,144	141,151,152	150,166,158	159,179,172

    :param input_file: str
    :param output_file: str
    """
    # If the input file does not exist raise an error
    if not os.path.exists(input_file):
        raise IOError(f"File does not exist: {input_file}")

    # Read the file into a string
    with open(input_file, "r") as fd:
        pixel_data = fd.read()

    # Split the file string by the classname/header character
    classes = pixel_data.split("#")

    # Parse the class data
    class_dict = {}
    # Ignore the first item, it's the empty string or whitespace to the "left" of the first class/header
    for i in range(1, len(classes)):
        # Replace tabs with newlines
        classes[i] = classes[i].replace("\t", "\n")
        # Split the class data on newlines
        class_data = classes[i].split("\n")
        # The class name is the first item
        class_name = class_data[0]
        rgb_values = []
        # Loop over the RGB values, starting with the second element
        for j in range(1, len(class_data)):
            # Skip blank lines but keep the lines with RGB values
            if len(class_data[j]) > 0:
                rgb_values.append(class_data[j])
        class_dict[class_name] = rgb_values

    # Each class could have a different number of RGB values, find the largest
    total_rgb = 0
    for class_name in class_dict:
        if len(class_dict[class_name]) > total_rgb:
            total_rgb = len(class_dict[class_name])

    # Pad the classes with empty strings if they have less than the total RGB values
    for class_name in class_dict:
        missing = total_rgb - len(class_dict[class_name])
        if missing > 0:
            for i in range(missing):
                class_dict[class_name].append("")

    # Open the output file
    with open(output_file, "w") as out:
        # Create the output table
        class_names = class_dict.keys()
        out.write("\t".join(map(str, class_names)) + "\n")
        for i in range(0, total_rgb):
            row = []
            for class_name in class_names:
                row.append(class_dict[class_name][i])
            out.write("\t".join(map(str, row)) + "\n")
