# PlantCV classes
import copy
import functools
import cv2
import numpy as np
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv._helpers import _find_closest, _rescale
from plantcv.plantcv.annotate.points import _find_closest_pt
import matplotlib.pyplot as plt
from math import floor


class Spectral_data:
    """PlantCV Hyperspectral data class"""

    def __init__(self, array_data, max_wavelength, min_wavelength, max_value, min_value, d_type, wavelength_dict,
                 samples, lines, interleave, wavelength_units, array_type, filename, default_bands,
                 byte_order=0, file_type="ENVI", header_offset=0, metadata=None):
        # The actual array/datacube
        self.array_data = array_data
        # Min/max available wavelengths (for spectral datacube)
        self.max_wavelength = max_wavelength
        self.min_wavelength = min_wavelength
        #  Min/max pixel value for single wavelength or index
        self.max_value = max_value
        self.min_value = min_value
        # Numpy data type
        self.d_type = d_type
        # Contains all available wavelengths where keys are wavelength and value are indices
        self.wavelength_dict = wavelength_dict
        # Resolution of a single band of spectral data is (samples, lines) rather than (x,y) with other arrays
        self.samples = samples
        self.lines = lines
        # Interleave type
        self.interleave = interleave
        self.wavelength_units = wavelength_units
        # store byte order, file type, and header offset
        self.byte_order = byte_order
        self.file_type = file_type
        self.header_offset = header_offset
        # The type of array data (entire datacube, specific index, first derivative, etc)
        self.array_type = array_type
        # The filename where the data originated from
        self.filename = filename
        # The default band indices needed to make an pseudo_rgb image, if not available then store None
        self.default_bands = default_bands
        # Metadata, flexible components in a dictionary
        self.metadata = metadata
        if not metadata:
            self.metadata = {}

    def pseudo_rgb(self):
        """Make a pseudo rgb"""
        # Make shorter variable names for data from the spectral class instance object
        array_data = self.array_data
        default_bands = self.default_bands
        wl_keys = self.wavelength_dict.keys()

        if len(wl_keys) <= 1:
            pseudo_rgb = array_data
            if len(np.shape(pseudo_rgb)) > 2:
                # the shape for these is [wavelengths, X, Y]
                pseudo_rgb = array_data[0, :, :]
            return np.repeat(_rescale(pseudo_rgb ** (1 / 2.2))[..., np.newaxis], 3, axis=-1)

        if default_bands is not None:
            pseudo_rgb = _make_default_bands_pseudo_rgb(self)
        else:
            pseudo_rgb = _make_no_default_bands_pseudo_rgb(self)
        # Gamma correct pseudo_rgb image
        pseudo_rgb = pseudo_rgb ** (1 / 2.2)
        # Scale each of the channels up to 255
        pseudo_rgb = cv2.merge((_rescale(pseudo_rgb[:, :, 0]),
                                _rescale(pseudo_rgb[:, :, 1]),
                                _rescale(pseudo_rgb[:, :, 2])))

        return pseudo_rgb


def _make_default_bands_pseudo_rgb(spectral_data):
    """Helper to reduce complexity in Spectral_data.pseudo_rgb

    Parameters:
    -----------
    spectral_data : plantcv.plantcv.Spectral_data,
        the data to make a pseudo rgb image of

    Returns:
    --------
    pseudo_rgb : numpy.ndarray
    """
    default_bands = spectral_data.default_bands
    array_data = spectral_data.array_data
    # The ENVI standard defines one default band for a grayscale image and three for an RGB image
    if len(default_bands) == 1:
        # Repeat the single band in each channel to make a grayscale pseudo-rgb image
        default_bands = default_bands * 3
    if len(default_bands) != 3:
        fatal_error(
            f"Expected 1 or 3 default bands in the header file but found {len(default_bands)}. " +
            "Consider removing default_bands field of the header file."
        )
    # Default bands are positions on the band axis of the datacube, so they have to be in range
    bands = [int(band) for band in default_bands]
    if not all(0 <= band < array_data.shape[2] for band in bands):
        fatal_error(f"Default bands {bands} are not all valid band numbers for a datacube with "
                    f"{array_data.shape[2]} bands.")
    pseudo_rgb = cv2.merge((array_data[:, :, bands[0]],
                            array_data[:, :, bands[1]],
                            array_data[:, :, bands[2]]))
    return pseudo_rgb


def _make_no_default_bands_pseudo_rgb(spectral_data):
    """Helper to reduce complexity in Spectral_data.pseudo_rgb

    Parameters:
    -----------
    spectral_data : plantcv.plantcv.Spectral_data,
        the data to make a pseudo rgb image of

    Returns:
    --------
    pseudo_rgb : numpy.ndarray
    """
    array_data = spectral_data.array_data
    wl_keys = spectral_data.wavelength_dict.keys()
    max_wavelength = max(float(i) for i in wl_keys)
    min_wavelength = min(float(i) for i in wl_keys)
    # Check range of available wavelength
    if max_wavelength >= 600 and min_wavelength <= 490:
        id_red = _find_closest(spectral_array=np.array([float(i) for i in wl_keys]), target=630)
        id_green = _find_closest(spectral_array=np.array([float(i) for i in wl_keys]), target=540)
        id_blue = _find_closest(spectral_array=np.array([float(i) for i in wl_keys]), target=480)

        pseudo_rgb = cv2.merge((array_data[:, :, [id_blue]],
                                array_data[:, :, [id_green]],
                                array_data[:, :, [id_red]]))
    else:
        # Otherwise take 3 wavelengths, first, middle and last available wavelength
        id_red = int(len(spectral_data.wavelength_dict)) - 1
        id_green = int(id_red / 2)
        pseudo_rgb = cv2.merge((array_data[:, :, [0]],
                                array_data[:, :, [id_green]],
                                array_data[:, :, [id_red]]))
    return pseudo_rgb


class PSII_data:
    """PSII data class"""

    def __init__(self, metadata: dict = None):
        self.metadata = metadata
        if self.metadata is None:
            self.metadata = {}
            self.datapath = None
            self.filename = None
            # Dataset attributes: None = file not present, lazy-loaded object = file present
        self.aph = None
        self.chl = None
        self.clr = None
        self.npq = None
        self._ojip_dark = None
        self._ojip_light = None
        self.psd = None
        self.psl = None
        self.pmd = None
        self.pml = None
        self.pmt = None
        self.spectral = None
        self.gfp = None
        self.rfp = None

    @property
    def ojip_dark(self):
        if isinstance(self._ojip_dark, str):
            self._ojip_dark = getattr(self.__dict__[self._ojip_dark], "ojip_dark", None)
        return self._ojip_dark

    @ojip_dark.setter
    def ojip_dark(self, value):
        self._ojip_dark = value

    @property
    def ojip_light(self):
        if isinstance(self._ojip_light, str):
            self._ojip_light = getattr(self.__dict__[self._ojip_light], "ojip_light", None)
        return self._ojip_light

    @ojip_light.setter
    def ojip_light(self, value):
        self._ojip_light = value


class Point:
    """Point annotation/collection class to use in Jupyter notebooks. It allows the user to
    interactively click to collect coordinates from an image. Left click collects the point and
    right click removes the closest collected point
    """

    def __init__(self, img, figsize=(12, 6)):
        """
        Initialization
        :param img: image data
        :param figsize: desired figure size, (12,6) by default
        :attribute points: list of points as (x,y) coordinates tuples
        """
        self.fig, self.ax = plt.subplots(1, 1, figsize=figsize)
        self.ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        self.points = []
        self.events = []

        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):
        """Handle mouse click events"""
        self.events.append(event)
        if event.button == 1:

            self.ax.plot(event.xdata, event.ydata, 'x', c='red')
            self.points.append((floor(event.xdata), floor(event.ydata)))

        else:
            idx_remove, _ = _find_closest_pt((event.xdata, event.ydata), self.points)
            # remove the closest point to the user right clicked one
            self.points.pop(idx_remove)
            self.ax.lines[idx_remove].remove()
        self.fig.canvas.draw()


class Objects:
    """Class for managing image contours/objects and their hierarchical relationships."""

    def __init__(self, contours: list = None, hierarchy: list = None):
        self.contours = contours
        self.hierarchy = hierarchy
        self._n = 0
        if contours is None:
            self.contours = []
            self.hierarchy = []

    def __iter__(self):
        self._n = 0
        return self

    def __next__(self):
        if self._n < len(self.contours):
            self._n += 1
            return Objects(contours=[self.contours[self._n-1]], hierarchy=[self.hierarchy[self._n-1]])
        raise StopIteration

    def append(self, contour, h):
        """Append a contour and its hierarchy to the object"""
        self.contours.append(contour)
        self.hierarchy.append(h)

    def save(self, filename):
        """Save the object to a file"""
        np.savez(filename, contours=self.contours, hierarchy=self.hierarchy)

    @staticmethod
    def load(filename):
        """Load a saved object file"""
        file = np.load(filename)
        obj = Objects(file['contours'].tolist(), file['hierarchy'])
        return obj


class MS_data:
    """PlantCV Multispectral data class"""

    def __init__(self,
                 array_data,
                 wavelength_dict,
                 max_wavelength,
                 min_wavelength,
                 filename,
                 metadata=None):
        # The actual array/datacube
        self.array_data = array_data
        # Contains all available wavelengths where keys are wavelength and value are indices
        self.wavelength_dict = wavelength_dict
        # store max/min wavelengths
        self.max_wavelength = max_wavelength
        self.min_wavelength = min_wavelength
        # The filename where the data originated from
        self.filename = filename
        # default wavelengths for making pseudo rgb
        self.default_bands = None
        # Metadata, flexible components in a dictionary
        self.metadata = metadata

    def pseudo_rgb(self):
        """Make pseudo rgb image on the fly"""
        array_data = self.array_data
        waves = list(self.wavelength_dict)

        max_wavelength = float(self.max_wavelength)
        min_wavelength = float(self.min_wavelength)
        # Check range of available wavelength
        if max_wavelength >= 600 and min_wavelength <= 490:
            id_red = _find_closest(spectral_array=np.array([float(i) for i in waves]), target=630)
            id_green = _find_closest(spectral_array=np.array([float(i) for i in waves]), target=540)
            id_blue = _find_closest(spectral_array=np.array([float(i) for i in waves]), target=480)

            pseudo_rgb = cv2.merge((array_data[:, :, [id_blue]],
                                    array_data[:, :, [id_green]],
                                    array_data[:, :, [id_red]]))
        else:
            # Otherwise take 3 wavelengths, first, middle and last available wavelength
            id_red = int(len(waves)) - 1
            id_green = int(id_red / 2)
            pseudo_rgb = cv2.merge((array_data[:, :, [0]],
                                    array_data[:, :, [id_green]],
                                    array_data[:, :, [id_red]]))

        # Gamma correct pseudo_rgb image
        pseudo_rgb = pseudo_rgb ** (1 / 2.2)
        # Scale each of the channels up to 255
        pseudo_rgb = cv2.merge((_rescale(pseudo_rgb[:, :, 0]),
                                _rescale(pseudo_rgb[:, :, 1]),
                                _rescale(pseudo_rgb[:, :, 2])))
        return pseudo_rgb

    def select(self, wavelength, ms=True):
        """Select a wavelength"""
        if not isinstance(wavelength, list):
            wavelength = [wavelength]
        wavelength_dict_new = {}
        for v, k in enumerate(wavelength):
            wavelength_dict_new[k] = v
        index = [self.wavelength_dict[wave] for wave in wavelength]
        sub_array = self.array_data[:, :, index]
        if not ms:
            return sub_array
        sub_ms = MS_data(
            array_data=sub_array,
            wavelength_dict=wavelength_dict_new,
            max_wavelength=max(wavelength),
            min_wavelength=min(wavelength),
            filename=self.filename,
            metadata=self.metadata
        )
        return sub_ms


def _to_plain(obj):
    """Convert Image objects, including those inside tuples and lists, to plain numpy arrays.

    Parameters
    ----------
    obj : object
        Any object returned by a NumPy function.

    Returns
    -------
    object
        The same object with every Image replaced by a numpy.ndarray view of its data.
    """
    if isinstance(obj, Image):
        return obj.view(np.ndarray)
    if isinstance(obj, list):
        return [_to_plain(item) for item in obj]
    if isinstance(obj, tuple):
        items = [_to_plain(item) for item in obj]
        # Named tuples (e.g. results of np.linalg.svd) are rebuilt with their own type
        if hasattr(obj, "_fields"):
            return type(obj)(*items)
        return tuple(items)
    return obj


def _plain_method(name):
    """Wrap a numpy.ndarray method so that it operates on, and returns, plain numpy arrays.

    Parameters
    ----------
    name : str
        Name of the numpy.ndarray method to wrap.

    Returns
    -------
    function
        Method that calls the numpy.ndarray method on a plain view of the data.
    """
    base = getattr(np.ndarray, name)

    @functools.wraps(base)
    def method(self, *args, **kwargs):
        return base(self.view(np.ndarray), *args, **kwargs)
    return method


class Image(np.ndarray):
    """Abstract base class for PlantCV images.

    Image extends numpy.ndarray with metadata, starting with the uniform resource identifier (uri) of the
    source file. Image itself cannot be constructed; use one of the image kinds Color, Gray, Mask,
    LabeledMask, or Spectral.

    Only PlantCV code assigns an image kind. NumPy operations whose effect on the meaning of the
    channels is not guaranteed return a plain numpy.ndarray:

    - Ufuncs, comparisons, and reductions (e.g. ``img + 1``, ``img > 100``, ``np.mean(img, axis=2)``).
      In-place operations with ``out`` (e.g. ``img += 1``) keep the original object.
    - NumPy functions such as ``np.dstack``, ``np.concatenate``, ``np.where``, ``np.flip``, and ``np.copy``.
    - Indexing, unless the key is a slice or a tuple of at most two slices and the result keeps the same
      number of dimensions (spatial crops, flips, and strides keep the image kind).
    - Shape-changing and index-returning methods (``reshape``, ``transpose``, ``T``, ``argmax``,
      ``take``, ``flat``, etc.) and ``view`` with a dtype.

    ``copy()`` and ``astype()`` keep the image kind and metadata. ``copy()`` shares mutable metadata
    (e.g. dictionaries) with the original, while ``copy.deepcopy`` copies it.

    Viewing a plain array as an image kind (e.g. ``arr.view(Color)``) bypasses validation and leaves the
    metadata set to None.

    Attributes
    ----------
    uri : str or None
        Uniform resource identifier of the source file.
    """

    # Names of the metadata attributes carried by each image kind
    _meta = ("uri",)

    # numpy.ndarray methods that bypass __array_ufunc__ and __array_function__ and would otherwise
    # return an Image whose shape, values, or channel meaning may have changed
    _PLAIN_METHODS = ("reshape", "transpose", "swapaxes", "ravel", "flatten", "squeeze", "argmax", "argmin",
                      "argsort", "argpartition", "take", "repeat", "diagonal", "compress", "choose", "dot",
                      "byteswap", "getfield")

    def __new__(cls, input_array, uri=None):
        """Create a new Image instance.

        Parameters
        ----------
        input_array : numpy.ndarray
            Image data.
        uri : str, optional
            Uniform resource identifier of the source file.

        Returns
        -------
        Image
            Never returned; Image is abstract.

        Raises
        ------
        TypeError
            Always, because Image is abstract.
        """
        return cls._create(input_array, uri)

    @classmethod
    def _create(cls, input_array, uri=None, **meta):
        """Create, populate, and validate an instance of an image kind.

        Parameters
        ----------
        input_array : numpy.ndarray
            Image data.
        uri : str, optional
            Uniform resource identifier of the source file.
        **meta
            Additional metadata attributes of the image kind.

        Returns
        -------
        Image
            A validated instance of cls.

        Raises
        ------
        TypeError
            If cls is the abstract Image class.
        """
        if cls is Image:
            raise TypeError("Image is abstract; use Color, Gray, Mask, LabeledMask, or Spectral.")
        obj = np.asarray(input_array).view(cls)
        obj.uri = uri
        for name, value in meta.items():
            setattr(obj, name, value)
        obj._validate()
        return obj

    def __array_finalize__(self, obj):
        """Copy metadata from the source object to a new view or copy.

        Parameters
        ----------
        obj : numpy.ndarray or None
            The object the new array was created from.
        """
        for name in self._meta:
            setattr(self, name, getattr(obj, name, None))

    def __reduce__(self):
        """Support pickling, including the metadata attributes.

        Returns
        -------
        tuple
            numpy.ndarray reduce tuple with a dictionary of metadata appended to the state.
        """
        reconstruct, args, state = super().__reduce__()
        meta = {name: getattr(self, name, None) for name in self._meta}
        return reconstruct, args, state + (meta,)

    def __setstate__(self, state):
        """Restore the array data and metadata attributes when unpickling.

        Parameters
        ----------
        state : tuple
            numpy.ndarray state with a dictionary of metadata appended.
        """
        super().__setstate__(state[:-1])
        for name, value in state[-1].items():
            setattr(self, name, value)

    def __deepcopy__(self, memo):
        """Deep copy the array data and metadata attributes.

        Parameters
        ----------
        memo : dict
            Deep copy memo dictionary.

        Returns
        -------
        Image
            Independent copy of the image and its metadata.
        """
        new = super().__deepcopy__(memo)
        for name in self._meta:
            setattr(new, name, copy.deepcopy(getattr(self, name, None), memo))
        return new

    def __array_ufunc__(self, ufunc, method, *inputs, out=None, **kwargs):
        """Run ufuncs on plain arrays and return plain results.

        Parameters
        ----------
        ufunc : numpy.ufunc
            The ufunc being called.
        method : str
            The ufunc method being called (e.g. "__call__" or "reduce").
        *inputs
            Ufunc inputs.
        out : tuple, optional
            Output arrays.
        **kwargs
            Additional ufunc keyword arguments.

        Returns
        -------
        numpy.ndarray or object
            The plain ufunc result, or the original output object(s) if out was given.
        """
        args = tuple(i.view(np.ndarray) if isinstance(i, Image) else i for i in inputs)
        if out is not None:
            kwargs["out"] = tuple(o.view(np.ndarray) if isinstance(o, Image) else o for o in out)
        result = getattr(ufunc, method)(*args, **kwargs)
        if out is None:
            return result
        return out[0] if len(out) == 1 else out

    def __array_function__(self, func, types, args, kwargs):
        """Run NumPy functions and return plain results.

        Parameters
        ----------
        func : function
            The NumPy function being called.
        types : collection
            Types of the arguments that implement __array_function__.
        args : tuple
            Positional arguments.
        kwargs : dict
            Keyword arguments.

        Returns
        -------
        object
            The function result with every Image converted to numpy.ndarray.
        """
        return _to_plain(super().__array_function__(func, types, args, kwargs))

    def __getitem__(self, key):
        """Index the image, keeping the image kind only for spatial slicing.

        Parameters
        ----------
        key : object
            Index key.

        Returns
        -------
        Image, numpy.ndarray, or scalar
            An image of the same kind for spatial crops, flips, and strides; otherwise a plain
            numpy.ndarray, or a scalar for single-element indexing.
        """
        result = super().__getitem__(key)
        if not isinstance(result, np.ndarray):
            return result
        spatial = isinstance(key, slice) or (
            isinstance(key, tuple) and len(key) <= 2 and all(isinstance(k, slice) for k in key))
        if spatial and result.ndim == self.ndim:
            return result
        return result.view(np.ndarray)

    def view(self, *args, **kwargs):
        """Return a new view of the image data.

        A view with a new dtype returns a plain numpy.ndarray, because reinterpreting the bytes can change
        the number and meaning of the channels.

        Parameters
        ----------
        *args
            Positional arguments passed to numpy.ndarray.view (dtype and/or type).
        **kwargs
            Keyword arguments passed to numpy.ndarray.view (dtype and/or type).

        Returns
        -------
        numpy.ndarray
            View of the data.
        """
        result = super().view(*args, **kwargs)
        dtype = kwargs.get("dtype")
        if args and not (isinstance(args[0], type) and issubclass(args[0], np.ndarray)):
            dtype = args[0]
        if dtype is not None and isinstance(result, Image):
            return result.view(np.ndarray)
        return result

    @property
    def T(self):
        """Transposed data as a plain numpy.ndarray.

        Returns
        -------
        numpy.ndarray
            Transposed array.
        """
        return self.view(np.ndarray).T

    @property
    def flat(self):
        """Flat iterator over the data as a plain numpy.ndarray.

        Returns
        -------
        numpy.flatiter
            Flat iterator over a plain view of the data.
        """
        return self.view(np.ndarray).flat

    @flat.setter
    def flat(self, value):
        """Assign values through the flat iterator.

        Parameters
        ----------
        value : array-like
            Values to assign.
        """
        self.view(np.ndarray).flat = value


for _name in Image._PLAIN_METHODS:
    setattr(Image, _name, _plain_method(_name))


class Color(Image):
    """Multichannel color image with recorded channel order.

    Channel order cannot be inferred from pixel values, so it is required. RGB, BGR, HSV, LAB, etc.
    are all Color images with different channel labels.

    Parameters
    ----------
    input_array : numpy.ndarray
        Image data with shape (height, width, channels).
    uri : str, optional
        Uniform resource identifier of the source file.
    channels : sequence of str
        Unique channel labels in the order of the last axis, e.g. ("B", "G", "R").

    Attributes
    ----------
    uri : str or None
        Uniform resource identifier of the source file.
    channels : tuple of str
        Channel labels in the order of the last axis.

    Raises
    ------
    ValueError
        If channels is missing, the data are not 3-dimensional, the labels are not unique strings, or
        the number of labels does not match the number of channels.
    """

    _meta = Image._meta + ("channels",)

    def __new__(cls, input_array, uri=None, channels=None):
        """Create a new Color image."""
        return cls._create(input_array, uri, channels=None if channels is None else tuple(channels))

    def _validate(self):
        """Validate the image data and channel labels."""
        if self.channels is None:
            raise ValueError("Color images require channel labels, e.g. channels=('B', 'G', 'R').")
        if self.ndim != 3:
            raise ValueError(f"Color images must be 3-dimensional, got {self.ndim} dimensions.")
        if not all(isinstance(c, str) for c in self.channels) or len(set(self.channels)) != len(self.channels):
            raise ValueError(f"Channel labels must be unique strings, got {self.channels}.")
        if len(self.channels) != self.shape[-1]:
            raise ValueError(f"{len(self.channels)} channel labels were given for {self.shape[-1]} channels.")

    def channel(self, label):
        """Extract a single channel as a grayscale image.

        Parameters
        ----------
        label : str
            Label of the channel to extract.

        Returns
        -------
        Gray
            The channel, with the same uri and channel set to label.

        Raises
        ------
        ValueError
            If label is not one of the channel labels.
        """
        if label not in self.channels:
            raise ValueError(f"Channel {label!r} not found; available channels are {self.channels}.")
        idx = self.channels.index(label)
        return Gray(np.asarray(self)[:, :, idx], uri=self.uri, channel=label)

    def reorder(self, order):
        """Reorder the channels.

        Parameters
        ----------
        order : sequence of str
            New channel order; a permutation of the current channel labels.

        Returns
        -------
        Color
            New image with the data permuted and channels set to order.

        Raises
        ------
        ValueError
            If order is not a permutation of the current channel labels.
        """
        order = tuple(order)
        if sorted(order) != sorted(self.channels):
            raise ValueError(f"{order} is not a permutation of the channels {self.channels}.")
        idx = [self.channels.index(label) for label in order]
        return Color(np.asarray(self)[:, :, idx], uri=self.uri, channels=order)


class Gray(Image):
    """Single-channel grayscale image.

    Parameters
    ----------
    input_array : numpy.ndarray
        Image data with shape (height, width).
    uri : str, optional
        Uniform resource identifier of the source file.
    channel : str or float, optional
        Source of the channel, e.g. a color channel label or a wavelength.

    Attributes
    ----------
    uri : str or None
        Uniform resource identifier of the source file.
    channel : str, float, or None
        Source of the channel.

    Raises
    ------
    ValueError
        If the data are not 2-dimensional.
    """

    _meta = Image._meta + ("channel",)

    def __new__(cls, input_array, uri=None, channel=None):
        """Create a new Gray image."""
        return cls._create(input_array, uri, channel=channel)

    def _validate(self):
        """Validate the image data."""
        if self.ndim != 2:
            raise ValueError(f"Gray images must be 2-dimensional, got {self.ndim} dimensions.")


class Mask(Image):
    """Binary mask stored as uint8 with values 0 and 255.

    Parameters
    ----------
    input_array : numpy.ndarray
        Mask data with shape (height, width): bool, or uint8 with values only 0 and 255.
        Boolean input is converted to uint8 0/255.
    uri : str, optional
        Uniform resource identifier of the source file.

    Attributes
    ----------
    uri : str or None
        Uniform resource identifier of the source file.

    Raises
    ------
    ValueError
        If the data are not 2-dimensional, not bool or uint8, or contain values other than 0 and 255.
    """

    def __new__(cls, input_array, uri=None):
        """Create a new Mask."""
        arr = np.asarray(input_array)
        if arr.dtype == bool:
            arr = arr.astype(np.uint8) * 255
        return cls._create(arr, uri)

    def _validate(self):
        """Validate the mask data."""
        if self.ndim != 2:
            raise ValueError(f"Masks must be 2-dimensional, got {self.ndim} dimensions.")
        if self.dtype != np.uint8:
            raise ValueError(f"Masks must be bool or uint8, got {self.dtype}.")
        # The value check scans every pixel (O(n))
        arr = np.asarray(self)
        if not np.all((arr == 0) | (arr == 255)):
            raise ValueError("uint8 masks must contain only the values 0 and 255.")


class LabeledMask(Image):
    """Integer label image, where each object has a unique integer value.

    Parameters
    ----------
    input_array : numpy.ndarray
        Label data with shape (height, width) and an integer dtype.
    uri : str, optional
        Uniform resource identifier of the source file.

    Attributes
    ----------
    uri : str or None
        Uniform resource identifier of the source file.

    Raises
    ------
    ValueError
        If the data are not 2-dimensional or not an integer dtype.
    """

    def __new__(cls, input_array, uri=None):
        """Create a new LabeledMask."""
        return cls._create(input_array, uri)

    def _validate(self):
        """Validate the label data."""
        if self.ndim != 2:
            raise ValueError(f"Labeled masks must be 2-dimensional, got {self.ndim} dimensions.")
        if not np.issubdtype(self.dtype, np.integer):
            raise ValueError(f"Labeled masks must have an integer dtype, got {self.dtype}.")


class Spectral(Image):
    """Multispectral or hyperspectral image, with wavelengths as the channel labels.

    Parameters
    ----------
    input_array : numpy.ndarray
        Image data with shape (height, width, bands).
    uri : str, optional
        Uniform resource identifier of the source file.
    wavelengths : sequence of float
        Wavelength of each band, in the order of the last axis.
    default_wavelengths : sequence of float, optional
        Wavelengths used to make thumbnails. Three wavelengths are used in blue, green, red order; any
        other number produces a grayscale thumbnail from the first. If None, [480, 540, 710] is used when
        the wavelengths cover 490 to 635, otherwise the brightest band. The brightest band is computed on
        first access because it requires summing the whole data cube.
    wavelength_units : str, optional
        Units of the wavelengths (default "nm").
    metadata : dict, optional
        Additional metadata from the source file.

    Attributes
    ----------
    uri : str or None
        Uniform resource identifier of the source file.
    wavelengths : list of float
        Wavelength of each band.
    wavelength_units : str
        Units of the wavelengths.
    metadata : dict
        Additional metadata from the source file.

    Raises
    ------
    ValueError
        If wavelengths is missing, the data are not 3-dimensional, or the number of wavelengths does not
        match the number of bands.
    """

    _meta = Image._meta + ("wavelengths", "wavelength_units", "_default_wavelengths", "metadata")

    def __new__(cls, input_array, uri=None, wavelengths=None, default_wavelengths=None, wavelength_units="nm",
                metadata=None):
        """Create a new Spectral image."""
        return cls._create(input_array, uri,
                           wavelengths=None if wavelengths is None else list(wavelengths),
                           _default_wavelengths=None if default_wavelengths is None else list(default_wavelengths),
                           wavelength_units=wavelength_units,
                           metadata={} if metadata is None else metadata)

    def _validate(self):
        """Validate the image data and wavelengths."""
        if self.wavelengths is None:
            raise ValueError("Spectral images require wavelengths.")
        if self.ndim != 3:
            raise ValueError(f"Spectral images must be 3-dimensional, got {self.ndim} dimensions.")
        if len(self.wavelengths) != self.shape[-1]:
            raise ValueError(f"{len(self.wavelengths)} wavelengths were given for {self.shape[-1]} bands.")

    @property
    def min_wavelength(self):
        """Shortest wavelength.

        Returns
        -------
        float
            Minimum of wavelengths.
        """
        return min(self.wavelengths)

    @property
    def max_wavelength(self):
        """Longest wavelength.

        Returns
        -------
        float
            Maximum of wavelengths.
        """
        return max(self.wavelengths)

    @property
    def default_wavelengths(self):
        """Wavelengths used to make thumbnails.

        Returns
        -------
        list of float
            The given default wavelengths; otherwise [480, 540, 710] when the wavelengths cover 490 to 635,
            or else the wavelength of the brightest band (computed on first access).
        """
        if self._default_wavelengths is None:
            if self.min_wavelength <= 490 and self.max_wavelength >= 635:
                self._default_wavelengths = [480, 540, 710]
            else:
                band_sums = np.sum(np.asarray(self), axis=(0, 1))
                self._default_wavelengths = [self.wavelengths[int(np.argmax(band_sums))]]
        return self._default_wavelengths

    @default_wavelengths.setter
    def default_wavelengths(self, value):
        """Set the wavelengths used to make thumbnails.

        Parameters
        ----------
        value : sequence of float or None
            Default wavelengths, or None to use the automatic choice.
        """
        self._default_wavelengths = None if value is None else list(value)

    def get_wavelength(self, wavelength):
        """Extract the band nearest to a wavelength.

        Parameters
        ----------
        wavelength : float
            Requested wavelength.

        Returns
        -------
        Gray
            The nearest band, with the same uri and channel set to that band's wavelength.
        """
        idx = int(np.argmin(np.abs(np.asarray(self.wavelengths, dtype=float) - wavelength)))
        return Gray(np.asarray(self)[:, :, idx], uri=self.uri, channel=self.wavelengths[idx])

    def thumbnail(self):
        """Create a color or grayscale thumbnail for quick visualization.

        Returns
        -------
        Color or Gray
            A Color image with channels ("B", "G", "R") built from the bands nearest to the three default
            wavelengths, or a Gray image of the band nearest to the first default wavelength otherwise.
        """
        defaults = self.default_wavelengths
        if len(defaults) == 3:
            bands = [self.get_wavelength(wl) for wl in defaults]
            return Color(np.dstack(bands), uri=self.uri, channels=("B", "G", "R"))
        return self.get_wavelength(defaults[0])
