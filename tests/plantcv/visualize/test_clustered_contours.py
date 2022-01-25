import cv2
from plantcv.plantcv import params
from plantcv.plantcv.visualize import clustered_contours


def test_clustered_contours(test_data):
    """Test for PlantCV."""
    # Reset the saved color scale (can be saved between tests)
    params.saved_color_scale = None
    # Read in test data
    img = cv2.imread(test_data.multi_rgb_img, 0)
    cnts, cnt_str = test_data.load_contours(test_data.multi_contours_file)
    clusters = [[36], [19, 28], [10, 11], [35], [22, 21, 27], [3, 14], [37, 33], [18, 26], [13, 12], [34, 41, 42], [25, 24],
                [1, 15, 2], [39, 38], [23, 20, 30, 29], [0, 16, 17], [40], [31, 32], [5, 6, 8, 4, 9, 7]]
    cluster_img = clustered_contours(img=img, grouped_contour_indices=clusters, roi_objects=cnts, roi_obj_hierarchy=cnt_str,
                                     nrow=4, ncol=6, bounding=True)
    assert img.shape == cluster_img.shape[:2]
