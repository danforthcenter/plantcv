"""PlantCV data classes"""
import numpy as np


class Image(np.ndarray):
    """Generic image class that extends the np.ndarray class."""

    # From NumPy documentation
    # Add uri attribute
    def __new__(cls, input_array: np.ndarray, uri: str):
        obj = np.asarray(input_array).view(cls)
        # New attribute uri stores uniform resource identifier of the source file
        obj.uri = uri
        return obj

    def __array_finalize__(self, obj):
        if obj is not None:
            self.uri = getattr(obj, "uri", None)

    def __getitem__(self, key):
        # Enhance the np.ndarray __getitem__ method
        # Slice the array as requested but return an array of the same class
        # Idea from NumPy examples of subclassing:
        return super(Image, self).__getitem__(key)


class GRAY(Image):
    """Subclass of Image for grayscale images."""

    def __new__(cls, input_array: np.ndarray, uri: str):
        return Image.__new__(cls, input_array, uri)


class BGR(Image):
    """Subclass of Image for Blue, Green, Red (BGR) images."""

    def __new__(cls, input_array: np.ndarray, uri: str):
        return Image.__new__(cls, input_array, uri)

    def __getitem__(self, key):
        # Overwrite the __getitem__ method to return a GRAY object if the
        # requested slice is 2D
        new_arr = super(Image, self).__getitem__(key)
        if len(new_arr.shape) == 2:
            return GRAY(input_array=new_arr, uri=self.uri)
        return new_arr


class RGB(Image):
    """Subclass of Image for Red, Green, Blue (RGB) images."""

    def __new__(cls, input_array: np.ndarray, uri: str):
        return Image.__new__(cls, input_array, uri)

    def __getitem__(self, key):
        # Overwrite the __getitem__ method to return a GRAY object if the
        # requested slice is 2D
        new_arr = super(Image, self).__getitem__(key)
        if len(new_arr.shape) == 2:
            return GRAY(input_array=new_arr, uri=self.uri)
        return new_arr


class HSI(Image):
    """Subclass of Image for hyperspectral images."""

    def __new__(cls, input_array: np.ndarray, uri: str, wavelengths: list, default_wavelengths: list,
                wavelength_units: str = "nm"):
        # Create an instance of Image with default attributes
        obj = Image.__new__(cls, input_array, uri)
        # Add HSI-specific attributes
        obj.wavelengths = wavelengths
        obj.wavelength_units = wavelength_units
        obj.min_wavelength = np.min(wavelengths)
        obj.max_wavelength = np.max(wavelengths)
        obj.default_wavelengths = default_wavelengths
        if default_wavelengths is None:
            if obj.max_wavelength >= 635 and obj.min_wavelength <= 490:
                obj.default_wavelengths = [480, 540, 710]
            else:
                obj.default_wavelengths = [wavelengths[np.argmax(np.sum(input_array, axis=(0, 1)))]]
        return obj

    def __init__(self, **kwargs):
        self.thumb = self._create_thumb()

    def get_wavelength(self, wavelength):
        idx = np.abs(np.array(self.wavelengths) - wavelength).argmin()
        obj = super(HSI, self).__getitem__(np.s_[:, :, idx])
        obj.wavelengths = [self.wavelengths[idx]]
        obj.min_wavelength = np.min(obj.wavelengths)
        obj.max_wavelength = np.max(obj.wavelengths)
        return obj

    def _create_thumb(self):
        if len(self.default_wavelengths) == 3:
            thumb = BGR(input_array=np.dstack([self.get_wavelength(self.default_wavelengths[0]),
                                               self.get_wavelength(self.default_wavelengths[1]),
                                               self.get_wavelength(self.default_wavelengths[2])]),
                        uri=self.uri)
        else:
            thumb = GRAY(input_array=self.get_wavelength(self.default_wavelengths[0]),
                         uri=self.uri)
        return thumb
