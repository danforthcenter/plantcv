import cv2
from plantcv.plantcv.analyze import spectral_reflectance
from plantcv.plantcv import outputs


def test_spectral_reflectance(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    mask = cv2.imread(test_data.hsi_mask_file, -1)
    _ = spectral_reflectance(hsi=test_data.load_hsi(test_data.hsi_file), labeled_mask=mask)
    assert len(outputs.observations['default1']['wavelength_means']['value']) == 978
