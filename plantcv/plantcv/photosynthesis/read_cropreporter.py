# Read in fluorescence images from a .DAT file

import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv.plot_image import plot_image
from plantcv.plantcv.print_image import print_image


def read_cropreporter(inf_filename):
    """Read in, reshape, and subset a datacube of fluorescence snapshots

        Inputs:
            inf_filename     = Fluorescence .INF filename

        Returns:
            fdark            = fdark (F0) image
            fmin             = fmin image
            fmax             = fmax image

        :param inf_filename: str
        :return fdark: numpy.ndarray
        :return fmin: numpy.ndarray
        :return fmax: numpy.ndarray
        """
    # Parse .inf file and create dictionary with metadata stored within
    with open(inf_filename, "r") as f:
        # Replace characters for easier parsing
        inf_data = f.read()
        inf_data = inf_data.replace(",\n", ",")
        inf_data = inf_data.replace("\n,", ",")
        inf_data = inf_data.replace("{\n", "{")
        inf_data = inf_data.replace("\n}", "}")
        inf_data = inf_data.replace(" \n ", "")
        inf_data = inf_data.replace(";", "")
    inf_data = inf_data.split("\n")

    inf_dict = {}  # Initialize dictionary

    # Loop through and create a dictionary from the inf file
    for i, string in enumerate(inf_data):
        if '=' in string:
            header_data = string.split("=")
            inf_dict.update({header_data[0].rstrip(): header_data[1].rstrip()})

    # Store image dimension data
    x = int(inf_dict["ImageCols"])
    y = int(inf_dict["ImageRows"])

    # Record a dictonary of all measurements done, 0 means not done, 1 means measurement done
    frames_captured = {key: value for key, value in inf_dict.items() if "Done" in key}
    # Record a list of measurements, just first three letters is enough to match them up
    frames_expected = [key.upper()[0:3] for key, value in frames_captured.items() if str(value) == "1"]
    # Define dictionary of measurement name and the corresponding binary image filename
    corresponding_dict = {"FVF": "PSD", "FQF": "PSL", "CHL": "CHL", "NPQ": "NPQ", "SPC": "SPC",
                          "CLR": "CLR", "RFD": "RFD", "GFP": "GFP", "RFP": "RFP"}
    all_imgs = {}
    # Loop over all expected binary image files
    for key in frames_expected:
        # Find the corresponding binary image filename based on the INF filename
        inf = os.path.split(inf_filename)[-1]
        path = os.path.dirname(inf_filename)
        filename_components = inf.split("_")
        filename_components[1] = corresponding_dict[key]
        s = "_"
        bin_filename = s.join(filename_components)
        bin_filename = bin_filename.replace(".INF", ".DAT")
        bin_file = os.path.join(path, bin_filename)
        # Read in binary image file
        raw_data = np.fromfile(bin_file, np.uint16, -1)
        # Reshape into a datacube
        img_cube = raw_data.reshape(int(len(raw_data) / (y * x)), x, y).transpose((2, 1, 0))
        # Append the image cube to a dictonary with all images
        all_imgs[corresponding_dict[key]] = img_cube

# NEEDS UPDATING, plan to use x-array objects to store all frames as a single thing that can be input into analysis fxns
    # # Extract fdark and fmin from the datacube of stacked frames
    # fdark = img_cube[:, :, [0]]
    # fdark = np.transpose(np.transpose(fdark)[0])  # Reshape frame from (x,y,1) to (x,y)
    # fmin = img_cube[:, :, [1]]
    # fmin = np.transpose(np.transpose(fmin)[0])
    #
    # # Identify fmax frame
    # i = 0
    # max_sum = 0
    # max_index = 1
    #
    # frame_sums = []
    # for i in range(img_cube.shape[2]):
    #     frame_sums.append(np.sum(img_cube[:, :, i]))
    # fmax = img_cube[:, :, np.argmax(frame_sums)]
    #
    # if params.debug == "print":
    #     print_image(fdark, os.path.join(params.debug_outdir, str(params.device) + "fdark_frame.png"))
    #     print_image(fmin, os.path.join(params.debug_outdir, str(params.device) + "fmin_frame.png"))
    #     print_image(fmax, os.path.join(params.debug_outdir, str(params.device) + "fmax_frame.png"))
    # elif params.debug == "plot":
    #     plot_image(fdark)
    #     plot_image(fmin)
    #     plot_image(fmax)
    #
    # return fdark, fmin, fmax
