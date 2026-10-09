import cv2
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import segment_width


def test_segment_width(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    # Read in test data
    # Divide by 255 to convert 0/255 into 0/1 mask, more like other labeled masks
    mask = cv2.imread(morphology_test_data.bin_img, -1) / 255
    skeleton = cv2.imread(morphology_test_data.skel_img, -1)
    mask[100, 100] = 2
    _ = segment_width(segmented_img=mask, skel_img=skeleton, labeled_mask=mask, n_labels=2)
    assert int(sum(outputs.observations['default']['mean_segment_width']['value'])) == 6
