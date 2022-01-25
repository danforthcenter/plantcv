import cv2
from plantcv.plantcv import outputs
from plantcv.plantcv.morphology import analyze_stem


def test_analyze_stem(morphology_test_data):
    """Test for PlantCV."""
    # Clear previous outputs
    outputs.clear()
    skel = cv2.imread(morphology_test_data.skel_img)
    stem_obj = morphology_test_data.load_segments(morphology_test_data.segments_file, "stem")
    _ = analyze_stem(rgb_img=skel, stem_objects=stem_obj)
    assert int(outputs.observations['default']['stem_angle']['value']) == 8


def test_analyze_stem_bad_angle(morphology_test_data):
    """Test for PlantCV."""
    skel = cv2.imread(morphology_test_data.skel_img)
    stem_obj = [[[[1116, 1728]], [[1116, 1]]]]
    _ = analyze_stem(rgb_img=skel, stem_objects=stem_obj)
    assert outputs.observations['default']['stem_angle']['value'] == 22877334.0
