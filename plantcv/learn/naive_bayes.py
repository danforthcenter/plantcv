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


def check_samples_file(samples_file, max_errors=20):
    """Quality control check of a naive Bayes multiclass samples file.
    Reports formatting problems with line numbers.

    Inputs:
    samples_file = Input text file containing sampled pixel RGB values for each training class.
    max_errors   = Maximum number of example messages to print per error category.

    :param samples_file: str
    :param max_errors: int
    :return valid: bool
    """
    # Example messages (capped at max_errors) and total occurrence counts, per error category
    labels = {"delimiter": "Delimiter problems", "header": "Header problems",
              "column_count": "Wrong column count", "rgb_value": "Invalid RGB values",
              "empty_class": "Classes with no samples"}
    messages = {category: [] for category in labels}
    totals = {category: 0 for category in labels}

    def _record(category, message):
        totals[category] += 1
        if len(messages[category]) < max_errors:
            messages[category].append(message)

    with open(samples_file, "r") as f:
        # Read the first line and use the column headers as class labels
        header = f.readline().rstrip("\n")
        class_list = header.split("\t")

        # Assume a header with one column isn't tab-delimited
        if len(class_list) == 1:
            msg = "Line 1: only 1 column found in the header. Is this file tab-delimited, with one column per class?"
            _record("delimiter", msg)

        # Check for empty or duplicate class labels
        seen_labels = {}
        for i, cls in enumerate(class_list):
            if cls == "":
                _record("header", f"Line 1, column {i + 1}: class label is empty. Every column needs a label")
            elif cls in seen_labels:
                msg = (f"Line 1: class label '{cls}' is used in both column {seen_labels[cls] + 1} and "
                       f"column {i + 1}. Class labels must be unique")
                _record("header", msg)
            else:
                seen_labels[cls] = i

        # Count valid samples per class so we can flag classes that ended up with none
        sample_counts = {cls: 0 for cls in class_list}

        # Loop over the rest of the data in the input file
        for line_num, row in enumerate(f, start=2):
            # Remove newlines and quotes
            row = row.rstrip("\n").replace('"', '')
            # Skip blank lines
            if len(row) == 0:
                continue
            # Split the row into a list of points per class
            points = row.split("\t")
            if len(points) != len(class_list):
                msg = (f"Line {line_num}: row has {len(points)} tab-delimited column(s) but the header defines "
                       f"{len(class_list)} class(es)")
                _record("column_count", msg)
            for i, point in enumerate(points):
                # A row longer than the header has no class to attribute this column to
                if i >= len(class_list) or len(point) == 0:
                    continue
                cls = class_list[i]
                values = point.split(",")
                if len(values) != 3:
                    msg = (f"Line {line_num}, class '{cls}' (column {i + 1}): expected 3 comma-separated RGB "
                           f"values, found {len(values)} ('{point}')")
                    _record("rgb_value", msg)
                    continue
                valid_point = True
                for channel, value in zip(("red", "green", "blue"), values):
                    if not value.strip().lstrip("-").isdigit():
                        msg = (f"Line {line_num}, class '{cls}' (column {i + 1}): {channel} value '{value}' is "
                               "not an integer")
                        _record("rgb_value", msg)
                        valid_point = False
                        continue
                    ivalue = int(value)
                    if ivalue < 0 or ivalue > 255:
                        msg = (f"Line {line_num}, class '{cls}' (column {i + 1}): {channel} value {ivalue} is "
                               "outside the valid 8-bit range (0-255)")
                        _record("rgb_value", msg)
                        valid_point = False
                if valid_point:
                    sample_counts[cls] += 1

        # Flag any labeled class that never got a valid sample
        for cls, n in sample_counts.items():
            if cls != "" and n == 0:
                msg = (f"Class '{cls}' has zero valid sampled pixels. Add at least one row with a valid value "
                       "in this column")
                _record("empty_class", msg)

    total_problems = sum(totals.values())
    if total_problems == 0:
        print(f"{samples_file} looks good: {len(class_list)} classes, "
              + ", ".join(f"{cls}={n}" for cls, n in sample_counts.items()) + " valid sampled pixels each.")
        return True

    print(f"Found {total_problems} formatting problem(s) in {samples_file}:\n")
    for category, label in labels.items():
        count = totals[category]
        if count == 0:
            continue
        print(f"{label} ({min(count, max_errors)} of {count} shown):")
        for message in messages[category]:
            print(f"  {message}")
        if count > max_errors:
            print(f"  ...and {count - max_errors} more.")
        print()
    return False


def naive_bayes_multiclass(samples_file, outfile, mkplots=False, max_errors=20):
    """Naive Bayes training function for two or more classes from sampled pixel RGB values.

    Inputs:
    samples_file = Input text file containing sampled pixel RGB values for each training class. The file should be a
                   tab-delimited table with one training class per column. The required first row must contain header
                   labels for each class. The row values for each class must be comma-delimited RGB values.
                   You must have at least 2 classes. See the file plantcv/tests/data/sampled_rgb_points.txt for
                   an example.
    outfile      = Name of the output text file that will store the color channel probability density functions.
    mkplots      = Make PDF plots (True or False).
    max_errors   = Maximum number of example messages printed per formatting problem category if samples_file
                   fails quality control. See check_samples_file.

    :param samples_file: str
    :param outfile: str
    :param mkplots: bool
    :param max_errors: int
    """
    # Quality control check of the input samples file. Abort before training on a file we can't parse correctly
    if not check_samples_file(samples_file, max_errors=max_errors):
        msg = (f"Naive Bayes multiclass training aborted: {samples_file} has formatting problems. See the "
               "messages above for details on what to fix.")
        raise RuntimeError(msg)

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
