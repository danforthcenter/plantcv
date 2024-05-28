import pytest
import cv2
import numpy as np
from plantcv.plantcv.visualize import obj_sizes


@pytest.mark.parametrize("num,expected", [[100, 4], [1, 4]])
def test_obj_sizes(num, expected, test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.multi_bin_img, -1)
    visualization = obj_sizes(img=img, mask=img, num_objects=num)
    # Output unique colors are the 32 objects, the gray text, the black background, and white unlabeled leaves
    assert len(np.unique(visualization.reshape(-1, visualization.shape[2]), axis=0)) == expected
