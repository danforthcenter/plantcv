import cv2
from plantcv.plantcv.annotate import ClickCount


def test_plantcv_clickcount_file_import(annotate_test_data):
    """Test for PlantCV."""
    img = cv2.imread(annotate_test_data.discs_mask, -1)
    counter = ClickCount(img, figsize=(8, 6))
    file  = annotate_test_data.pollen_coords
    counter.file_import(img, file)

    assert counter.count['total'] == 70
