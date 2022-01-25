import pytest
import numpy as np
import cv2
from plantcv.plantcv.hyperspectral import analyze_index
from plantcv.plantcv import outputs


def test_analyze_index(hyperspectral_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    index_array = hyperspectral_test_data.load_hsi(hyperspectral_test_data.savi_file)
    mask_img = np.ones(np.shape(index_array.array_data), dtype=np.uint8) * 255
    _ = analyze_index(index_array=index_array, mask=mask_img, histplot=True)

    assert outputs.observations['default']['mean_index_savi']['value'] > 0


def test_analyze_index_set_range(hyperspectral_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    index_array = hyperspectral_test_data.load_hsi(hyperspectral_test_data.savi_file)
    mask = np.ones(np.shape(index_array.array_data), dtype=np.uint8) * 255
    _ = analyze_index(index_array=index_array, mask=mask, histplot=True, min_bin=0, max_bin=1)
    assert outputs.observations['default']['mean_index_savi']['value'] > 0


def test_analyze_index_auto_range(hyperspectral_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    index_array = hyperspectral_test_data.load_hsi(hyperspectral_test_data.savi_file)
    mask = np.ones(np.shape(index_array.array_data), dtype=np.uint8) * 255
    _ = analyze_index(index_array=index_array, mask=mask, min_bin="auto", max_bin="auto")
    assert outputs.observations['default']['mean_index_savi']['value'] > 0


def test_analyze_index_outside_range_warning(hyperspectral_test_data):
    """Test for PlantCV."""
    import io
    from contextlib import redirect_stdout
    index_array = hyperspectral_test_data.load_hsi(hyperspectral_test_data.savi_file)
    mask = np.ones(np.shape(index_array.array_data), dtype=np.uint8) * 255
    f = io.StringIO()
    with redirect_stdout(f):
        _ = analyze_index(index_array=index_array, mask=mask, min_bin=.5, max_bin=.55, label="i")
    out = f.getvalue()
    assert out[0:10] == 'WARNING!!!'


def test_analyze_index_bad_input_mask(hyperspectral_test_data):
    """Test for PlantCV."""
    index_array = hyperspectral_test_data.load_hsi(hyperspectral_test_data.savi_file)
    mask = cv2.imread(hyperspectral_test_data.hsi_mask_file)
    with pytest.raises(RuntimeError):
        _ = analyze_index(index_array=index_array, mask=mask)


def test_analyze_index_bad_input_index(hyperspectral_test_data):
    """Test for PlantCV."""
    index_array = hyperspectral_test_data.load_hsi(hyperspectral_test_data.savi_file)
    mask = cv2.imread(hyperspectral_test_data.hsi_mask_file, -1)
    index_array.array_data = cv2.imread(hyperspectral_test_data.hsi_mask_file)
    with pytest.raises(RuntimeError):
        _ = analyze_index(index_array=index_array, mask=mask)


def test_analyze_index_bad_input_datatype(hyperspectral_test_data):
    """Test for PlantCV."""
    array_data = hyperspectral_test_data.load_hsi(hyperspectral_test_data.hsi_file)
    mask = cv2.imread(hyperspectral_test_data.hsi_mask_file, -1)
    with pytest.raises(RuntimeError):
        _ = analyze_index(index_array=array_data, mask=mask)
