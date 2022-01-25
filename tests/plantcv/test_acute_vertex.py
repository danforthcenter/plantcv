import cv2
import numpy as np
from plantcv.plantcv import acute_vertex


def test_acute_vertex(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.small_rgb_img)
    obj_contour = test_data.load_composed_contours(test_data.small_composed_contours_file)
    points, _ = acute_vertex(obj=obj_contour, win=5, thresh=15, sep=5, img=img)
    assert points == [[222, 139]]


def test_acute_vertex_bad_obj(test_data):
    """Test for PlantCV."""
    img = cv2.imread(test_data.small_rgb_img)
    obj_contour = np.array([])
    points = acute_vertex(obj=obj_contour, win=5, thresh=15, sep=5, img=img)
    assert points == ["NA", "NA"]
