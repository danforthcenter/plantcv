import cv2
from plantcv.plantcv.hyperspectral import analyze_spectral
from plantcv.plantcv import outputs


def test_analyze_spectral(hyperspectral_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    mask = cv2.imread(hyperspectral_test_data.hsi_mask_file, -1)
    _ = analyze_spectral(array=hyperspectral_test_data.load_hsi(hyperspectral_test_data.hsi_file), mask=mask,
                         histplot=True, label="prefix")
    assert len(outputs.observations['prefix']['spectral_frequencies']['value']) == 978
