import cv2
import numpy as np
from plantcv.plantcv.morphology import prune, _iterative_prune


def test_prune(morphology_test_data):
    """Test for PlantCV."""
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    pruned_img, _, _ = prune(skel_img=skeleton, size=1, mask=skeleton)
    assert np.sum(pruned_img) < np.sum(skeleton)


def test_prune_no_mask(morphology_test_data):
    """Test for PlantCV."""
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    pruned_img, _, _ = prune(skel_img=skeleton, size=100)
    assert np.sum(pruned_img) < np.sum(skeleton)


def test_prune_size0(morphology_test_data):
    """Test for PlantCV."""
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    pruned_img, _, _ = prune(skel_img=skeleton, size=0)
    assert np.sum(pruned_img) == np.sum(skeleton)


def test_iterative_prune(morphology_test_data):
    """Test for PlantCV."""
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    pruned_img = _iterative_prune(skel_img=skeleton, size=3)
    assert np.sum(pruned_img) < np.sum(skeleton)
