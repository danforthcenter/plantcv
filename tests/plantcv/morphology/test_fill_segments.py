import cv2
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import fill_segments


def test_fill_segments(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    mask = cv2.imread(morphology_test_data.bin_img, -1)
    _ = fill_segments(mask=mask, objects=morphology_test_data.load_segments(morphology_test_data.segments_file, "edges"),
                      stem_objects=morphology_test_data.load_segments(morphology_test_data.segments_file, "stem"))
    assert outputs.observations['default']["leaf_area"]["value"] == [263, 848, 1407, 1558]


def test_fill_segments_no_stem(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    mask = cv2.imread(morphology_test_data.bin_img, -1)
    _ = fill_segments(mask=mask, objects=morphology_test_data.load_segments(morphology_test_data.segments_file, "edges"))
    assert outputs.observations['default']['segment_area']['value'] == [83, 266, 145, 193, 865, 1407, 1564]
