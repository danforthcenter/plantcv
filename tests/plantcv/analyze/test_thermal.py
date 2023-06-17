import cv2
from plantcv.plantcv import outputs
from plantcv.plantcv.analyze import thermal as analyze_thermal


def test_thermal(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    mask = cv2.imread(test_data.thermal_mask, -1)
    img = test_data.load_npz(test_data.thermal_obj_file)
    _ = analyze_thermal(thermal_img=img, labeled_mask=mask)
    assert outputs.observations['default1']['median_temp']['value'] == 33.20922
