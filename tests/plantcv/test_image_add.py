import numpy as np
from plantcv.plantcv import image_add


def test_image_add():
    """Test for PlantCV."""
    # Create test data
    img1 = np.zeros((25, 25), dtype=np.uint8)
    img1[0:10, 0:10] = 255
    img2 = np.zeros((25, 25), dtype=np.uint8)
    img2[15:25, 15:25] = 255
    added_img = image_add(gray_img1=img1, gray_img2=img2)
    # Assert that the output image has the dimensions of the input image and is binary
    assert np.count_nonzero(added_img) == 200
