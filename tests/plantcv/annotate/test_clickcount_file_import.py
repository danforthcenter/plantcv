import cv2
from plantcv.plantcv.annotate import clickcount_file_import


def test_plantcv_clickcount_file_import(annotate_test_data):
    """Test for PlantCV."""
    img = cv2.imread(annotate_test_data.discs_mask, -1)
    file  = annotate_test_data.pollen_coords
    counter = clickcount_file_import(img, file)

    assert counter.count['total'] == 70
