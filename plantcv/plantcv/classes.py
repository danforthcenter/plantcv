# PlantCV classes
import os
import re
import cv2
import json
import datetime
import numpy as np
from importlib.metadata import version
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv._helpers import _find_closest, _rescale
from plantcv.plantcv.annotate.points import _find_closest_pt
from plantcv.plantcv.coco.coco_from_mask import _coco_object_annotation_from_mask, _next_id
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


class COCO:
    """PlantCV COCO data class"""

    def __init__(self, source=None, **kwargs):
        # Define which keys are for each coco field
        info_fields = ["description", "version", "year", "contributor", "date_created",
                       "datetime", "date", "time"]
        license_fields = ["id", "name", "url"]
        image_anno_fields = ["image_id", "file_name", "filename", "date_captured",
                             "license", "iscrowd", "category_id", "shape"]
        kwargs = {k.lower(): v for k, v in kwargs.items()}

        info_kwargs = {k.lower(): v for k, v in kwargs.items() if k in info_fields}
        info_kwargs["plantcv_version"] = version("plantcv")
        run_datetime = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        info_kwargs["plantcv_run_date"] = run_datetime
        license_kwargs = {k.lower(): v for k, v in kwargs.items() if k in license_fields}

        licenses = []
        if license_kwargs:
            licenses = [license_kwargs]

        self._info = info_kwargs
        self._licenses = licenses
        self._images = []
        self._annotations = []
        self._categories = []

        if source is not None:
            image_kwargs = {k: v for k, v in kwargs.items() if k in image_anno_fields}
            self.add_record(source=source, info=None, rights=None,
                            category={"id": kwargs.get("category_id", 1), "name": "plant"},
                            **image_kwargs)
            
    @staticmethod
    def _standardize_source(source, **kwargs):
        """Standardize sources to different annotation types' inputs"""
        if isinstance(source, (np.ndarray, Objects)):
            shape = kwargs.get("shape")
            standardized_source = COCO._source_to_mask(source, shape)
            kind = "object"
        else:
            fatal_error(f"source is type {str(type(source))}, which is not supported.")
        return standardized_source, kind

    @staticmethod
    def _source_to_mask(source, shape):
        """Convert a plantcv.plantcv.Objects ROI to a mask given a shape"""
        if isinstance(source, np.ndarray):
            return source
        if shape is None:
            fatal_error("'shape' must be given to use ROI as source.")
        mask = np.zeros(shape, dtype=np.int32)
        for i, one_roi in enumerate(source):
            cv2.drawContours(mask, one_roi.contours[0], -1, i + 1, -1)
        return mask

    def _to_dict(self):
        """COCO formatted dictionary of the data"""
        return {"info": self.info,
                "licenses": self.licenses,
                "images": self.images,
                "annotations": self.annotations,
                "categories": self.categories}

    def __str__(self):
        """string representation of COCO object"""
        content = vars(self)
        content = {k.strip("_"): v for k, v in content.items()}
        return "plantcv.plantcv.COCO object: " + str(content)

    def __repr__(self):
        """string representation of COCO object"""
        content = vars(self)
        content = {k.strip("_"): v for k, v in content.items()}
        content["images"] = "{" + str(len(content["images"])) + " images...}"
        content["annotations"] = "{" + str(
            int(np.sum([len(d) for d in content["annotations"]]))
        ) + " object annotations...}"
        return "plantcv.plantcv.COCO object:\n" + json.dumps(content, sort_keys=True, indent=4)

    def clear(self):
        """Clear all coco data"""
        self._info = {}
        self._licenses = []
        self._images = []
        self._annotations = []
        self._categories = []

    @property
    def info(self):
        """Get info value"""
        return self._info

    @info.setter
    def info(self, new):
        """Set new info value"""
        self._info = new

    @property
    def licenses(self):
        """Get license value"""
        return self._licenses

    @licenses.setter
    def licenses(self, new):
        """Set new license value"""
        self._licenses = new

    @property
    def images(self):
        """Get images value"""
        return self._images

    @images.setter
    def images(self, new):
        """Set new images value"""
        self._images = new

    @property
    def annotations(self):
        """Get annotations value"""
        return self._annotations

    @annotations.setter
    def annotations(self, new):
        """Set new annotations value"""
        self._annotations = new

    @property
    def categories(self):
        """Get categories value"""
        return self._categories

    @categories.setter
    def categories(self, new):
        """Set new categories value"""
        self._categories = new

    def _update_list_field(self, attr, new):
        """Update a list field to update existing values or append new values"""
        existing = getattr(self, attr)
        new_records = new if isinstance(new, list) else [new]
        for record in new_records:
            which_match = [i for i, v in enumerate(existing) if "id" in record and v.get("id") == record["id"]]
            if which_match:
                for i in which_match:
                    existing[i] = existing[i] | record
            else:
                existing.append(record)
        setattr(self, attr, existing)

    def append(self, other):
        """Append another COCO object's records, renumbering its image and annotation ids"""
        # categories with the same id must be the same category or annotations change meaning
        existing_names = {c["id"]: c.get("name") for c in self.categories}
        for category in other.categories:
            if category["id"] in existing_names and existing_names[category["id"]] != category.get("name"):
                raise ValueError(f"category id {category['id']} is '{existing_names[category['id']]}' "
                                 f"in existing data but '{category.get('name')}' in new data")
        self.info = self.info | other.info
        self._update_list_field(attr="licenses", new=other.licenses)
        self._update_list_field(attr="categories", new=other.categories)
        # offset ids so appended images and annotations never collide with existing ones
        image_offset = _next_id(self.images) - 1
        annotation_offset = _next_id(self.annotations) - 1
        self.images = self.images + [img | {"id": img["id"] + image_offset} for img in other.images]
        self.annotations = self.annotations + [
            ann | {"id": ann["id"] + annotation_offset, "image_id": ann["image_id"] + image_offset}
            for ann in other.annotations
        ]

    def add_record(self, source=None, info=None, rights=None, category=None, **kwargs):
        """Add an image and any appropriate annotations

        Parameters
        ----------
        source : numpy.ndarray or plantcv.plantcv.Objects class ROI,
            binary or labelled mask or ROI object.
        info : dict,
            new key: value pairs to add to the info dictionary
        rights : dict,
            new key: value pairs to add to the license list of dictionaries.
            If any key: value pairs are duplicated then the dictionary is updated
            with any of the new values.
        """
        annotation_kinds = {
            "object": _coco_object_annotation_from_mask
        }
        if info is not None:
            self.info = self.info | info

        if rights is not None:
            self._update_list_field(attr="licenses", new=rights)

        if category is not None:
            self._update_list_field(attr="categories", new=category)

        if source is not None:
            kwargs = {k.lower(): v for k, v in kwargs.items()}
            shape = kwargs.get("shape")
            source, kind = self._standardize_source(source, **kwargs)
            if category is not None and "category_id" not in kwargs:
                kwargs["category_id"] = category["id"]
            category_id = kwargs.get("category_id", 1)
            if category_id not in [c["id"] for c in self.categories]:
                if category_id != 1 or self.categories:
                    raise ValueError(f"category_id {category_id} is not defined, "
                                     "pass category={'id': ..., 'name': ...}")
                # default category, matching COCO(mask)
                self._update_list_field(attr="categories", new={"id": 1, "name": "plant"})
            new_annotations, new_image = annotation_kinds[kind](self, source, **kwargs)
            self.annotations.extend(new_annotations)
            self.images.append(new_image)

    def save(self, filename, mode="a", coco_suffix=True):
        """Save COCO data

        Parameters
        ----------
        filename : str,
            Name of file to save. If file exists then data will be appended.
        mode : str,
            "a" or "w", for "append" or "write".
            If "a" then an existing file will be appended to if possible.
        coco_suffix : bool,
            Should names be enforced to end with '_pcv_coco.json' for compatibility
            with other plantcv functions (plantcv.plantcv.coco.combine)?
        """
        content = self._to_dict()
        suffix = "_pcv_coco.json"
        if not re.search(suffix, filename) and coco_suffix:
            filename = os.path.splitext(filename)[0] + suffix
            print(f"Adding '_pcv_coco.json' suffix ({filename})")

        # if file already exists then append/merge records
        if os.path.isfile(filename) and mode.lower() == "a":
            existing = COCO()
            existing.load(filename)
            existing.append(self)
            content = existing._to_dict()

        with open(filename, mode='w') as fp:
            # Save the data in JSON format with indentation
            json.dump(obj=content, fp=fp, indent=4)

    def load(self, filename):
        """Load COCO data

        Parameters
        ----------
        filename : str,
            Name of file to read from. Should be in COCO format.
        """
        with open(filename, "r") as fp:
            data = json.load(fp)
        self.info = data.get("info", {})
        self.licenses = data.get("licenses", [])
        self.images = data.get("images", [])
        self.annotations = data.get("annotations", [])
        self.categories = data.get("categories", [])
