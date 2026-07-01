import cv2
import numpy as np
from plantcv.plantcv.analyze import spectral_reflectance
from plantcv.plantcv import outputs


def test_spectral_reflectance(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    mask = cv2.imread(test_data.hsi_mask_file, -1)
    _ = spectral_reflectance(hsi=test_data.load_hsi(test_data.hsi_file), labeled_mask=mask)
    assert len(outputs.observations['default_1']['wavelength_means']['value']) == 978


def test_spectral_reflectance_key_conversion(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    mask = cv2.imread(test_data.hsi_mask_file, -1)
    hsi = test_data.load_hsi(test_data.hsi_file)
    hsi.wavelength_dict = {np.int_(k): v for k, v in hsi.wavelength_dict.items()}
    _ = spectral_reflectance(hsi=hsi, labeled_mask=mask)
    assert len(outputs.observations['default_1']['wavelength_means']['value']) == 622
