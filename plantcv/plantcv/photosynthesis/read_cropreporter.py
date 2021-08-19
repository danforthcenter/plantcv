# Read in fluorescence images from a .DAT file

import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv.plot_image import plot_image
from plantcv.plantcv.print_image import print_image


def read_cropreporter(filename):
    """Read in, reshape, and subset a datacube of fluorescence snapshots

        Inputs:
            filename        = Fluorescence .DAT filename

        Returns:
            fdark            = fdark (F0) image
            fmin             = fmin image
            fmax             = fmax image

        :param filename: str
        :param inf_filename: str
        :return fdark: numpy.ndarray
        :return fmin: numpy.ndarray
        :return fmax: numpy.ndarray
        """
    # Find .INF filename based on the .DAT filename
    inf_filename = filename.replace("PSD", "HDR")
    inf_filename = inf_filename.replace(".DAT", ".INF")

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

    # Dump and reshape raw data so that the z dimension is the number of frames
    raw_data = np.fromfile(filename, np.uint16, -1)
    img_cube = raw_data.reshape(int(len(raw_data) / (y * x)), x, y).transpose((2, 1, 0))

    # Extract fdark and fmin from the datacube of stacked frames
    fdark = img_cube[:, :, [0]]
    fdark = np.transpose(np.transpose(fdark)[0])  # Reshape frame from (x,y,1) to (x,y)
    fmin = img_cube[:, :, [1]]
    fmin = np.transpose(np.transpose(fmin)[0])

    # Identify fmax frame
    i = 0
    max_sum = 0
    max_index = 1

    frame_sums = []
    for i in range(img_cube.shape[2]):
        frame_sums.append(np.sum(img_cube[:, :, i]))
    fmax = img_cube[:, :, np.argmax(frame_sums)]

    if params.debug == "print":
        print_image(fdark, os.path.join(params.debug_outdir, str(params.device) + "fdark_frame.png"))
        print_image(fmin, os.path.join(params.debug_outdir, str(params.device) + "fmin_frame.png"))
        print_image(fmax, os.path.join(params.debug_outdir, str(params.device) + "fmax_frame.png"))
    elif params.debug == "plot":
        plot_image(fdark)
        plot_image(fmin)
        plot_image(fmax)

    return fdark, fmin, fmax
