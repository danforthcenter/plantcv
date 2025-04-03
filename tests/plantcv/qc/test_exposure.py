import cv2
import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.qc import exposure


def test_plantcv_quality_control(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img, -1)
    _ = exposure(img)
    assert np.isclose(outputs.metadata["red_percent_bad_exposure_qc"]["value"], 0.0007238805970149253)
