import cv2
import numpy as np
from plantcv.plantcv.morphology import skeletonize


def test_skeletonize(morphology_test_data):
    """Test for PlantCV."""
    mask = cv2.imread(morphology_test_data.bin_img, -1)
    input_skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    skeleton = skeletonize(mask=mask)
    arr = np.array(skeleton == input_skeleton)
    assert arr.all()
