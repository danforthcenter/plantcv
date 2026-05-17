"""Read in fluorescence images from a .DAT file."""
import os
import numpy as np
import xarray as xr
from plantcv.plantcv._globals import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import PSII_data
from plantcv.plantcv import Spectral_data
from plantcv.plantcv.classes import NamedImageCollection
from skimage.util import img_as_ubyte


class CHL:
    """Chlorophyll dataset. Stores the file path at init; image data is loaded on first access."""

    def __init__(self, filepath, height, width):
        """Initialize CHL dataset with file path and image dimensions."""
        self._filepath = filepath
        self._height = height
        self._width = width
        self._chlorophyll = None

    def __bool__(self):
        """The existence of the CHL class is true."""
        return True

    def __repr__(self):
        """String representation of the CHL dataset, indicating whether the data has been loaded."""
        loaded = self._chlorophyll is not None
        return f"CHL(filepath={self._filepath!r}, loaded={loaded})"

    @property
    def chlorophyll(self):
        """Return the chlorophyll frame as a NumPy array."""
        if self._chlorophyll is None:
            self._load()
        return self._chlorophyll

    def _load(self):
        """Load the chlorophyll frame from the .DAT file."""
        img_cube, _, _ = _read_dat_file(
            dataset="CHL",
            filename=str(self._filepath),
            height=self._height,
            width=self._width,
        )
        # index 0 = Fdark (when present), last index = Chl
        self._chlorophyll = img_cube[:, :, img_cube.shape[2] - 1]


def read_cropreporter(filename):
    """Read datacubes from PhenoVation B.V. CropReporter or PlantExplorer cameras into a PSII_data instance.

    Parameters
    ----------
    filename : str
        .INF filename

    Returns
    -------
    plantcv.plantcv.classes.PSII_data
        photosynthesis data in xarray or NumPy format.
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
    ps = PSII_data(metadata=metadata_dict)

    # INF file prefix and path
    ps.filename = os.path.split(filename)[-1]
    ps.datapath = os.path.dirname(filename)

    # Image dimensions (assumed to be consistent across all datasets for a given acquisition)
    height = int(ps.metadata["ImageRows"])
    width = int(ps.metadata["ImageCols"])

    # Dataset-specific processing functions. Class constructors for lazy loading.
    dataset_classes = {
        # Chlorophyll fluorescence data
        "CHL": lambda fp: CHL(filepath=fp, height=height, width=width),
    }

    # Process datasets
    for dataset in ["APH", "CHL", "CLR", "NPQ", "PMD", "PML", "PMT", "PSD", "PSL", "SPC"]:
        # Construct the expected binary file path for the dataset
        bin_filepath = _dat_filepath(dataset=dataset, datapath=ps.datapath, filename=ps.filename)
        # Check if the file exists
        if os.path.exists(bin_filepath):
            key = dataset.lower()
            # Get the class constructor
            constructor = dataset_classes.get(dataset)
            if constructor is not None:
                # Set the attribute on the PSII_data instance to a lazy-loading object
                setattr(ps, key, constructor(bin_filepath))

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
        ps.ojip_dark = psd

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
        ps.ojip_light = psl

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
        ps.ojip_dark = psd

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
        ps.ojip_light = psd

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
        ps.pam_dark = pmd

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
        ps.pam_light = pml

        _debug(visual=ps.pam_light.squeeze('measurement', drop=True),
               filename=os.path.join(params.debug_outdir, f"{str(params.device)}_PML-frames.png"),
               col='frame_label',
               col_wrap=int(np.ceil(ps.pam_light.frame_label.size / 4)))


def _process_pmt_data(ps, metadata):
    """
    Create an xarray DataArray for a PMT dataset.

    Parameters
    ----------
    ps : plantcv.plantcv.classes.PSII_data
        PSII_data instance.
    metadata : dict
        INF file metadata dictionary.

    Notes
    -----
    Measurements are stored along the `measurement` dimension (t0, t1, ...),
    not encoded in frame labels.
    """
    bin_filepath = _dat_filepath(dataset="PMT", datapath=ps.datapath, filename=ps.filename)

    if os.path.exists(bin_filepath):
        img_cube, _, _ = _read_dat_file(
            dataset="PMT",
            filename=bin_filepath,
            height=int(metadata["ImageRows"]),
            width=int(metadata["ImageCols"])
        )

        # metadata-driven measurement counts
        n_fqfm = int(metadata.get("TmPamMeasFqfm", 0))
        # TmPamMeasFvfm=1 means only the baseline dark-adapted block exists, so n_fvfm should be 0
        n_fvfm = max(0, int(metadata.get("TmPamMeasFvfm", 0)) - 1)

        # Initialize with the base requirement
        blocks = [{"labels": ["Fdark", "F0", "Fm", "Fdarksat"], "count": 1, "start_meas": 0}]

        # Handle the absence of Light/Quenching measurements
        if n_fqfm > 0:
            blocks.append({"labels": ["Flight", "Fp", "Fmp", "Flightsat"], "count": n_fqfm, "start_meas": 1})

        # Handle the absence of Variable Fluorescence measurements
        if n_fvfm > 0:
            blocks.append({"labels": ["Fdarkpp", "F0pp", "Fmpp", "Fdarksatpp"], "count": n_fvfm, "start_meas": 1 + n_fqfm})

        # Flatten labels explicitly so coverage tools can "see" each step
        frame_labels = []
        for b in blocks:
            for label in b["labels"]:
                frame_labels.append(label)
        frame_labels.append("F0p")

        measurement_labels = [f"t{i}" for i in range(1 + n_fqfm + n_fvfm)]

        # Initialize and fill data
        n_x, n_y, n_frames = img_cube.shape
        pmt_data = np.zeros((n_x, n_y, len(frame_labels), len(measurement_labels)), dtype=img_cube.dtype)

        idx = 0
        for block in blocks:
            for m_offset in range(block["count"]):
                meas_idx = block["start_meas"] + m_offset
                for label in block["labels"]:
                    # Check (idx < n_frames - 1) to reserve the final frame for F0p
                    if idx < n_frames - 1:
                        # Map raw data to the dynamic label index
                        pmt_data[:, :, frame_labels.index(label), meas_idx] = img_cube[:, :, idx]
                        idx += 1

        # Final Frame: F0p
        # Phenovation places F0p at the very end of the binary file
        if n_frames > 0:
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
        ps.pam_time = pmt

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
        ps.gfp = gfp

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
        ps.rfp = rfp

        _debug(visual=ps.rfp,
               filename=os.path.join(params.debug_outdir, f"{str(params.device)}_RFP-frames.png"),
               col='frame_label',
               col_wrap=int(np.ceil(ps.rfp.frame_label.size / 4)))


def _process_aph_data(ps, metadata):
    """Read APH dataset and keep the Red and FarRed frames as a NumPy array.

    Parameters
    ----------
    ps : plantcv.plantcv.classes.PSII_data
        PSII_data instance.
    metadata : dict
        INF file metadata dictionary.
    """
    bin_filepath = _dat_filepath(dataset="APH", datapath=ps.datapath, filename=ps.filename)

    if os.path.exists(bin_filepath):
        # Read the raw data cube (contains Fdark, Red, and FarRed or just Red and FarRed)
        img_cube, _, _ = _read_dat_file(dataset="APH", filename=bin_filepath,
                                        height=int(metadata["ImageRows"]),
                                        width=int(metadata["ImageCols"]))

        # The APH file typically has: index 0 = Fdark, index 1 = Red, index 2 = FarRed.
        # Some acquisitions may only contain two frames (e.g. no dark frame).
        # Select the Red and FarRed frames based on the number of frames present.
        # Use the last 2 frames as Red and FarRed:
        # - When there are 3 frames, indices are [0]=Fdark, [1]=Red, [2]=FarRed -> use indices 1 and 2.
        # - When there are 2 frames, indices are [0]=Red, [1]=FarRed -> use indices 0 and 1.
        num_frames = img_cube.shape[2]
        if num_frames < 2:
            raise RuntimeError(f"APH DAT file contains {num_frames} frame(s); expected at least 2 (Red and FarRed).")
        aph_frames = img_cube[:, :, num_frames - 2:num_frames]

        # Store as a standard attribute
        ps.aph = NamedImageCollection(red=aph_frames[:, :, 0], farred=aph_frames[:, :, 1])

        # Debugging — wrap in a temporary DataArray so frame labels appear in the plot
        aph_debug = xr.DataArray(
            data=aph_frames,
            dims=('x', 'y', 'frame_label'),
            coords={'frame_label': ['Red', 'FarRed']}
        )
        _debug(visual=aph_debug,
               filename=os.path.join(params.debug_outdir, f"{str(params.device)}_APH-frames.png"),
               col='frame_label',
               col_wrap=2)


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
