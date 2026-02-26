"""Read in fluorescence images from a .DAT file."""
import os
import numpy as np
import xarray as xr
from plantcv.plantcv._globals import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import PSII_data
from plantcv.plantcv import Spectral_data
from skimage.util import img_as_ubyte


def read_cropreporter(filename):
    """
    Read datacubes from PhenoVation B.V. CropReporter into a PSII_Data instance.

    Inputs:
        filename        = CropReporter .INF filename

    Returns:
        ps               = photosynthesis data in xarray DataArray format

    :param filename: str
    :return ps: plantcv.plantcv.classes.PSII_data
    """
    # Initialize metadata dictionary
    metadata_dict = {}

    # Parse .inf file and create dictionary with metadata stored within
    with open(filename, "r") as fp:
        for line in fp:
            if "=" in line:
                key, value = line.rstrip("\n").split("=")
                metadata_dict[key] = value

    # Initialize PSII_data class
    ps = PSII_data()

    # INF file prefix and path
    ps.filename = os.path.split(filename)[-1]
    ps.datapath = os.path.dirname(filename)

    # Dark-adapted measurements
    _process_psd_data(ps=ps, metadata=metadata_dict)

    # Light-adapted measurements
    _process_psl_data(ps=ps, metadata=metadata_dict)

    # NPQ measurements
    _process_npq_data(ps=ps, metadata=metadata_dict)

    # Dark-adapted PAM measurements
    _process_pmd_data(ps=ps, metadata=metadata_dict)

    # Light-adapted PAM measurements
    _process_pml_data(ps=ps, metadata=metadata_dict)

    # PAM time (dark, light, and second dark adapted) measurements
    _process_pmt_data(ps=ps, metadata=metadata_dict)

    # Chlorophyll fluorescence data
    _process_chl_data(ps=ps, metadata=metadata_dict)

    # Spectral measurements
    _process_spc_data(ps=ps, metadata=metadata_dict)

    # GFP fluorescence intensity data
    _process_gfp_data(ps=ps, metadata=metadata_dict)

    # RFP fluorescence intensity data
    _process_rfp_data(ps=ps, metadata=metadata_dict)

    # APH reflectance data
    _process_aph_data(ps=ps, metadata=metadata_dict)

    return ps


def _process_psd_data(ps, metadata):
    """
    Create an xarray DataArray for a PSD dataset.

    Inputs:
        ps       = PSII_data instance
        metadata = INF file metadata dictionary

    :param ps: plantcv.plantcv.classes.PSII_data
    :param metadata: dict
    """
    bin_filepath = _dat_filepath(dataset="PSD", datapath=ps.datapath, filename=ps.filename)
    if os.path.exists(bin_filepath):
        img_cube, frame_labels, frame_nums = _read_dat_file(dataset="PSD", filename=bin_filepath,
                                                            height=int(metadata["ImageRows"]),
                                                            width=int(metadata["ImageCols"]))
        # If not all frames are saved the order is fixed
        # Phenovation does not update the framenumbers in the references.
        # Default frames (when SaveAllFrames == 0)
        f0_frame = 1
        fm_frame = 2
        # If the method is labeled FvFm
        if 'FvFmFrameF0' in metadata and metadata["SaveAllFrames"] != "0":
            f0_frame = int(metadata["FvFmFrameF0"]) + 1
            fm_frame = int(metadata["FvFmFrameFm"]) + 1
        # If the method is labeled DkOjip
        if 'DkOjipFrameF0' in metadata and metadata["SaveAllFrames"] != "0":
            f0_frame = int(metadata["DkOjipFrameF0"]) + 1  # data cube includes Fdark at the beginning
            fm_frame = int(metadata["DkOjipFrameFm"]) + 1
        frame_labels[0] = 'Fdark'
        frame_labels[f0_frame] = 'F0'
        frame_labels[fm_frame] = 'Fm'
        psd = xr.DataArray(
            data=img_cube[..., None],
            dims=('x', 'y', 'frame_label', 'measurement'),
            coords={'frame_label': frame_labels,
                    'frame_num': ('frame_label', frame_nums),
                    'measurement': ['t0']},
            name='ojip_dark'
        )
        psd.attrs["long_name"] = "OJIP dark-adapted measurements"
        ps.add_data(psd)

        _debug(visual=ps.ojip_dark.squeeze('measurement', drop=True),
               filename=os.path.join(params.debug_outdir, f"{str(params.device)}_PSD-frames.png"),
               col='frame_label',
               col_wrap=int(np.ceil(ps.ojip_dark.frame_label.size / 4)))


def _process_psl_data(ps, metadata):
    """
    Create an xarray DataArray for a PSL dataset.

    Inputs:
        ps       = PSII_data instance
        metadata = INF file metadata dictionary

    :param ps: plantcv.plantcv.classes.PSII_data
    :param metadata: dict
    """
    bin_filepath = _dat_filepath(dataset="PSL", datapath=ps.datapath, filename=ps.filename)
    if os.path.exists(bin_filepath):
        img_cube, frame_labels, frame_nums = _read_dat_file(dataset="PSL", filename=bin_filepath,
                                                            height=int(metadata["ImageRows"]),
                                                            width=int(metadata["ImageCols"]))
        # If not all frames are saved the order is fixed
        # Phenovation does not update the framenumbers in the references.
        # Default frames (when SaveAllFrames == 0)
        fsp_frame = 1
        fmp_frame = 2
        # If the method is labeled FqFm
        if 'FqFmFrameFsp' in metadata and metadata["SaveAllFrames"] != "0":
            fsp_frame = int(metadata["FqFmFrameFsp"]) + 1
            fmp_frame = int(metadata["FqFmFrameFmp"]) + 1
        # If the method is labeled LtOjip
        if 'LtOjipFrameFsp' in metadata and metadata["SaveAllFrames"] != "0":
            fsp_frame = int(metadata["LtOjipFrameFsp"]) + 1
            fmp_frame = int(metadata["LtOjipFrameFmp"]) + 1
        frame_labels[0] = "Flight"
        frame_labels[fsp_frame] = 'Fp'
        frame_labels[fmp_frame] = 'Fmp'
        psl = xr.DataArray(
            data=img_cube[..., None],
            dims=('x', 'y', 'frame_label', 'measurement'),
            coords={'frame_label': frame_labels,
                    'frame_num': ('frame_label', frame_nums),
                    'measurement': ['t1']},
            name='ojip_light'
        )
        psl.attrs["long_name"] = "OJIP light-adapted measurements"
        ps.add_data(psl)

        _debug(visual=ps.ojip_light.squeeze('measurement', drop=True),
               filename=os.path.join(params.debug_outdir, f"{str(params.device)}_PSL-frames.png"),
               col='frame_label',
               col_wrap=int(np.ceil(ps.ojip_light.frame_label.size / 4)))


def _process_npq_data(ps, metadata):
    """
    Create an xarray DataArray for a NPQ dataset.

    Parameters
    ----------
    ps : plantcv.plantcv.classes.PSII_data
        PSII_data instance
    metadata : dict
        INF file metadata dictionary
    """
    bin_filepath = _dat_filepath(dataset="NPQ", datapath=ps.datapath, filename=ps.filename)
    if os.path.exists(bin_filepath):
        img_cube, frame_labels, frame_nums = _read_dat_file(dataset="NPQ", filename=bin_filepath,
                                                            height=int(metadata["ImageRows"]),
                                                            width=int(metadata["ImageCols"]))
        # Add the OJIP dark frames
        frame_labels[0] = 'Fdark'
        frame_labels[1] = 'F0'
        frame_labels[2] = 'Fm'
        psd = xr.DataArray(
            data=img_cube[:, :, 0:3, None],
            dims=('x', 'y', 'frame_label', 'measurement'),
            coords={'frame_label': frame_labels[0:3],
                    'frame_num': ('frame_label', frame_nums[0:3]),
                    'measurement': ['t0']},
            name='ojip_dark'
        )
        psd.attrs["long_name"] = "OJIP dark-adapted measurements"
        ps.add_data(psd)

        _debug(visual=ps.ojip_dark.squeeze('measurement', drop=True),
               filename=os.path.join(params.debug_outdir, f"{str(params.device)}_PSD-frames.png"),
               col='frame_label',
               col_wrap=int(np.ceil(ps.ojip_dark.frame_label.size / 4)))

        # Add the OJIP light frames
        frame_labels[3] = 'Flight'
        frame_labels[4] = 'Fp'
        frame_labels[5] = 'Fmp'
        psd = xr.DataArray(
            data=img_cube[:, :, 3:6, None],
            dims=('x', 'y', 'frame_label', 'measurement'),
            coords={'frame_label': frame_labels[3:6],
                    'frame_num': ('frame_label', frame_nums[3:6]),
                    'measurement': ['t0']},
            name='ojip_light'
        )
        psd.attrs["long_name"] = "OJIP light-adapted measurements"
        ps.add_data(psd)

        _debug(visual=ps.ojip_light.squeeze('measurement', drop=True),
               filename=os.path.join(params.debug_outdir, f"{str(params.device)}_PSL-frames.png"),
               col='frame_label',
               col_wrap=int(np.ceil(ps.ojip_light.frame_label.size / 4)))


def _process_pmd_data(ps, metadata):
    """
    Create an xarray DataArray for a PMD dataset.

    Inputs:
        ps       = PSII_data instance
        metadata = INF file metadata dictionary

    :param ps: plantcv.plantcv.classes.PSII_data
    :param metadata: dict
    """
    bin_filepath = _dat_filepath(dataset="PMD", datapath=ps.datapath, filename=ps.filename)
    if os.path.exists(bin_filepath):
        img_cube, frame_labels, frame_nums = _read_dat_file(dataset="PMD", filename=bin_filepath,
                                                            height=int(metadata["ImageRows"]),
                                                            width=int(metadata["ImageCols"]))
        frame_labels = ["Fdark", "F0", "Fm", "Fdarksat"]
        pmd = xr.DataArray(
            data=img_cube[..., None],
            dims=('x', 'y', 'frame_label', 'measurement'),
            coords={'frame_label': frame_labels,
                    'frame_num': ('frame_label', frame_nums),
                    'measurement': ['t0']},
            name='pam_dark'
        )
        pmd.attrs["long_name"] = "pam dark-adapted measurements"
        ps.add_data(pmd)

        _debug(visual=ps.pam_dark.squeeze('measurement', drop=True),
               filename=os.path.join(params.debug_outdir, f"{str(params.device)}_PMD-frames.png"),
               col='frame_label',
               col_wrap=int(np.ceil(ps.pam_dark.frame_label.size / 4)))


def _process_pml_data(ps, metadata):
    """
    Create an xarray DataArray for a PML dataset.

    Inputs:
        ps       = PSII_data instance
        metadata = INF file metadata dictionary

    :param ps: plantcv.plantcv.classes.PSII_data
    :param metadata: dict
    """
    bin_filepath = _dat_filepath(dataset="PML", datapath=ps.datapath, filename=ps.filename)
    if os.path.exists(bin_filepath):
        img_cube, frame_labels, frame_nums = _read_dat_file(dataset="PML", filename=bin_filepath,
                                                            height=int(metadata["ImageRows"]),
                                                            width=int(metadata["ImageCols"]))
        frame_labels = ["Flight", "Fp", "Fmp", "Flightsat"]
        pml = xr.DataArray(
            data=img_cube[..., None],
            dims=('x', 'y', 'frame_label', 'measurement'),
            coords={'frame_label': frame_labels,
                    'frame_num': ('frame_label', frame_nums),
                    'measurement': ['t0']},
            name='pam_light'
        )
        pml.attrs["long_name"] = "pam light-adapted measurements"
        ps.add_data(pml)

        _debug(visual=ps.pam_light.squeeze('measurement', drop=True),
               filename=os.path.join(params.debug_outdir, f"{str(params.device)}_PML-frames.png"),
               col='frame_label',
               col_wrap=int(np.ceil(ps.pam_light.frame_label.size / 4)))


def _process_pmt_data(ps, metadata):
    """
    Create an xarray DataArray for a PMT dataset with measurements stored
    along the `measurement` dimension (t0, t1, ...), not encoded in frame labels.

    Inputs:
        ps       = PSII_data instance
        metadata = INF file metadata dictionary
    """
    bin_filepath = _dat_filepath(dataset="PMT", datapath=ps.datapath, filename=ps.filename)

    if not os.path.exists(bin_filepath):
        return

    img_cube, _, _ = _read_dat_file(
        dataset="PMT",
        filename=bin_filepath,
        height=int(metadata["ImageRows"]),
        width=int(metadata["ImageCols"])
    )

    # metadata-driven measurement counts
    n_fqfm = int(metadata.get("TmPamMeasFqfm", 0))
    n_fvfm = int(metadata.get("TmPamMeasFvfm", 0)) - 1

    # t0 = initial dark, then fqfm blocks, then fvfm blocks
    measurement_labels = [f"t{i}" for i in range(1 + n_fqfm + n_fvfm)]

    # canonical frame labels (no suffixes)
    frame_labels = [
        "Fdark", "F0", "Fm", "Fdarksat",
        "Flight", "Fsp", "Fmp", "Flightsat",
        "Fdarkpp", "F0pp", "Fmpp", "Fdarksatpp",
        "F0p"
    ]

    n_x, n_y, _ = img_cube.shape

    # initialize output cube: (x, y, frame_label, measurement)
    pmt_data = np.zeros(
        (n_x, n_y, len(frame_labels), len(measurement_labels)),
        dtype=img_cube.dtype
        )

    idx = 0  # frame counter in raw img_cube

    # t0: dark-adapted block
    for f in ["Fdark", "F0", "Fm", "Fdarksat"]:
        pmt_data[:, :, frame_labels.index(f), 0] = img_cube[:, :, idx]
        idx += 1

    # Fq'/Fm' light-adapted blocks
    for meas in range(1, 1 + n_fqfm):
        for f in ["Flight", "Fsp", "Fmp", "Flightsat"]:
            pmt_data[:, :, frame_labels.index(f), meas] = img_cube[:, :, idx]
            idx += 1

    # Fq"/Fm" dark blocks
    base = 1 + n_fqfm
    for j in range(n_fvfm):
        meas = base + j
        for f in ["Fdarkpp", "F0pp", "Fmpp", "Fdarksatpp"]:
            pmt_data[:, :, frame_labels.index(f), meas] = img_cube[:, :, idx]
            idx += 1

    # final frame is always F0p (last measurement) per Phenovation file types
    pmt_data[:, :, frame_labels.index("F0p"), -1] = img_cube[:, :, -1]

    # build DataArray
    pmt = xr.DataArray(
        data=pmt_data,
        dims=("x", "y", "frame_label", "measurement"),
        coords={
            "frame_label": frame_labels,
            "measurement": measurement_labels
        },
        name="pam_time"
    )

    pmt.attrs["long_name"] = "pam time measurements"
    ps.add_data(pmt)

    # debug visualization
    _debug(
        visual=ps.pam_time.isel(measurement=-1),
        filename=os.path.join(
            params.debug_outdir,
            f"{str(params.device)}_PMT-frames.png"
        ),
        col="frame_label",
        col_wrap=int(np.ceil(len(frame_labels) / 4))
    )


def _process_chl_data(ps, metadata):
    """
    Create an xarray DataArray for a CHL dataset.

    Inputs:
        ps       = PSII_data instance
        metadata = INF file metadata dictionary

    :param ps: plantcv.plantcv.classes.PSII_data
    :param metadata: dict
    """
    bin_filepath = _dat_filepath(dataset="CHL", datapath=ps.datapath, filename=ps.filename)
    if os.path.exists(bin_filepath):
        img_cube, frame_labels, _ = _read_dat_file(dataset="CHL", filename=bin_filepath,
                                                   height=int(metadata["ImageRows"]),
                                                   width=int(metadata["ImageCols"]))
        frame_labels = ["Fdark", "Chl"]
        chl = xr.DataArray(
            data=img_cube,
            dims=('x', 'y', 'frame_label'),
            coords={'frame_label': frame_labels},
            name='chlorophyll'
        )
        chl.attrs["long_name"] = "chlorophyll measurements"
        ps.add_data(chl)

        _debug(visual=ps.chlorophyll,
               filename=os.path.join(params.debug_outdir, f"{str(params.device)}_CHL-frames.png"),
               col='frame_label',
               col_wrap=int(np.ceil(ps.chlorophyll.frame_label.size / 4)))


def _process_spc_data(ps, metadata):
    """
    Create a Spectral_data object for the SPC and CLR datasets.

    Inputs:
        ps       = PSII_data instance
        metadata = INF file metadata dictionary

    :param ps: plantcv.plantcv.classes.PSII_data
    :param metadata: dict
    """
    img_cubes = []
    wavelengths = []
    clr_filepath = _dat_filepath(dataset="CLR", datapath=ps.datapath, filename=ps.filename)
    spc_filepath = _dat_filepath(dataset="SPC", datapath=ps.datapath, filename=ps.filename)
    rgb = None
    if os.path.exists(clr_filepath):
        rgb_cube, _, _ = _read_dat_file(dataset="CLR", filename=clr_filepath,
                                        height=int(metadata["ImageRows"]),
                                        width=int(metadata["ImageCols"]))
        img_cubes.append(rgb_cube)
        wavelengths += [640, 550, 475]
        rgb = img_as_ubyte(rgb_cube[:, :, [2, 1, 0]])
    if os.path.exists(spc_filepath):
        spc_cube, _, _ = _read_dat_file(dataset="SPC", filename=spc_filepath,
                                        height=int(metadata["ImageRows"]),
                                        width=int(metadata["ImageCols"]))
        img_cubes.append(spc_cube)
        wavelengths += [540, 710, 770]
        if rgb is None:
            rgb = img_as_ubyte(spc_cube)

    if len(img_cubes) > 0:
        if len(img_cubes) == 2:
            # Concatenate the images on the depth/spectral (z) axis
            array_data = np.concatenate(img_cubes, axis=2)
        else:
            array_data = img_cubes[0]

        # sort all wavelengths
        wavelengths = np.array(wavelengths)
        ind = np.argsort(wavelengths)
        wavelengths = wavelengths[ind]

        wavelength_dict = {}
        for (idx, wv) in enumerate(wavelengths):
            wavelength_dict[wv] = float(idx)

        # sort array_data based on wavelengths
        array_data = array_data[:, :, ind]
        # Scale the array data to 0-1 by dividing by the maximum data type value
        array_data = (array_data / np.iinfo(array_data.dtype).max).astype(np.float32)

        # Create a Spectral_data object
        rows, columns = array_data.shape[0:2]
        multispec = Spectral_data(array_data=array_data,
                                  max_wavelength=float(max(wavelengths)),
                                  min_wavelength=float(min(wavelengths)),
                                  max_value=float(np.amax(array_data)),
                                  min_value=float(np.amin(array_data)),
                                  d_type=array_data.dtype,
                                  wavelength_dict=wavelength_dict,
                                  samples=columns, lines=rows, interleave="NA",
                                  wavelength_units="nm", array_type="multispectral",
                                  pseudo_rgb=rgb, filename="NA", default_bands=None)

        ps.spectral = multispec

        _debug(visual=ps.spectral.pseudo_rgb,
               filename=os.path.join(params.debug_outdir, f"{str(params.device)}_spectral-RGB.png"))


def _process_gfp_data(ps, metadata):
    """
    Create an xarray DataArray for a GFP dataset.

    Parameters
    ----------
    ps : plantcv.plantcv.classes.PSII_data
        PSII_data instance
    metadata : dict
        INF file metadata dictionary
    """
    bin_filepath = _dat_filepath(dataset="GFP", datapath=ps.datapath, filename=ps.filename)
    if os.path.exists(bin_filepath):
        img_cube, frame_labels, frame_nums = _read_dat_file(dataset="GFP", filename=bin_filepath,
                                                            height=int(metadata["ImageRows"]),
                                                            width=int(metadata["ImageCols"]))
        frame_labels = ["Fdark", "GFP", "Auto"]
        gfp = xr.DataArray(
            data=img_cube,
            dims=('x', 'y', 'frame_label'),
            coords={'frame_label': frame_labels,
                    'frame_num': ('frame_label', frame_nums)},
            name='gfp'
        )
        gfp.attrs["long_name"] = "Green fluorescence protein fluorescence intensity (525nm GFP, 585nm Auto)"
        gfp.attrs["dark_comp_on"] = int(metadata.get("GfpDarkCompOn", "0"))
        gfp.attrs["calib_factor"] = float(metadata.get("GfpCalibFactor", metadata.get("GfpCalFactor", "nan")))
        gfp.attrs["meas_power"] = float(metadata.get("GfpMeasPower", "nan"))
        gfp.attrs["shutter"] = float(metadata.get("GfpShutter", metadata.get("GfpShutterFrames", "nan")))
        ps.add_data(gfp)

        _debug(visual=ps.gfp,
               filename=os.path.join(params.debug_outdir, f"{str(params.device)}_GFP-frames.png"),
               col='frame_label',
               col_wrap=int(np.ceil(ps.gfp.frame_label.size / 4)))


def _process_rfp_data(ps, metadata):
    """
    Create an xarray DataArray for a RFP dataset.

    Parameters
    ----------
    ps : plantcv.plantcv.classes.PSII_data
        PSII_data instance.
    metadata : dict
        INF file metadata dictionary.

    """
    bin_filepath = _dat_filepath(dataset="RFP", datapath=ps.datapath, filename=ps.filename)
    if os.path.exists(bin_filepath):
        img_cube, frame_labels, frame_nums = _read_dat_file(dataset="RFP", filename=bin_filepath,
                                                            height=int(metadata["ImageRows"]),
                                                            width=int(metadata["ImageCols"]))
        frame_labels = ["Fdark", "RFP"]
        rfp = xr.DataArray(
            data=img_cube,
            dims=('x', 'y', 'frame_label'),
            coords={'frame_label': frame_labels,
                    'frame_num': ('frame_label', frame_nums)},
            name='rfp'
        )
        rfp.attrs["long_name"] = "Red fluorescence protein fluorescence intensity (585nm)"
        rfp.attrs["dark_comp_on"] = int(metadata.get("RfpDarkCompOn", "0"))
        rfp.attrs["calib_factor"] = float(metadata.get("RfpCalibFactor", "nan"))
        rfp.attrs["meas_power"] = float(metadata.get("RfpMeasPower", "nan"))
        rfp.attrs["shutter"] = float(metadata.get("RfpShutter", metadata.get("RfpShutterFrames", "nan")))
        ps.add_data(rfp)

        _debug(visual=ps.rfp,
               filename=os.path.join(params.debug_outdir, f"{str(params.device)}_RFP-frames.png"),
               col='frame_label',
               col_wrap=int(np.ceil(ps.rfp.frame_label.size / 4)))


def _process_aph_data(ps, metadata):
    """
    Create an xarray DataArray for an APH dataset.

    Parameters
    ----------
    ps : plantcv.plantcv.classes.PSII_data
        PSII_data instance.
    metadata : dict
        INF file metadata dictionary.

    """
    bin_filepath = _dat_filepath(dataset="APH", datapath=ps.datapath, filename=ps.filename)
    if os.path.exists(bin_filepath):
        img_cube, frame_labels, frame_nums = _read_dat_file(dataset="APH", filename=bin_filepath,
                                                            height=int(metadata["ImageRows"]),
                                                            width=int(metadata["ImageCols"]))
        frame_labels = ["Red", "FarRed"]
        aph = xr.DataArray(
            data=img_cube,
            dims=('x', 'y', 'frame_label'),
            coords={'frame_label': frame_labels,
                    'frame_num': ('frame_label', frame_nums)},
            name='aph'
        )
        aph.attrs["long_name"] = "Alpha Light absorption coefficient (Reflection) (640nm Red, 732nm FarRed)"
        aph.attrs["dark_comp_on"] = int(metadata.get("AphDarkCompOn", metadata.get("AlphaDarkCompOn", "0")))
        aph.attrs["gain_red"] = float(metadata.get("AphGainRed", metadata.get("AlphaGainRed", "nan")))
        aph.attrs["gain_farred"] = float(metadata.get("AphGainFarRed", metadata.get("AlphaGainFarRed", "nan")))
        ps.add_data(aph)

        _debug(
            visual=ps.aph,
            filename=os.path.join(params.debug_outdir, f"{str(params.device)}_APH-frames.png"),
            col='frame_label',
            col_wrap=int(np.ceil(ps.aph.frame_label.size / 4))
        )


def _dat_filepath(dataset, datapath, filename):
    """
    Create the filepath to a DAT file based on the INF filename.

    Inputs:
        dataset  = dataset key (PSD, PSL, SPC, CHL, CLR)
        datapath = path to the dataset (basepath of the INF file)
        filename = INF filename

    Returns:
        bin_filepath = fully-qualified path to the DAT file

    :param dataset: str
    :param datapath: str
    :param filename: str
    :return bin_filepath: str
    """
    filename_components = filename.split("_")
    # Find corresponding bin img filepath based on .INF filepath
    # replace header with bin img type
    filename_components[filename_components.index('HDR')] = dataset
    bin_filenames = "_".join(filename_components)
    bin_filename = bin_filenames.replace(".INF", ".DAT")
    bin_filepath = os.path.join(datapath, bin_filename)

    return bin_filepath


def _read_dat_file(dataset, filename, height, width):
    """
    Read raw data from DAT file.

    Inputs:
        dataset  = dataset key (PSD, PSL, SPC, CHL, CLR)
        filename = fully-qualified path to the DAT file
        height   = height (rows) of the images
        width    = width (columns) of the image

    Returns:
        img_cube     = raw data cube in NumPy shape
        frame_labels = list of labels for each frame
        frame_nums   = the number of frames

    :param dataset: str
    :param filename: str
    :param height: int
    :param width: int
    :return img_cube: numpy.ndarray
    :return frame_labels: list
    :return frame_numbs: int
    """
    print(f'Compiling: {dataset}')
    # Dump in bin img data
    raw_data = np.fromfile(filename, np.uint16, -1)
    # Reshape, numpy shaped
    img_cube = raw_data.reshape(int(len(raw_data) / (height * width)), width, height).transpose((2, 1, 0))

    # Calculate frames of interest and keep track of their labels. labels must be unique across all measurements
    frame_labels = [(dataset + str(i)) for i in range(img_cube.shape[2])]
    frame_nums = np.arange(img_cube.shape[2])

    return img_cube, frame_labels, frame_nums
