import numpy as np
from plantcv.plantcv.analyze import spectral_reflectance
from plantcv.plantcv import outputs
from tests import synthetic


def test_spectral_reflectance():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    _ = spectral_reflectance(hsi=synthetic.spectral_data(), labeled_mask=synthetic.spectral_mask())
    # The mean of the two masked pixels (1 and 4) in each of the 601 bands
    expected = [np.mean(synthetic.reflectance(wl)[:, 1]) for wl in synthetic.SPECTRAL_WAVELENGTHS]
    np.testing.assert_allclose(outputs.observations['default_1']['wavelength_means']['value'], expected, rtol=1e-12)


def test_spectral_reflectance_key_conversion():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    hsi = synthetic.spectral_data()
    hsi.wavelength_dict = {np.int_(k): v for k, v in hsi.wavelength_dict.items()}
    _ = spectral_reflectance(hsi=hsi, labeled_mask=synthetic.spectral_mask())
    # NumPy integer wavelengths are reported as Python integers
    labels = outputs.observations['default_1']['wavelength_means']['label']
    assert labels == list(synthetic.SPECTRAL_WAVELENGTHS)
    assert all(type(wl) is int for wl in labels)
