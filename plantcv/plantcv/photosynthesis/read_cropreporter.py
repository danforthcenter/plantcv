# Read in fluorescence images from a .DAT file

import os
import numpy as np
import xarray as xr
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug



def read_cropreporter(filename):
    """Read in, reshape, and subset a datacube of fluorescence snapshots

        Inputs:
            filename        = Fluorescence .DAT filename

        Returns:
            da               = x-array data array
            path             = path to image files
            filename         = name of .DAT file

        :param inf_filename: str
        :return da: numpy.ndarray
        :return path: str
        :return filename: str
        """

    # Parse .inf file and create dictionary with metadata stored within
    with open(filename, "r") as f:
        # Replace characters for easier parsing
        metadata = f.read()
        metadata = metadata.replace(",\n", ",")
        metadata = metadata.replace("\n,", ",")
        metadata = metadata.replace("{\n", "{")
        metadata = metadata.replace("\n}", "}")
        metadata = metadata.replace(" \n ", "")
        metadata = metadata.replace(";", "")
    metadata = metadata.split("\n")

    metadata_dict = {}  # Initialize dictionary

    # Loop through and create a dictionary from the .INF file
    for i, string in enumerate(metadata):
        if '=' in string:
            header_data = string.split("=")
            metadata_dict.update({header_data[0].rstrip(): header_data[1].rstrip()})

    # Store image dimension data
    x = int(metadata_dict["ImageCols"])
    y = int(metadata_dict["ImageRows"])
    # Use metadata to determine which frames to expect
    frames_captured = {key: value for key, value in metadata_dict.items() if "Done" in key}
    frames_expected = [key.upper()[0:3] for key, value in frames_captured.items() if str(value) == "1"]
    corresponding_dict = {"FVF": "PSD", "FQF": "PSL", "CHL": "CHL", "NPQ": "NPQ", "SPC": "SPC",
                          "CLR": "CLR", "RFD": "RFD", "GFP": "GFP", "RFP": "RFP"}
    # Initialize lists
    param_labels = []
    img_frames = []
    all_indices = []
    all_frame_labels = []
    print(frames_expected)

    # Loop over all raw bin files
    for key in frames_expected:
        # Find corresponding bin img filepath based on .INF filepath
        inf = os.path.split(filename)[-1]
        path = os.path.dirname(filename)
        filename_components = inf.split("_")
        filename_components[1] = corresponding_dict[key]  # replace header with bin img type
        s = "_"
        bin_filenames = s.join(filename_components)
        bin_filename = bin_filenames.replace(".INF", ".DAT")
        bin_filepath = os.path.join(path, bin_filename)

        # Dump in bin img data
        raw_data = np.fromfile(bin_filepath, np.uint16, -1)
        # Reshape
        img_cube = raw_data.reshape(int(len(raw_data) / (y * x)), x, y).transpose((2, 1, 0))  # numpy shaped
        # Store bin img data
        img_frames.append(img_cube)  # append cube to a list

        # Compile COORDS (lists of indicies)
        index_list = np.arange(np.shape(img_cube)[2]).tolist()
        all_indices = all_indices + index_list
        param_label = [corresponding_dict[key]] * (np.shape(img_cube)[2])  # repetitive list of parameter labels
        param_labels = param_labels + param_label

        # Calculate frames of interest and keep track of their labels
        if corresponding_dict[key] == "NPQ":
            frame_sums = []
            for i in range(img_cube.shape[2]):
                frame_sums.append(np.sum(img_cube[:, :, i]))
            f_min = np.argmin(frame_sums)
            frame_labels = ["other"] * (np.shape(img_cube)[2])
            frame_labels[f_min] = "Fp"
            frame_labels[np.argmax(frame_sums)] = "Fmp"
        elif corresponding_dict[key] == "PSD":
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

    # Stack all the frames
    f = np.dstack(img_frames)
    # Make coordinates list
    x_coord = range(0, x)
    y_coord = range(0, y)
    index_list = np.arange(np.shape(f)[2])

    # Create DataArray
    da = xr.DataArray(data=f, coords={"y": y_coord, "x": x_coord, "frame_label": all_frame_labels},
                      dims=["y", "x", "frame_label"])
    # Pass fmax frame to _debug function
    fmax = da.sel(frame_label='fmax').data
    _debug(visual=fmax, filename=os.path.join(params.debug_outdir, str(params.device) + "_fmax.png"))

    return da, path, filename
