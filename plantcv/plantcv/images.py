import numpy as np


class Image(np.ndarray):
    """The generic Image class extends the np.ndarray class by adding attributes."""

    # From NumPy documentation
    # Add filename attribute
    def __new__(cls, input_array: np.ndarray, filename: str):
        obj = np.asarray(input_array).view(cls)
        # New attribute filename stores the path and filename of the source file
        obj.filename = filename
        return obj

    def __array_finalize__(self, obj):
        if obj is not None:
            self.filename = getattr(obj, "filename", None)

    def __getitem__(self, key):
        # Enhance the np.ndarray __getitem__ method
        # Slice the array as requested but return an array of the same class
        # Idea from NumPy examples of subclassing:
        value = super(Image, self).__getitem__(key)
        return value


class BGR(Image):
    """Subclass of Image for Blue Green Red (BGR)/OpenCV-type images."""

    def __new__(cls, input_array: np.ndarray, filename: str):
        # Create an instance of Image but return an instance of BGR
        obj = Image.__new__(cls, input_array, filename)
        return obj


class RGB(Image):
    """Subclass of Image for Red Green Blue (RGB)-type images."""

    def __new__(cls, input_array: np.ndarray, filename: str):
        # Create an instance of Image but return an instance of RGB
        obj = Image.__new__(cls, input_array, filename)
        return obj


class GRAY(Image):
    """Subclass of Image for grayscale images."""

    def __new__(cls, input_array: np.ndarray, filename: str):
        # Create an instance of Image but return an instance of GRAY
        obj = Image.__new__(cls, input_array, filename)
        return obj


class HSI(Image):
    """Subclass of Image for hyperspectral images."""

    def __new__(cls, input_array: np.ndarray, filename: str, wavelengths: list, wavelength_units: str,
                default_wavelengths: list):
        # Create an instance of Image with default attributes
        obj = Image.__new__(cls, input_array, filename)
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
        idx = np.abs(self - wavelength).argmin()
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
                        filename=self.filename)
        else:
            thumb = GRAY(input_array=self.get_wavelength(self.default_wavelengths[0]),
                         filename=self.filename)
        return thumb
