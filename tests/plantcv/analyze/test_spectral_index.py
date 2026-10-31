import pytest
import numpy as np
from plantcv.plantcv import Spectral_data
from plantcv.plantcv.analyze import spectral_index
from plantcv.plantcv import outputs
from tests import synthetic

# A 2 x 3 SAVI index with values 0.1 to 0.6: mean and median 0.35, standard deviation sqrt(35 / 1200)
INDEX_VALUES = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])


def _savi_index():
    """Create a SAVI index image with INDEX_VALUES."""
    return Spectral_data(array_data=INDEX_VALUES.copy(), max_wavelength=0, min_wavelength=0, max_value=0.6,
                         min_value=0.1, d_type=np.uint8, wavelength_dict={}, samples=3, lines=2, interleave="bil",
                         wavelength_units="nm", array_type="index_savi", filename="synthetic", default_bands=None)


def _check_stats():
    """Check the statistics of the whole index."""
    obs = outputs.observations['default_1']
    assert obs['mean_index_savi']['value'] == pytest.approx(0.35)
    assert obs['med_index_savi']['value'] == pytest.approx(0.35)
    assert obs['std_index_savi']['value'] == pytest.approx(np.sqrt(35 / 1200))


def test_spectral_index():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    index_array = _savi_index()
    mask_img = np.ones(np.shape(index_array.array_data), dtype=np.uint8)
    _ = spectral_index(index_img=index_array, labeled_mask=mask_img)
    _check_stats()


def test_spectral_index_set_range():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    index_array = _savi_index()
    mask = np.ones(np.shape(index_array.array_data), dtype=np.uint8)
    _ = spectral_index(index_img=index_array, labeled_mask=mask, min_bin=0, max_bin=1)
    _check_stats()


def test_spectral_index_auto_range():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    index_array = _savi_index()
    mask = np.ones(np.shape(index_array.array_data), dtype=np.uint8)
    _ = spectral_index(index_img=index_array, labeled_mask=mask, min_bin="auto", max_bin="auto")
    _check_stats()


def test_spectral_index_outside_range_warning():
    """Test for PlantCV."""
    import io
    from contextlib import redirect_stderr
    index_array = _savi_index()
    mask = np.ones(np.shape(index_array.array_data), dtype=np.uint8)
    f = io.StringIO()
    with redirect_stderr(f):
        # The values 0.1 to 0.6 extend past both ends of the bin range
        _ = spectral_index(index_img=index_array, labeled_mask=mask, min_bin=.5, max_bin=.55, label="i")
    out = f.getvalue()
    assert out[0:7] == 'Warning'


def test_spectral_index_bad_input_mask():
    """Test for PlantCV."""
    index_array = _savi_index()
    # A 3-channel mask
    mask = np.zeros((2, 3, 3), dtype=np.uint8)
    with pytest.raises(RuntimeError):
        _ = spectral_index(index_img=index_array, labeled_mask=mask)


def test_spectral_index_bad_input_index():
    """Test for PlantCV."""
    index_array = _savi_index()
    mask = synthetic.spectral_mask()
    # A 3-channel index
    index_array.array_data = np.zeros((2, 3, 3), dtype=np.uint8)
    with pytest.raises(RuntimeError):
        _ = spectral_index(index_img=index_array, labeled_mask=mask)


def test_spectral_index_bad_input_datatype():
    """Test for PlantCV."""
    # A datacube is not an index
    with pytest.raises(RuntimeError):
        _ = spectral_index(index_img=synthetic.spectral_data(), labeled_mask=synthetic.spectral_mask())
