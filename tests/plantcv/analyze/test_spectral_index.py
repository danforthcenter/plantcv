import pytest
import numpy as np
import cv2
from plantcv.plantcv.analyze import spectral_index
from plantcv.plantcv import outputs


def test_spectral_index(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    index_array = test_data.load_hsi(test_data.savi_file)
    mask_img = np.ones(np.shape(index_array.array_data), dtype=np.uint8)
    _ = spectral_index(index_img=index_array, labeled_mask=mask_img)

    assert outputs.observations['default1']['mean_index_savi']['value'] > 0


def test_spectral_index_set_range(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    index_array = test_data.load_hsi(test_data.savi_file)
    mask = np.ones(np.shape(index_array.array_data), dtype=np.uint8)
    _ = spectral_index(index_img=index_array, labeled_mask=mask, min_bin=0, max_bin=1)
    assert outputs.observations['default1']['mean_index_savi']['value'] > 0


def test_spectral_index_auto_range(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    index_array = test_data.load_hsi(test_data.savi_file)
    mask = np.ones(np.shape(index_array.array_data), dtype=np.uint8)
    _ = spectral_index(index_img=index_array, labeled_mask=mask, min_bin="auto", max_bin="auto")
    assert outputs.observations['default1']['mean_index_savi']['value'] > 0


def test_spectral_index_outside_range_warning(test_data):
    """Test for PlantCV."""
    import io
    from contextlib import redirect_stderr
    index_array = test_data.load_hsi(test_data.savi_file)
    mask = np.ones(np.shape(index_array.array_data), dtype=np.uint8)
    f = io.StringIO()
    with redirect_stderr(f):
        _ = spectral_index(index_img=index_array, labeled_mask=mask, min_bin=.5, max_bin=.55, label="i")
    out = f.getvalue()
    assert out[0:7] == 'Warning'


def test_spectral_index_bad_input_mask(test_data):
    """Test for PlantCV."""
    index_array = test_data.load_hsi(test_data.savi_file)
    mask = cv2.imread(test_data.hsi_mask_file)
    with pytest.raises(RuntimeError):
        _ = spectral_index(index_img=index_array, labeled_mask=mask)


def test_spectral_index_bad_input_index(test_data):
    """Test for PlantCV."""
    index_array = test_data.load_hsi(test_data.savi_file)
    mask = cv2.imread(test_data.hsi_mask_file, -1)
    index_array.array_data = cv2.imread(test_data.hsi_mask_file)
    with pytest.raises(RuntimeError):
        _ = spectral_index(index_img=index_array, labeled_mask=mask)


def test_spectral_index_bad_input_datatype(test_data):
    """Test for PlantCV."""
    array_data = test_data.load_hsi(test_data.hsi_file)
    mask = cv2.imread(test_data.hsi_mask_file, -1)
    with pytest.raises(RuntimeError):
        _ = spectral_index(index_img=array_data, labeled_mask=mask)
