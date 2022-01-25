import pytest
import cv2
from plantcv.plantcv import params, outputs
from plantcv.plantcv.photosynthesis import analyze_fvfm


@pytest.mark.parametrize("debug", ["print", "plot", None])
def test_analyze_fvfm(debug, photosynthesis_test_data, tmpdir):
    """Test for PlantCV."""
    # Clear outputs
    outputs.clear()
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    params.debug_outdir = cache_dir
    params.debug = debug
    # Read in test data
    fdark = cv2.imread(photosynthesis_test_data.fdark, -1)
    fmin = cv2.imread(photosynthesis_test_data.fmin, -1)
    fmax = cv2.imread(photosynthesis_test_data.fmax, -1)
    fmask = cv2.imread(photosynthesis_test_data.ps_mask, -1)
    _ = analyze_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=fmask, bins=1000)
    assert outputs.observations['default']['fdark_passed_qc']['value'] is True


def test_analyze_fvfm_bad_fdark(photosynthesis_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    fdark = cv2.imread(photosynthesis_test_data.fdark, -1)
    fmin = cv2.imread(photosynthesis_test_data.fmin, -1)
    fmax = cv2.imread(photosynthesis_test_data.fmax, -1)
    fmask = cv2.imread(photosynthesis_test_data.ps_mask, -1)
    _ = analyze_fvfm(fdark=fdark + 3000, fmin=fmin, fmax=fmax, mask=fmask, bins=1000)
    assert outputs.observations['default']['fdark_passed_qc']['value'] is False


def test_analyze_fvfm_bad_input(photosynthesis_test_data):
    """Test for PlantCV."""
    fdark = cv2.imread(photosynthesis_test_data.fdark)
    fmin = cv2.imread(photosynthesis_test_data.fmin, -1)
    fmax = cv2.imread(photosynthesis_test_data.fmax, -1)
    fmask = cv2.imread(photosynthesis_test_data.ps_mask, -1)
    with pytest.raises(RuntimeError):
        _ = analyze_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=fmask, bins=1000)
