import cv2
import numpy as np
from plantcv.plantcv import distance_transform


def test_distance_transform(test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(test_data.small_bin_img, -1)
    distance_transform_img = distance_transform(bin_img=mask, distance_type=1, mask_size=3)
    # Assert that the output image has the dimensions of the input image and is binary
    assert mask.shape == distance_transform_img.shape and distance_transform_img.dtype == np.float32
