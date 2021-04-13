# Read in fluorescence images from a .DAT file

import os
import numpy as np
import xarray as xr
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug



def read_cropreporter(inf_filename):
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

    frames_captured = {key: value for key, value in inf_dict.items() if "Done" in key}
    frames_expected = [key.upper()[0:3] for key, value in frames_captured.items() if str(value) == "1"]
    corresponding_dict = {"FVF": "PSD", "FQF": "PSL", "CHL": "CHL", "NPQ": "NPQ", "SPC": "SPC",
                          "CLR": "CLR", "RFD": "RFD", "GFP": "GFP", "RFP": "RFP"}

    # print(inf_dict)
    all_imgs = {}
    param_labels = []
    img_frames = []
    all_indices = []
    all_frame_labels = []

    # Loop over all raw bin files
    for key in frames_expected:
        # Find corresponding bin img filepath based on .DAT filepath
        inf = os.path.split(inf_filename)[-1]
        path = os.path.dirname(inf_filename)
        filename_components = inf.split("_")
        filename_components[1] = corresponding_dict[key]  # replace header with bin img type
        s = "_"
        bin_filenames = s.join(filename_components)
        bin_filename = bin_filenames.replace(".INF", ".DAT")
        bin_filepath = os.path.join(path, bin_filename)

        # Dump in bin img data
        raw_data = np.fromfile(bin_filepath, np.uint16, -1)

        # Reshape
        # img_cube = raw_data.reshape(int(len(raw_data) / (y * x)), x, y).transpose((1, 2, 0))
        img_cube = raw_data.reshape(int(len(raw_data) / (y * x)), x, y).transpose((2, 1, 0))  # numpy shaped

        # Store bin img data
        all_imgs[corresponding_dict[key]] = img_cube  # store each data cube into a dictionary with labeled source
        img_frames.append(img_cube)  # append cube to a list

        # Compile COORDS (lists of indicies)
        index_list = np.arange(np.shape(img_cube)[2]).tolist()
        all_indices = all_indices + index_list
        param_label = [corresponding_dict[key]] * (np.shape(img_cube)[2])  # repetitive list of parameter labels
        param_labels = param_labels + param_label

        # Calculate frames of interest and keep track of their labels

        if corresponding_dict[key] is "NPQ":
            frame_sums = []
            for i in range(img_cube.shape[2]):
                frame_sums.append(np.sum(img_cube[:, :, i]))
            f_min = np.argmin(frame_sums)
            frame_labels = ["other"] * (np.shape(img_cube)[2])
            frame_labels[f_min] = "Fp"
            frame_labels[np.argmax(frame_sums)] = "Fmp"
        elif corresponding_dict[key] is "PSD":
            frame_labels = ["other"] * (np.shape(img_cube)[2])
            frame_labels[0] = "fdark"
            frame_labels[1] = "fmin"
            frame_sums = []
            for i in range(img_cube.shape[2]):
                frame_sums.append(np.sum(img_cube[:, :, i]))
            frame_labels[np.argmax(frame_sums)] = "fmax"
        else:
            frame_labels = ["other"] * (np.shape(img_cube)[2])
        all_frame_labels = all_frame_labels + frame_labels

        # # TESTING SHTUFF
    # print(param_labels)
    # print(all_indices)
    # print(all_frame_labels)

    # Make coordinates list
    x_coord = range(0, x)
    y_coord = range(0, y)
    index_list = np.arange(np.shape(all_imgs[corresponding_dict[key]])[2])

    # Stack all the frames
    f = np.dstack(img_frames)
    # Create DataArray
    da = xr.DataArray(data=f, coords={"y": y_coord, "x": x_coord, "frame_label": all_frame_labels},
                      dims=["y", "x", "frame_label"])

    fmax = da.sel(frame_label='fmax').data
    _debug(visual=fmax, filename=os.path.join(params.debug_outdir, str(params.device) + "_fmax.png"))

    return inf_dict, all_imgs, da
