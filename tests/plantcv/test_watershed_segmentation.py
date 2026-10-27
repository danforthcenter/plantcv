import cv2
from plantcv.plantcv import watershed_segmentation, outputs
from tests import synthetic


def test_watershed_segmentation():
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    mask = synthetic.two_plants_mask()
    img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    _ = watershed_segmentation(rgb_img=img, mask=mask, distance=10)
    # One distance-transform peak per disk
    assert outputs.observations['default']['estimated_object_count']['value'] == 2
