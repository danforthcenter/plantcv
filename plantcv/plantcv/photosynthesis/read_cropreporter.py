# Read in fluorescence images from a .DAT file

import os
import numpy as np
import xarray as xr
from plantcv.plantcv import params
from plantcv.plantcv.plot_image import plot_image
from plantcv.plantcv.print_image import print_image


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
    frames_expected = [key.upper()[0:3] for key,value in frames_captured.items() if str(value) == "1"]
    corresponding_dict = {"FVF":"PSD", "FQF": "PSL", "CHL":"CHL", "NPQ":"NPQ", "SPC":"SPC",
                          "CLR":"CLR", "RFD":"RFD", "GFP":"GFP", "RFP":"RFP"}

    print(inf_dict)
    all_imgs = {}
    param_labels = []
    all_xarrays = []
    # Loop over all raw bin files
    for key in frames_expected:
        inf = os.path.split(inf_filename)[-1]
        path = os.path.dirname(inf_filename)
        filename_components = inf.split("_")
        filename_components[1] = corresponding_dict[key]

        s = "_"
        bin_filenames = s.join(filename_components)
        bin_filename = bin_filenames.replace(".INF", ".DAT")
        bin_filepath = os.path.join(path, bin_filename)
        raw_data = np.fromfile(bin_filepath, np.uint16, -1)
        #img_cube = raw_data.reshape(int(len(raw_data) / (y * x)), x, y).transpose((2, 1, 0)) #numpy shaped
        img_cube = raw_data.reshape(int(len(raw_data) / (y * x)), x, y).transpose((1, 2, 0))
        all_imgs[corresponding_dict[key]] = img_cube # store each data cube into a dictionary with labeled source

        x_coord = np.arange(x)
        y_coord = np.arange(y)
        index_list = np.arange(np.shape(all_imgs[corresponding_dict[key]])[2])

        param_label = [corresponding_dict[key]]*(np.shape(img_cube)[2]) # repetitive list of parameter labels
        param_labels = param_labels + [corresponding_dict[key]] # concat onto list of all slices in the data cube

        # Create x-array data array
        da = xr.DataArray(img_cube[None, ...], dims=["parameter", "x", "y", "frame"], coords= {"index":index_list})
        all_xarrays.append(da)

        print("total data array shape:" + str(np.shape(img_cube)))
        print("^" + corresponding_dict[key])

    # Join data array from each bin file into a single array
    all_xarrays = xr.concat(all_xarrays, 'parameter')
    # Add labels
    param_labels = pd.Index(param_labels)
    all_xarrays.coords['parameter'] = param_labels
    #plot_image(img_cube[:, :, [0]])
    return inf_dict, all_imgs, all_xarrays
