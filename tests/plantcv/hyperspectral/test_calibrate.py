import copy
import numpy as np
from plantcv.plantcv.hyperspectral import calibrate
from tests import synthetic


def _reference(line_values):
    """Copy the synthetic datacube with one constant value per line."""
    reference = copy.deepcopy(synthetic.spectral_data())
    bands = len(synthetic.SPECTRAL_WAVELENGTHS)
    reference.array_data = np.stack([np.full((synthetic.SPECTRAL_SHAPE[1], bands), v) for v in line_values])
    return reference


def test_calibrate():
    """Test for PlantCV."""
    raw = synthetic.spectral_data()
    # References are averaged over their lines: white 2, dark 0.5
    white = _reference([1.5, 2.5, 2, 2])
    dark = _reference([0.4, 0.6])
    calibrated = calibrate(raw_data=raw, white_reference=white, dark_reference=dark)
    assert np.shape(calibrated.array_data) == (2, 3, 601)
    # (raw - dark) / (white - dark), clipped to [0, 1]
    np.testing.assert_allclose(calibrated.array_data, np.clip((raw.array_data - 0.5) / 1.5, 0, 1), rtol=1e-12)
