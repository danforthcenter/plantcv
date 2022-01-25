import cv2
from plantcv.plantcv import analyze_thermal_values, outputs


def test_analyze_thermal_values(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    mask = cv2.imread(test_data.thermal_mask, -1)
    img = test_data.load_npz(test_data.thermal_obj_file)
    _ = analyze_thermal_values(thermal_array=img, mask=mask, histplot=True)
    assert outputs.observations['default']['median_temp']['value'] == 33.20922
