import cv2
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import check_cycles


def test_check_cycles(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    mask = cv2.imread(morphology_test_data.ps_mask, -1)
    _ = check_cycles(mask)
    assert outputs.observations['default']['num_cycles']['value'] == 16
