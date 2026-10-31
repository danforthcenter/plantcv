import numpy as np
from plantcv.plantcv.hyperspectral import extract_wavelength
from tests import synthetic


def test_extract_wavelength():
    """Test for PlantCV."""
    new = extract_wavelength(spectral_data=synthetic.spectral_data(), wavelength=500)
    assert np.shape(new.array_data) == (2, 3)
    # The datacube has a band at exactly 500 nm
    assert np.array_equal(new.array_data, synthetic.reflectance(500))
