import cv2
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import find_branch_pts


def test_find_branch_pts(morphology_test_data):
    """Test for PlantCV."""
    outputs.clear()
    mask = cv2.imread(morphology_test_data.bin_img, -1)
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    _ = find_branch_pts(skel_img=skeleton, mask=mask)
    assert len(outputs.observations["default"]["branch_pts"]["value"]) == 5


def test_find_branch_pts_no_mask(morphology_test_data):
    """Test for PlantCV."""
    outputs.clear()
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    _ = find_branch_pts(skel_img=skeleton)
    assert len(outputs.observations["default"]["branch_pts"]["value"]) == 5
