# PlantCV classes
import os
import cv2
import json
import datetime
import numpy as np
from importlib.metadata import version
from plantcv.plantcv.annotate.points import _find_closest_pt
from plantcv.plantcv.coco.coco_from_mask import _coco_annotation_from_mask
import matplotlib.pyplot as plt
from math import floor


class Spectral_data:
    """PlantCV Hyperspectral data class"""

    def __init__(self, array_data, max_wavelength, min_wavelength, max_value, min_value, d_type, wavelength_dict,
                 samples, lines, interleave, wavelength_units, array_type, pseudo_rgb, filename, default_bands,
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
        # Pseudo-RGB image if the array_type is a datacube
        self.pseudo_rgb = pseudo_rgb
        # The filename where the data originated from
        self.filename = filename
        # The default band indices needed to make an pseudo_rgb image, if not available then store None
        self.default_bands = default_bands
        # Metadata, flexible components in a dictionary
        self.metadata = metadata
        if not metadata:
            self.metadata = {}


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
                 pseudo_rgb, filename,
                 metadata=None):
        # The actual array/datacube
        self.array_data = array_data
        # Contains all available wavelengths where keys are wavelength and value are indices
        self.wavelength_dict = wavelength_dict
        # store max/min wavelengths
        self.max_wavelength = max_wavelength
        self.min_wavelength = min_wavelength
        # Pseudo-RGB image if the array_type is a datacube
        self.pseudo_rgb = pseudo_rgb
        # The filename where the data originated from
        self.filename = filename
        # default wavelengths for making pseudo rgb
        self.default_bands = None
        # Metadata, flexible components in a dictionary
        self.metadata = metadata

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
            pseudo_rgb=self.pseudo_rgb,
            filename=self.filename,
            metadata=self.metadata
        )
        return sub_ms


class COCO:
    """PlantCV COCO data class"""

    def __init__(self, mask=None, **kwargs):
        # Define which keys are for each coco field
        info_fields = ["description", "datetime", "date", "time"]
        license_fields = ["id", "name", "url"]
        image_anno_fields = ["image_id", "file_name", "date_captured",
                             "license", "iscrowd", "category_id"]

        info_kwargs = {k.lower(): v for k, v in kwargs.items() if k.lower() in info_fields}
        info_kwargs["plantcv_version"] = version("plantcv")
        run_datetime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        info_kwargs["plantcv_run_date"] = run_datetime
        license_kwargs = {k.lower(): v for k, v in kwargs.items() if k.lower() in license_fields}

        licenses = []
        if license_kwargs:
            licenses = [license_kwargs]

        self._info = info_kwargs
        self._license = licenses
        self._images = []
        self._annotations = []
        self._categories = []

        if mask is not None:
            image_kwargs = {k.lower(): v for k, v in kwargs.items() if k.lower() in image_anno_fields}
            self.add_record(mask=mask, info=None, rights=None,
                            category={"id": 1, "name": "plant"},
                            **image_kwargs)

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
        self._info = []
        self._license = []
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
    def license(self):
        """Get license value"""
        return self._license

    @license.setter
    def license(self, new):
        """Set new license value"""
        self._license = new

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
        """Update a list field to update existingvalues or append new values"""
        existing = getattr(self, attr)
        which_match = [i for i, v in enumerate(existing) if bool(set(v.items()) & set(new.items()))]
        if which_match:
            for i in which_match:
                existing[i] = existing[i] | new
        else:
            existing.append(new)
        setattr(self, attr, existing)

    def add_record(self, mask=None, info=None, rights=None, category=None, **kwargs):
        """Add an image and any appropriate annotations

        Parameters
        ----------
        mask : numpy.ndarray,
            binary or labelled mask.
        info : dict,
            new key: value pairs to add to the info dictionary
        rights : dict,
            new key: value pairs to add to the license list of dictionaries.
            If any key: value pairs are duplicated then 
        """
        if info is not None:
            self.info = self.info | info

        if rights is not None:
            self._update_list_field(attr="license", new=rights)

        if category is not None:
            self._update_list_field(attr="categories", new=category)

        if mask is not None:
            new_annotation, new_image = _coco_annotation_from_mask(self, mask, **kwargs)
            self.annotations.append(new_annotation)
            self.images.append(new_image)

    def save(self, filename, mode="a"):
        """Save COCO data

        Parameters
        ----------
        filename : str,
            Name of file to save. If file exists then data will be appended.
        mode : str,
            "a" or "w", for "append" or "write".
            If "a" then an existing file will be appended to if possible.
        """
        # if file already exists then append/merge records
        if os.path.isfile(filename) and mode.lower() == "a":
            with open(filename, 'r') as f:
                existing_data = json.load(f)
                # for info this is a single dict, so overwriting may happen
                self.info= existing_data["info"] | self.info
                # update license, images, and annotations with update method
                self._update_list_field(attr="license", new=existing_data["license"])
                self._update_list_field(attr="images", new=existing_data["images"])
                self._update_list_field(attr="annotations", new=existing_data["annotations"])

        with open(filename, mode='w') as fp:
            content = vars(self)
            content = {k.strip("_"): v for k, v in content.items()}
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
            for key, value in data.items():
                object.__setattr__(self, key, value)
        
