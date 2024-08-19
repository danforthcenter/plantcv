import cv2
from plantcv.plantcv.visualize import tile


def test_tile(visualize_test_data):
    """Test for PlantCV."""
    # Read in image list
    images = []
    for _ in range(4):
        images.append(cv2.imread(visualize_test_data.small_rgb_img))
    composite = tile(images=images, ncol=3)
    assert composite.shape == (670, 1200, 3)
