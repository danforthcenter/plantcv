import cv2
from plantcv.plantcv import cluster_contour_splitimg


def test_cluster_contours_splitimg(test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    # Read in test data
    img = cv2.imread(test_data.multi_rgb_img)
    cnts, cnt_str = test_data.load_contours(test_data.multi_contours_file)
    clusters = [[36], [19, 28], [10, 11], [35], [22, 21, 27], [3, 14], [37, 33], [18, 26], [13, 12], [34, 41, 42], [25, 24],
                [1, 15, 2], [39, 38], [23, 20, 30, 29], [0, 16, 17], [40], [31, 32], [5, 6, 8, 4, 9, 7]]
    cluster_names = test_data.cluster_names
    _, imgs, _ = cluster_contour_splitimg(img=img, grouped_contour_indexes=clusters, contours=cnts, hierarchy=cnt_str,
                                          outdir=cache_dir, file="multi", filenames=cluster_names)
    assert len(imgs) == 15


def test_cluster_contours_splitimg_defaults(test_data, tmpdir):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.multi_rgb_img)
    cnts, cnt_str = test_data.load_contours(test_data.multi_contours_file)
    clusters = [[36], [19, 28], [10, 11], [35], [22, 21, 27], [3, 14], [37, 33], [18, 26], [13, 12], [34, 41, 42], [25, 24],
                [1, 15, 2], [39, 38], [23, 20, 30, 29], [0, 16, 17], [40], [31, 32], [5, 6, 8, 4, 9, 7]]
    _, imgs, _ = cluster_contour_splitimg(img=img, grouped_contour_indexes=clusters, contours=cnts, hierarchy=cnt_str,
                                          outdir=None, file=None, filenames=None)
    assert len(imgs) == 18


def test_cluster_contours_splitimg_grayscale(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.multi_rgb_img, 0)
    cnts, cnt_str = test_data.load_contours(test_data.multi_contours_file)
    clusters = [[36], [19, 28], [10, 11], [35], [22, 21, 27], [3, 14], [37, 33], [18, 26], [13, 12], [34, 41, 42], [25, 24],
                [1, 15, 2], [39, 38], [23, 20, 30, 29], [0, 16, 17], [40], [31, 32], [5, 6, 8, 4, 9, 7]]
    _, imgs, _ = cluster_contour_splitimg(img=img, grouped_contour_indexes=clusters, contours=cnts, hierarchy=cnt_str,
                                          outdir=None, file=None, filenames=None)
    assert len(imgs) == 18


def test_cluster_contours_splitimg_mismatch(test_data):
    """Test for PlantCV."""
    # Read in test data
    img = cv2.imread(test_data.multi_rgb_img)
    cnts, cnt_str = test_data.load_contours(test_data.multi_contours_file)
    clusters = [[36], [19, 28], [10, 11], [35], [22, 21, 27], [3, 14], [37, 33], [18, 26], [13, 12], [34, 41, 42], [25, 24],
                [1, 15, 2], [39, 38], [23, 20, 30, 29], [0, 16, 17], [40], [31, 32], [5, 6, 8, 4, 9, 7]]
    cluster_names_too_many = test_data.cluster_names_too_many
    _, imgs, _ = cluster_contour_splitimg(img=img, grouped_contour_indexes=clusters, contours=cnts, hierarchy=cnt_str,
                                          outdir=None, file=None, filenames=cluster_names_too_many)
    assert len(imgs) == 18
