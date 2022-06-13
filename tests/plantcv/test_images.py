import numpy as np
from plantcv.plantcv import Image, BGR, RGB, GRAY, HSI


def test_image():
    """Test creating an Image class image."""
    img = Image(input_array=np.zeros((10, 10), dtype=np.uint8), filename="image.png")
    assert isinstance(img, Image)


def test_image_none():
    """Test creating an Image class image."""
    img = Image(input_array=None, filename=None)
    assert isinstance(img, Image)


def test_image_slice():
    """Test subsetting an Image."""
    img = Image(input_array=np.zeros((10, 10), dtype=np.uint8), filename="image.png")
    assert img[0:5, 0:5].shape == (5, 5)


def test_bgr():
    """Test creating a BGR class image."""
    bgr = BGR(input_array=np.zeros((10, 10, 3), dtype=np.uint8), filename="bgr.png")
    assert isinstance(bgr, BGR)


def test_rgb():
    """Test creating a RGB class image."""
    bgr = RGB(input_array=np.zeros((10, 10, 3), dtype=np.uint8), filename="rgb.png")
    assert isinstance(bgr, RGB)


def test_gray():
    """Test creating a GRAY class image."""
    gray = GRAY(input_array=np.zeros((10, 10), dtype=np.uint8), filename="gray.png")
    assert isinstance(gray, GRAY)


def test_hsi():
    """Test creating an HSI class image."""
    hsi = HSI(input_array=np.zeros((10, 10, 5), dtype=np.uint8), filename="hsi.data", wavelengths=[480, 540, 710, 800, 900],
              default_wavelengths=None, wavelength_units="nm")
    assert isinstance(hsi, HSI)


def test_hsi_grayscale_thumb():
    """Test creating an HSI class image."""
    hsi = HSI(input_array=np.zeros((10, 10, 5), dtype=np.uint8), filename="hsi.data", wavelengths=[700, 800, 900],
              default_wavelengths=None, wavelength_units="nm")
    assert isinstance(hsi, HSI)
