# Read in fluorescence images from a .DAT file

import os
import numpy as np
import xarray as xr
from plantcv.plantcv.transform import rescale
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def read_cropreporter(filename):
    """Read in, reshape, and subset a datacube of fluorescence snapshots

    Inputs:
        filename        = PhenoVation B.V. CropReporter .INF filename

    Returns:
        ps               = photosynthesis data in xarray DataArray format
        imgpath          = path to image files
        inf_filename     = name of .INF file

    :param filename: str
    :return ps: xarray.core.dataarray.DataArray
    :return imgpath: str
    :return inf_filename: str
    """

    # Initialize metadata dictionary
    metadata_dict = {}

    # Parse .inf file and create dictionary with metadata stored within
    with open(filename, "r") as fp:
        for line in fp:
            if "=" in line:
                key, value = line.rstrip("\n").split("=")
                metadata_dict[key] = value

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

    # INF file prefix and path
    inf_filename = os.path.split(filename)[-1]
    imgpath = os.path.dirname(filename)
    filename_components = inf_filename.split("_")

    # Metadata attributes to attach to the xarray DataArray
    attributes = {}

    # Loop over all raw bin files
    for key in frames_expected:
        # Find corresponding bin img filepath based on .INF filepath
        filename_components[1] = corresponding_dict[key]  # replace header with bin img type
        bin_filenames = "_".join(filename_components)
        bin_filename = bin_filenames.replace(".INF", ".DAT")
        bin_filepath = os.path.join(imgpath, bin_filename)

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
            frame_labels = ["NPQ-Fdark", "NPQ-F0", "NPQ-Fm", "NPQ-Fdark'", "NPQ-F0'", "NPQ-Fm'"]
            # Debug image NPQ-Fm
            _debug(visual=img_cube[:, :, 2],
                   filename=os.path.join(params.debug_outdir,  f"{str(params.device)}_NPQ-Fm.png"))
        elif corresponding_dict[key] == "PSD":
            frame_labels = ["Fdark", "F0"]
            for i in range(2, np.shape(img_cube)[2]):
                frame_labels.append(f"F{i - 1}")
            attributes["F-frames"] = img_cube.shape[2] - 1
            _debug(visual=img_cube[:, :, -1],
                   filename=os.path.join(params.debug_outdir, f"{str(params.device)}_PSD-{frame_labels[-1]}.png"))
        elif corresponding_dict[key] == "PSL":
            frame_labels = ["Fdark'", "F0'"]
            for i in range(2, np.shape(img_cube)[2]):
                frame_labels.append(f"F{i - 1}'")
            attributes["F'-frames"] = img_cube.shape[2] - 1
            _debug(visual=img_cube[:, :, -1],
                   filename=os.path.join(params.debug_outdir, f"{str(params.device)}_PSL-{frame_labels[-1]}.png"))
        elif corresponding_dict[key] == "CLR":
            frame_labels = ["Red", "Green", "Blue"]
            debug = params.debug
            params.debug = None
            red = rescale(gray_img=img_cube[:, :, 0])
            green = rescale(gray_img=img_cube[:, :, 1])
            blue = rescale(gray_img=img_cube[:, :, 2])
            rgb_img = np.dstack([blue, green, red])
            params.debug = debug
            _debug(visual=rgb_img,
                   filename=os.path.join(params.debug_outdir, f"{str(params.device)}_CLR-RGB.png"))
        elif corresponding_dict[key] == "CHL":
            frame_labels = ["Chl", "Chl-NIR"]
            _debug(visual=img_cube[:, :, 1],
                   filename=os.path.join(params.debug_outdir, f"{str(params.device)}_CHL-NIR.png"))
        elif corresponding_dict[key] == "SPC":
            frame_labels = ["Anth", "Far-red", "Anth-NIR"]
            _debug(visual=img_cube[:, :, 0],
                   filename=os.path.join(params.debug_outdir, f"{str(params.device)}_SPC-Anth.png"))
        else:
            frame_labels = [key + "other"] * (np.shape(img_cube)[2])
        all_frame_labels = all_frame_labels + frame_labels

    # Stack all the frames
    f = np.dstack(img_frames)
    # Make coordinates list
    x_coord = range(0, x)
    y_coord = range(0, y)
    # index_list = np.arange(np.shape(f)[2])

    # Create DataArray
    ps = xr.DataArray(data=f, coords={"y": y_coord, "x": x_coord, "frame_label": all_frame_labels},
                      dims=["y", "x", "frame_label"], attrs=attributes)

    return ps, imgpath, inf_filename
