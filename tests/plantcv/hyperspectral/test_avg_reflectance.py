import numpy as np
from plantcv.plantcv.hyperspectral import _avg_reflectance
from tests import synthetic


def test_avg_reflectance():
    """Test for PlantCV."""
    avg_reflect = _avg_reflectance(synthetic.spectral_data(), mask=synthetic.spectral_mask())
    # The mean of the two masked pixels (1 and 4) in each band
    expected = [np.mean(synthetic.reflectance(wl)[:, 1]) for wl in synthetic.SPECTRAL_WAVELENGTHS]
    np.testing.assert_allclose(avg_reflect, expected, rtol=1e-12)
