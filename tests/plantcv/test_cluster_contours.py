import cv2
from plantcv.plantcv import cluster_contours


def test_cluster_contours(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.multi_rgb_img)
    cnts, cnt_str = test_data.load_contours(test_data.multi_contours_file)
    clusters_i, _, _ = cluster_contours(img=img, roi_objects=cnts, roi_obj_hierarchy=cnt_str, nrow=4, ncol=6, show_grid=True)
    assert len(clusters_i) == 18


def test_cluster_contours_grayscale_input(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.multi_rgb_img, 0)
    cnts, cnt_str = test_data.load_contours(test_data.multi_contours_file)
    clusters_i, _, _ = cluster_contours(img=img, roi_objects=cnts, roi_obj_hierarchy=cnt_str, nrow=4, ncol=6, show_grid=True)
    assert len(clusters_i) == 18


def test_cluster_contours_default_rc(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.multi_rgb_img)
    cnts, cnt_str = test_data.load_contours(test_data.multi_contours_file)
    clusters_i, _, _ = cluster_contours(img=img, roi_objects=cnts, roi_obj_hierarchy=cnt_str, show_grid=True)
    assert len(clusters_i) == 1
