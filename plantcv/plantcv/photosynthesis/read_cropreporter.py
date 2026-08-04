"""Read in fluorescence images from a .DAT file."""
import os
import numpy as np
import xarray as xr
from plantcv.plantcv import PSII_data
from plantcv.plantcv import Spectral_data
from skimage.util import img_as_ubyte


class APH:
    """Alpha light absorption coefficient (APH) dataset. Stores the file path at init; image data is loaded on first access."""

    def __init__(self, filepath, height, width):
        """Initialize APH dataset with file path and image dimensions."""
        self._filepath = filepath
        self._height = height
        self._width = width
        self._red = None
        self._farred = None

    def __bool__(self):
        """The existence of the APH class is true."""
        return True

    def __repr__(self):
        """String representation of the APH dataset, indicating whether the data has been loaded."""
        loaded = self._red is not None and self._farred is not None
        return f"APH(filepath={self._filepath!r}, loaded={loaded})"

    @property
    def red(self):
        """Return the red frame as a NumPy array."""
        if self._red is None:
            self._load()
        return self._red

    @property
    def farred(self):
        """Return the far-red frame as a NumPy array."""
        if self._farred is None:
            self._load()
        return self._farred

    def _load(self):
        """Load the APH frames from the .DAT file."""
        img_cube, _, _ = _read_dat_file(
            dataset="APH",
            filename=str(self._filepath),
            height=self._height,
            width=self._width,
        )
        # red = second to last frame, far-red = last frame. Fdark frame, if collected, is not stored.
        self._red = img_cube[:, :, -2]
        self._farred = img_cube[:, :, -1]


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


class CLR:
    """Color dataset. Stores the file path at init; image data is loaded on first access."""

    def __init__(self, filepath, height, width):
        """Initialize CLR dataset with file path and image dimensions."""
        self._filepath = filepath
        self._height = height
        self._width = width
        self._color = None

    def __bool__(self):
        """The existence of the CLR class is true."""
        return True

    def __repr__(self):
        """String representation of the CLR dataset, indicating whether the data has been loaded."""
        loaded = self._color is not None
        return f"CLR(filepath={self._filepath!r}, loaded={loaded})"

    @property
    def color(self):
        """Return the color frame as a NumPy array."""
        if self._color is None:
            self._load()
        return self._color

    def _load(self):
        """Load the color frames from the .DAT file."""
        img_cube, _, _ = _read_dat_file(
            dataset="CLR",
            filename=str(self._filepath),
            height=self._height,
            width=self._width,
        )
        # Store the color data as BGR uint8
        self._color = img_as_ubyte(img_cube[:, :, [2, 1, 0]])


class GFP:
    """GFP dataset. Stores the file path at init; image data is loaded on first access."""

    def __init__(self, filepath, height, width, metadata):
        """Initialize GFP dataset with file path and image dimensions."""
        self._filepath = filepath
        self._height = height
        self._width = width
        self._metadata = metadata
        self._green = None
        self._auto = None

    def __bool__(self):
        """The existence of the GFP class is true."""
        return True

    def __repr__(self):
        """String representation of the GFP dataset, indicating whether the data has been loaded."""
        loaded = self._green is not None
        return f"GFP(filepath={self._filepath!r}, loaded={loaded})"

    @property
    def green(self):
        """Return the gfp frame as a NumPy array."""
        if self._green is None:
            self._load()
        return self._green

    @property
    def auto(self):
        """Return the auto frame as a Numpy array."""
        if self._auto is None:
            self._load()
        return self._auto

    def _load(self):
        """Load the gfp frames from the .DAT file."""
        img_cube, _, _ = _read_dat_file(dataset="GFP",
                                        filename=self._filepath,
                                        height=self._height,
                                        width=self._width)
        self._green = img_cube[:, :, -2]
        self._auto = img_cube[:, :, -1]


class RFP:
    """RFP dataset. Stores the file path at init; image data is loaded on first access."""

    def __init__(self, filepath, height, width, metadata):
        """Initialize RFP dataset with file path and image dimensions."""
        self._filepath = filepath
        self._height = height
        self._width = width
        self._metadata = metadata
        self._rfp = None

    def __bool__(self):
        """The existence of the RFP class is true."""
        return True

    def __repr__(self):
        """String representation of the RFP dataset, indicating whether the data has been loaded."""
        loaded = self._rfp is not None
        return f"RFP(filepath={self._filepath!r}, loaded={loaded})"

    @property
    def red(self):
        """Return the rfp frame as a NumPy array."""
        if self._rfp is None:
            self._load()
        return self._rfp

    def _load(self):
        """Load the rfp frames from the .DAT file."""
        img_cube, _, _ = _read_dat_file(dataset="RFP",
                                        filename=self._filepath,
                                        height=self._height,
                                        width=self._width)
        self._rfp = img_cube[:, :, img_cube.shape[2] - 1]


class PSD:
    """OJIP dark-adapted measurements dataset. Stores the file path at init; image data is loaded on first access."""

    def __init__(self, filepath, height, width, metadata):
        """Initialize PSD dataset with file path and image dimensions."""
        self._filepath = filepath
        self._height = height
        self._width = width
        self._metadata = metadata
        self._ojip_dark = None

    def __bool__(self):
        """The existence of the PSD class is true."""
        return True

    def __repr__(self):
        """String representation of the PSD dataset, indicating whether the data has been loaded."""
        loaded = self._ojip_dark is not None
        return f"PSD(filepath={self._filepath!r}, loaded={loaded})"

    @property
    def ojip_dark(self):
        """Return the ojip dark data"""
        if self._ojip_dark is None:
            self._load()
        return self._ojip_dark

    def _load(self):
        """Load the ojip dark frames from the .DAT file."""
        img_cube, frame_labels, frame_nums = _read_dat_file(
            dataset="PSD",
            filename=str(self._filepath),
            height=self._height,
            width=self._width,
        )
        # If not all frames are saved the order is fixed
        # Phenovation does not update the framenumbers in the references.
        # Default frames (when SaveAllFrames == 0)
        f0_frame = 1
        fm_frame = 2
        # F0 and Fm keys
        f0_key = "FvFmFrameF0" if "FvFmFrameF0" in self._metadata else "DkOjipFrameF0"
        fm_key = "FvFmFrameFm" if "FvFmFrameFm" in self._metadata else "DkOjipFrameFm"
        # Get the F0 and Fm frames based on the metadata if all frames are saved
        if f0_key in self._metadata and self._metadata["SaveAllFrames"] != "0":
            f0_frame = int(self._metadata[f0_key]) + 1
            fm_frame = int(self._metadata[fm_key]) + 1
        frame_labels[0] = 'Fdark'
        frame_labels[f0_frame] = 'F0'
        frame_labels[fm_frame] = 'Fm'
        # Replace frame_num with time, skip timepoint 0
        for i in range(len(frame_nums) - 1):
            frame_nums[i + 1] = int(self._metadata.get(f"FvFmTimePoint{i}", frame_nums[i + 1]))

        self._ojip_dark = xr.DataArray(
            data=img_cube[..., None],
            dims=('x', 'y', 'frame_label', 'measurement'),
            coords={'frame_label': frame_labels,
                    'frame_num': ('frame_label', frame_nums),
                    'measurement': ['t0']},
            name='ojip_dark'
        )


class PSL:
    """OJIP light-adapted measurements dataset. Stores the file path at init; image data is loaded on first access."""

    def __init__(self, filepath, height, width, metadata):
        """Initialize PSL dataset with file path and image dimensions."""
        self._filepath = filepath
        self._height = height
        self._width = width
        self._metadata = metadata
        self._ojip_light = None

    def __bool__(self):
        """The existence of the PSL class is true."""
        return True

    def __repr__(self):
        """String representation of the PSL dataset, indicating whether the data has been loaded."""
        loaded = self._ojip_light is not None
        return f"PSL(filepath={self._filepath!r}, loaded={loaded})"

    @property
    def ojip_light(self):
        """Return the ojip light data"""
        if self._ojip_light is None:
            self._load()
        return self._ojip_light

    def _load(self):
        """Load the OJIP light-adapted measurements from the .DAT file."""
        img_cube, frame_labels, frame_nums = _read_dat_file(
            dataset="PSL",
            filename=str(self._filepath),
            height=self._height,
            width=self._width,
        )
        # If not all frames are saved the order is fixed
        # Phenovation does not update the framenumbers in the references.
        # Default frames (when SaveAllFrames == 0)
        fsp_frame = 1
        fmp_frame = 2
        # F' and Fm' keys
        fsp_key = "FqFmFrameFsp" if "FqFmFrameFsp" in self._metadata else "LtOjipFrameFsp"
        fmp_key = "FqFmFrameFmp" if "FqFmFrameFmp" in self._metadata else "LtOjipFrameFmp"
        # Get the F' and Fm' frames based on the metadata if all frames are saved
        if fsp_key in self._metadata and self._metadata["SaveAllFrames"] != "0":
            fsp_frame = int(self._metadata[fsp_key]) + 1
            fmp_frame = int(self._metadata[fmp_key]) + 1
        frame_labels[0] = "Flight"
        frame_labels[fsp_frame] = 'Fp'
        frame_labels[fmp_frame] = 'Fmp'
        # Replace frame_num with time, skip timepoint 0
        for i in range(len(frame_nums) - 1):
            frame_nums[i + 1] = int(self._metadata.get(f"FqFmTimePoint{i}", frame_nums[i + 1]))

        self._ojip_light = xr.DataArray(
            data=img_cube[..., None],
            dims=('x', 'y', 'frame_label', 'measurement'),
            coords={'frame_label': frame_labels,
                    'frame_num': ('frame_label', frame_nums),
                    'measurement': ['t1']},
            name='ojip_light'
        )


class NPQ:
    """NPQ measurements dataset. Stores the file path at init; image data is loaded on first access."""

    def __init__(self, filepath, height, width, metadata):
        """Initialize PSL dataset with file path and image dimensions."""
        self._filepath = filepath
        self._height = height
        self._width = width
        self._metadata = metadata
        self._ojip_light = None
        self._ojip_dark = None

    def __bool__(self):
        """The existence of the PSL class is true."""
        return True

    def __repr__(self):
        """String representation of the NPQ dataset, indicating whether the data has been loaded."""
        loaded = self._ojip_light is not None and self._ojip_dark is not None
        return f"NPQ(filepath={self._filepath!r}, loaded={loaded})"

    @property
    def ojip_light(self):
        """Return the ojip light data"""
        if self._ojip_light is None:
            self._load()
        return self._ojip_light

    @property
    def ojip_dark(self):
        """Return the ojip dark data"""
        if self._ojip_dark is None:
            self._load()
        return self._ojip_dark

    def _load(self):
        """Load Light and Dark data when accessed"""
        img_cube, frame_labels, frame_nums = _read_dat_file(
            dataset="NPQ", filename=self._filepath,
            height=self._height,
            width=self._width
        )
        # Add the OJIP dark frames
        frame_labels[0] = 'Fdark'
        frame_labels[1] = 'F0'
        frame_labels[2] = 'Fm'
        self._ojip_dark = xr.DataArray(
            data=img_cube[:, :, 0:3, None],
            dims=('x', 'y', 'frame_label', 'measurement'),
            coords={'frame_label': frame_labels[0:3],
                    'frame_num': ('frame_label', frame_nums[0:3]),
                    'measurement': ['t0']},
            name='ojip_dark'
        )

        # Add the OJIP light frames
        frame_labels[3] = 'Flight'
        frame_labels[4] = 'Fp'
        frame_labels[5] = 'Fmp'
        self._ojip_light = xr.DataArray(
            data=img_cube[:, :, 3:6, None],
            dims=('x', 'y', 'frame_label', 'measurement'),
            coords={'frame_label': frame_labels[3:6],
                    'frame_num': ('frame_label', frame_nums[3:6]),
                    'measurement': ['t0']},
            name='ojip_light'
        )


class PMD:
    """Class to hold a PMD dataset"""

    def __init__(self, filepath, height, width, metadata):
        """Initialize PMD dataset with file path and image dimensions."""
        self._filepath = filepath
        self._height = height
        self._width = width
        self._metadata = metadata
        self._pam_dark = None

    def __bool__(self):
        """The existence of the PMD class is true."""
        return True

    def __repr__(self):
        """String representation of the PMD dataset, indicating whether the data has been loaded."""
        loaded = self._pam_dark is not None
        return f"PMD(filepath={self._filepath!r}, loaded={loaded})"

    @property
    def pam_dark(self):
        """Return the pam dark data"""
        if self._pam_dark is None:
            self._load()
        return self._pam_dark

    def _load(self):
        """Load the pam dark frames from the .DAT file."""
        img_cube, frame_labels, frame_nums = _read_dat_file(
            dataset="PMD",
            filename=str(self._filepath),
            height=self._height,
            width=self._width,
        )

        frame_labels = ["Fdark", "F0", "Fm", "Fdarksat"]
        self._pam_dark = xr.DataArray(
            data=img_cube[..., None],
            dims=('x', 'y', 'frame_label', 'measurement'),
            coords={'frame_label': frame_labels,
                    'frame_num': ('frame_label', frame_nums),
                    'measurement': ['t0']},
            name='pam_dark'
        )


class PML:
    """Class to hold a PML dataset"""

    def __init__(self, filepath, height, width, metadata):
        """Initialize PML dataset with file path and image dimensions."""
        self._filepath = filepath
        self._height = height
        self._width = width
        self._metadata = metadata
        self._pam_light = None

    def __bool__(self):
        """The existence of the PML class is true."""
        return True

    def __repr__(self):
        """String representation of the PML dataset, indicating whether the data has been loaded."""
        loaded = self._pam_light is not None
        return f"PML(filepath={self._filepath!r}, loaded={loaded})"

    @property
    def pam_light(self):
        """Return the pam light data"""
        if self._pam_light is None:
            self._load()
        return self._pam_light

    def _load(self):
        """Load the pam light frames from the .DAT file."""
        img_cube, frame_labels, frame_nums = _read_dat_file(
            dataset="PML",
            filename=str(self._filepath),
            height=self._height,
            width=self._width,
        )

        frame_labels = ["Fdark", "F0", "Fm", "Fdarksat"]
        self._pam_light = xr.DataArray(
            data=img_cube[..., None],
            dims=('x', 'y', 'frame_label', 'measurement'),
            coords={'frame_label': frame_labels,
                    'frame_num': ('frame_label', frame_nums),
                    'measurement': ['t0']},
            name='pam_light'
        )


class PMT:
    """Class to hold a PMT dataset"""

    def __init__(self, filepath, height, width, metadata):
        """Initialize PMT dataset with file path and image dimensions."""
        self._filepath = filepath
        self._height = height
        self._width = width
        self._metadata = metadata
        self._pam_time = None

    def __bool__(self):
        """The existence of the PML class is true."""
        return True

    def __repr__(self):
        """String representation of the PMT dataset, indicating whether the data has been loaded."""
        loaded = self._pam_time is not None
        return f"PMT(filepath={self._filepath!r}, loaded={loaded})"

    @property
    def pam_time(self):
        """Return the pam time data"""
        if self._pam_time is None:
            self._load()
        return self._pam_time

    def _load(self):
        """Load the pam time frames from the .DAT file."""
        img_cube, _, _ = _read_dat_file(
            dataset="PMT",
            filename=str(self._filepath),
            height=self._height,
            width=self._width
        )

        # metadata-driven measurement counts
        n_fqfm = int(self._metadata.get("TmPamMeasFqfm", 0))
        # TmPamMeasFvfm=1 means only the baseline dark-adapted block exists, so n_fvfm should be 0
        n_fvfm = max(0, int(self._metadata.get("TmPamMeasFvfm", 0)) - 1)

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
        self._pam_time = xr.DataArray(
            data=pmt_data,
            dims=("x", "y", "frame_label", "measurement"),
            coords={
                "frame_label": frame_labels,
                "measurement": measurement_labels
            },
            name="pam_time"
        )


class SPC:
    """Class to hold a SPC dataset"""

    def __init__(self, filepath, height, width, metadata):
        """Initialize SPC dataset with file path and image dimensions."""
        self._filepath = filepath
        self._height = height
        self._width = width
        self._metadata = metadata
        self._spectral = None

    def __bool__(self):
        """The existence of the SPC class is true."""
        return True

    def __repr__(self):
        """String representation of the SPC dataset, indicating whether the data has been loaded."""
        loaded = self._spectral is not None
        return f"SPC(filepath={self._filepath!r}, loaded={loaded})"

    @property
    def spectral(self):
        """Return the spectral data"""
        if self._spectral is None:
            self._load()
        return self._spectral

    def _load(self):
        """Load the spectral data from the .DAT file."""
        img_cubes = []
        wavelengths = []
        datapath = os.path.dirname(self._metadata["filename"])
        filename = os.path.split(self._metadata["filename"])[-1]
        clr_filepath = _dat_filepath(dataset="CLR", datapath=datapath, filename=filename)
        spc_filepath = _dat_filepath(dataset="SPC", datapath=datapath, filename=filename)
        rgb = None
        if os.path.exists(clr_filepath):
            rgb_cube, _, _ = _read_dat_file(dataset="CLR", filename=clr_filepath,
                                            height=self._height,
                                            width=self._width)
            img_cubes.append(rgb_cube)
            wavelengths += [640, 550, 475]
            rgb = img_as_ubyte(rgb_cube[:, :, [2, 1, 0]])
        if os.path.exists(spc_filepath):
            spc_cube, _, _ = _read_dat_file(dataset="SPC", filename=spc_filepath,
                                            height=self._height,
                                            width=self._width)
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
            self._spectral = multispec


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
    metadata_dict["filename"] = filename
    ps.filename = os.path.split(filename)[-1]
    ps.datapath = os.path.dirname(filename)

    # Image dimensions (assumed to be consistent across all datasets for a given acquisition)
    height = int(ps.metadata["ImageRows"])
    width = int(ps.metadata["ImageCols"])

    # Dataset-specific processing functions. Class constructors for lazy loading.
    dataset_classes = {
        # Alpha light absorption coefficient (APH) data
        "APH": lambda fp: APH(filepath=fp, height=height, width=width),
        # Chlorophyll fluorescence data
        "CHL": lambda fp: CHL(filepath=fp, height=height, width=width),
        # Color data
        "CLR": lambda fp: CLR(filepath=fp, height=height, width=width),
        # OJIP dark data
        "PSD": lambda fp: PSD(filepath=fp, height=height, width=width, metadata=ps.metadata),
        # OJIP light data
        "PSL": lambda fp: PSL(filepath=fp, height=height, width=width, metadata=ps.metadata),
        # NPQ data
        "NPQ": lambda fp: NPQ(filepath=fp, height=height, width=width, metadata=ps.metadata),
        # PMD data
        "PMD": lambda fp: PMD(filepath=fp, height=height, width=width, metadata=ps.metadata),
        # PML data
        "PML": lambda fp: PML(filepath=fp, height=height, width=width, metadata=ps.metadata),
        # PMT data
        "PMT": lambda fp: PMT(filepath=fp, height=height, width=width, metadata=ps.metadata),
        # GFP data
        "GFP": lambda fp: GFP(filepath=fp, height=height, width=width, metadata=ps.metadata),
        # RFP data
        "RFP": lambda fp: RFP(filepath=fp, height=height, width=width, metadata=ps.metadata),
        # SPC data
        "SPC": lambda fp: SPC(filepath=fp, height=height, width=width, metadata=ps.metadata)
    }

    # Process datasets
    for dataset in ["APH", "CHL", "CLR", "PMD", "PML", "PMT", "PSD", "PSL", "SPC", "NPQ", "GFP", "RFP"]:
        # Construct the expected binary file path for the dataset
        bin_filepath = _dat_filepath(dataset=dataset, datapath=ps.datapath, filename=ps.filename)
        # Check if the file exists
        if os.path.exists(bin_filepath):
            key = dataset.lower()
            # Get the class constructor
            constructor = dataset_classes.get(dataset)
            if constructor is not None:
                setattr(ps, key, constructor(bin_filepath))
            if dataset in ["PSL", "NPQ"]:
                setattr(ps, "ojip_light", key)
            if dataset in ["PSD", "NPQ"]:
                setattr(ps, "ojip_dark", key)

    return ps


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
