import cv2
from plantcv.plantcv import watershed_segmentation, outputs


def test_watershed_segmentation(test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    img = cv2.imread(test_data.multi_bin_img)
    mask = cv2.imread(test_data.multi_bin_img, -1)
    _ = watershed_segmentation(rgb_img=img, mask=mask, distance=10)
    assert outputs.observations['default']['estimated_object_count']['value'] == 3
