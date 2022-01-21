import cv2
from plantcv.plantcv.morphology import segment_skeleton


def test_segment_skeleton():
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    _ = segment_skeleton(skel_img=skeleton, mask=mask)
    segmented_img, segment_objects = segment_skeleton(skel_img=skeleton)
    assert len(segment_objects) == 73
