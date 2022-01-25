import cv2
import numpy as np
from plantcv.plantcv.transform import gamma_correct


def test_gamma_correct(transform_test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(transform_test_data.small_rgb_img)
    # Test
    gamma_corrected = gamma_correct(img=img, gamma=2, gain=1)
    imgavg = np.average(img)
    correctedavg = np.average(gamma_corrected)
    assert correctedavg != imgavg
