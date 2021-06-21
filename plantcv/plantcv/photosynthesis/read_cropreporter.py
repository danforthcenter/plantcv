# Read in fluorescence images from a .DAT file

import os
import numpy as np
import xarray as xr
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import PSII_data
from skimage.util import img_as_ubyte


def read_cropreporter(filename):
    """
    Read datacubes from PhenoVation B.V. CropReporter into a PSII_Data instance.

    Inputs:
        filename        = CropReporter .INF filename

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
    # ignore NPQ
    for i,k in enumerate(frames_expected):
        if 'NPQ' == k:
            frames_expected = [*frames_expected[0:i], *frames_expected[-i:]]

    corresponding_dict = {"FVF": "PSD", "FQF": "PSL", "CHL": "CHL", "SPC": "SPC",
                          "CLR": "CLR", "RFD": "RFD", "GFP": "GFP", "RFP": "RFP"}
    
    # Initialize lists
    img_frames = []
    ps = PSII_data()
    
    # INF file prefix and path
    inf_filename = os.path.split(filename)[-1]
    imgpath = os.path.dirname(filename)
    filename_components = inf_filename.split("_")

    # Loop over all raw bin files
    key = frames_expected[0]
    for key in frames_expected:
        print('Compiling:', corresponding_dict[key])
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

        # Calculate frames of interest and keep track of their labels. labels must be unique across all measurments
        frame_labels = [(corresponding_dict[key]+str(i)) for i in range(img_cube.shape[2])]
        frame_nums = np.arange(img_cube.shape[2])
        
        if corresponding_dict[key] == "PSD":
            F0_frame = int(metadata_dict["FvFmFrameF0"])+1 #data cube includes Fdark at the beginning
            Fm_frame = int(metadata_dict["FvFmFrameFm"])+1
            frame_labels[0] = 'Fdark'
            frame_labels[F0_frame] = 'F0'
            frame_labels[Fm_frame] = 'Fm'
            psd = xr.DataArray(
                data=img_cube[...,None],
                dims=('x','y','frame_label', 'measurement'),
                coords={'frame_label': frame_labels,
                        'frame_num' : ('frame_label', frame_nums),
                        'measurement' : ['t0']},
                name='darkadapted'
                )
            psd.attrs["long_name"] = "dark-adapted measurements"
            ps.add_data(psd)
            
            _debug(visual=ps.darkadapted,
                   filename=os.path.join(params.debug_outdir, f"{str(params.device)}_PSD-{frame_labels[-1]}.png"))

        elif corresponding_dict[key] == "PSL":
            Fsp_frame = int(metadata_dict["FqFmFrameFsp"])+1
            Fmp_frame = int(metadata_dict["FqFmFrameFmp"])+1
            frame_labels[0] = "Flight"
            frame_labels[Fsp_frame] = 'Fp'
            frame_labels[Fmp_frame] = 'Fmp'
            psl = xr.DataArray(
                data=img_cube[..., None],
                dims=('x','y','frame_label','measurement'),
                coords={'frame_label': frame_labels,
                        'frame_num' : ('frame_label', frame_nums),
                        'measurement' : ['t1']},
                name='lightadapted'
                )
            psl.attrs["long_name"] = "light-adapted measurements"
            ps.add_data(psl)

            _debug(visual=ps.lightadapted,
                   filename=os.path.join(params.debug_outdir, f"{str(params.device)}_PSL-{frame_labels[-1]}.png"))

        elif corresponding_dict[key] == "CLR":
            frame_labels = ["Red", "Green", "Blue"]
            debug = params.debug
            params.debug = None
            red = img_as_ubyte(img_cube[:, :, 0])# I don't think we can use rescale here because it will change the ratios of red to green to blue since it scales based on min-max rather than 0-255
            green = img_as_ubyte(img_cube[:, :, 1])
            blue = img_as_ubyte(img_cube[:, :, 2])
            rgb_img = np.dstack([blue, green, red])
            rgb = xr.DataArray(
                data=rgb_img,
                dims=('x','y','frame_label'),
                coords={'frame_label': frame_labels},
                name='rgb'
                )
            rgb.attrs["long_name"] = "rgb measurements"
            ps.add_data(rgb)

            params.debug = debug
            _debug(visual=ps.rgb, #does it make sense to show all three bands separately?
                   filename=os.path.join(params.debug_outdir, f"{str(params.device)}_CLR-RGB.png"))

        elif corresponding_dict[key] == "CHL":
            frame_labels = ["Chl", "Chl-NIR"]
            chl = xr.DataArray(
                data=img_cube,
                dims=('x','y','frame_label'),
                coords={'frame_label': frame_labels},
                name = 'chlorophyll'
                )
            chl.attrs["long_name"] = "chlorophyll measurements"
            ps.add_data(chl)

            _debug(visual=ps.chlorophyll,
                   filename=os.path.join(params.debug_outdir, f"{str(params.device)}_CHL-NIR.png"))

        elif corresponding_dict[key] == "SPC":
            frame_labels = ["Anth", "Far-red", "Anth-NIR"]
            spc = xr.DataArray(
                data=img_cube,
                dims=('x','y','frame_label'),
                coords={'frame_label': frame_labels},
                name='anthocyanin'
                )
            spc.attrs["long_name"] = "anthocyanin measurements"
            ps.add_data(spc)

            _debug(visual=ps.anthocyanin,
                   filename=os.path.join(params.debug_outdir, f"{str(params.device)}_SPC-Anth.png"))

    return ps, imgpath, inf_filename
