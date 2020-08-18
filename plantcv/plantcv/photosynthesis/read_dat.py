# VERSION 1
# Read in fluorescence images from a .DAT file

import numpy as np


def read_dat(filename):
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
    inf_filename = filename.replace("PSD", "HRD")
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
    img_cols = int(inf_dict["ImageCols"])
    img_rows = int(inf_dict["ImageRows"])

    # Dump and reshape raw data so that the z dimension is the number of frames
    raw_data = np.fromfile(filename, np.uint16, -1)
    img_cube = raw_data.reshape(int(len(raw_data) / (img_rows * img_cols)), img_cols, img_rows).transpose((2, 1, 0))

    return img_cube, inf_dict