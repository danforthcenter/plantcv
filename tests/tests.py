#!/usr/bin/env python

import pytest
import os
import shutil
import numpy as np
import cv2
from plantcv import plantcv as pcv
import plantcv.learn
# Import matplotlib and use a null Template to block plotting to screen
# This will let us test debug = "plot"
import matplotlib

matplotlib.use('Agg', warn=False)

TEST_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
TEST_TMPDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".cache")
TEST_COLOR_DIM = (2056, 2454, 3)
TEST_GRAY_DIM = (2056, 2454)
TEST_BINARY_DIM = TEST_GRAY_DIM
TEST_INPUT_COLOR = "input_color_img.jpg"
TEST_INPUT_GRAY = "input_gray_img.jpg"
TEST_INPUT_GRAY_SMALL = "input_gray_img_small.jpg"
TEST_INPUT_BINARY = "input_binary_img.png"
TEST_INPUT_BAYER = "bayer_img.png"
TEST_INPUT_ROI = "input_roi.npz"
TEST_INPUT_CONTOURS = "input_contours.npz"
TEST_INPUT_CONTOURS1 = "input_contours1.npz"
TEST_VIS = "VIS_SV_0_z300_h1_g0_e85_v500_93054.png"
TEST_NIR = "NIR_SV_0_z300_h1_g0_e15000_v500_93059.png"
TEST_VIS_TV = "VIS_TV_0_z300_h1_g0_e85_v500_93054.png"
TEST_NIR_TV = "NIR_TV_0_z300_h1_g0_e15000_v500_93059.png"
TEST_INPUT_MASK = "input_mask.png"
TEST_INPUT_MASK_RESIZE = "input_mask_resize.png"
TEST_INPUT_NIR_MASK = "input_nir.png"
TEST_INPUT_FDARK = "FLUO_TV_dark.png"
TEST_INPUT_FDARK_LARGE = "FLUO_TV_DARK_large"
TEST_INPUT_FMIN = "FLUO_TV_min.png"
TEST_INPUT_FMAX = "FLUO_TV_max.png"
TEST_INPUT_FMASK = "FLUO_TV_MASK.png"
TEST_INTPUT_GREENMAG = "input_green-magenta.jpg"
TEST_INTPUT_MULTI = "multi_ori_image.jpg"
TEST_INPUT_MULTI_OBJECT = "roi_objects.npz"
TEST_INPUT_MULTI_CONTOUR = "multi_contours.npz"
TEST_INPUT_ClUSTER_CONTOUR = "clusters_i.npz"
TEST_INPUT_MULTI_HIERARCHY = "multi_hierarchy.npz"
TEST_INPUT_GENOTXT = "cluster_names.txt"
TEST_INPUT_GENOTXT_TOO_MANY = "cluster_names_too_many.txt"
TEST_INPUT_CROPPED = 'cropped_img.jpg'
TEST_INPUT_CROPPED_MASK = 'cropped-mask.png'
TEST_INPUT_MARKER = 'seed-image.jpg'
TEST_FOREGROUND = "TEST_FOREGROUND.jpg"
TEST_BACKGROUND = "TEST_BACKGROUND.jpg"
TEST_PDFS = "naive_bayes_pdfs.txt"
TEST_PDFS_BAD = "naive_bayes_pdfs_bad.txt"
TEST_VIS_SMALL = "setaria_small_vis.png"
TEST_MASK_SMALL = "setaria_small_mask.png"
TEST_VIS_COMP_CONTOUR = "setaria_composed_contours.npz"
TEST_ACUTE_RESULT = np.asarray([[[119, 285]], [[151, 280]], [[168, 267]], [[168, 262]], [[171, 261]], [[224, 269]],
                                [[246, 271]], [[260, 277]], [[141, 248]], [[183, 194]], [[188, 237]], [[173, 240]],
                                [[186, 260]], [[147, 244]], [[163, 246]], [[173, 268]], [[170, 272]], [[151, 320]],
                                [[195, 289]], [[228, 272]], [[210, 272]], [[209, 247]], [[210, 232]]])
TEST_VIS_SMALL_PLANT = "setaria_small_plant_vis.png"
TEST_MASK_SMALL_PLANT = "setaria_small_plant_mask.png"
TEST_VIS_COMP_CONTOUR_SMALL_PLANT = "setaria_small_plant_composed_contours.npz"
TEST_SAMPLED_RGB_POINTS = "sampled_rgb_points.txt"
TEST_TARGET_IMG = "target_img.png"
TEST_TARGET_IMG_WITH_HEXAGON = "target_img_w_hexagon.png"
TEST_SOURCE1_IMG = "source1_img.png"
TEST_SOURCE2_IMG = "source2_img.png"
TEST_TARGET_MASK = "mask_img.png"
TEST_TARGET_IMG_COLOR_CARD = "color_card_target.png"
TEST_SOURCE2_MASK = "mask2_img.png"
TEST_TARGET_MATRIX = "target_matrix.npz"
TEST_SOURCE1_MATRIX = "source1_matrix.npz"
TEST_SOURCE2_MATRIX = "source2_matrix.npz"
TEST_MATRIX_B1 = "matrix_b1.npz"
TEST_MATRIX_B2 = "matrix_b2.npz"
TEST_TRANSFORM1 = "transformation_matrix1.npz"
TEST_MATRIX_M1 = "matrix_m1.npz"
TEST_MATRIX_M2 = "matrix_m2.npz"
TEST_S1_CORRECTED = "source_corrected.png"


# ##########################
# Tests setup function
# ##########################
def setup_function():
    if not os.path.exists(TEST_TMPDIR):
        os.mkdir(TEST_TMPDIR)


# ##########################
# Tests for the main package
# ##########################
def test_plantcv_acute():
    # Read in test data
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.acute(obj=obj_contour, win=5, thresh=15, mask=mask)
    _ = pcv.acute(obj=obj_contour, win=0, thresh=15, mask=mask)
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.acute(obj=obj_contour, win=0, thresh=15, mask=mask)
    homology_pts = pcv.acute(obj=obj_contour, win=5, thresh=15, mask=mask)
    assert all([i == j] for i, j in zip(np.shape(homology_pts), (29, 1, 2)))


def test_plantcv_acute_vertex():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_acute_vertex")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL))
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.acute_vertex(obj=obj_contour, win=5, thresh=15, sep=5, img=img)
    _ = pcv.acute_vertex(obj=[], win=5, thresh=15, sep=5, img=img)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.acute_vertex(obj=obj_contour, win=5, thresh=15, sep=5, img=img)
    # Test with debug = None
    pcv.params.debug = None
    acute = pcv.acute_vertex(obj=obj_contour, win=5, thresh=15, sep=5, img=img)
    assert all([i == j] for i, j in zip(np.shape(acute), np.shape(TEST_ACUTE_RESULT)))


def test_plantcv_acute_vertex_bad_obj():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL))
    obj_contour = np.array([])
    pcv.params.debug = None
    result = pcv.acute_vertex(obj=obj_contour, win=5, thresh=15, sep=5, img=img)
    assert all([i == j] for i, j in zip(result, [0, ("NA", "NA")]))


def test_plantcv_analyze_bound_horizontal():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_bound_horizontal")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    img_above_bound_only = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL_PLANT))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    object_contours = contours_npz['arr_0']
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=300)
    _ = pcv.analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=100)
    _ = pcv.analyze_bound_horizontal(img=img_above_bound_only, obj=object_contours, mask=mask, line_position=300)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=300)
    # Test with debug = None
    pcv.params.debug = None
    boundary_header, boundary_data, boundary_img1 = pcv.analyze_bound_horizontal(img=img, obj=object_contours,
                                                                                 mask=mask, line_position=300)
    assert boundary_data[3] == 62555


def test_plantcv_analyze_bound_horizontal_grayscale_image():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    object_contours = contours_npz['arr_0']
    # Test with a grayscale reference image and debug="plot"
    pcv.params.debug = "plot"
    boundary_header, boundary_data, boundary_img1 = pcv.analyze_bound_horizontal(img=img, obj=object_contours,
                                                                                 mask=mask, line_position=300)
    assert boundary_data[3] == 62555


def test_plantcv_analyze_bound_horizontal_neg_y():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    object_contours = contours_npz['arr_0']
    # Test with debug=None, line position that will trigger -y
    pcv.params.debug = None
    boundary_header, boundary_data, boundary_img1 = pcv.analyze_bound_horizontal(img=img, obj=object_contours,
                                                                                 mask=mask, line_position=2056)
    assert boundary_data[3] == 63632


def test_plantcv_analyze_bound_vertical():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_bound_vertical")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    object_contours = contours_npz['arr_0']
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.analyze_bound_vertical(img=img, obj=object_contours, mask=mask, line_position=1000)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.analyze_bound_vertical(img=img, obj=object_contours, mask=mask, line_position=1000)
    # Test with debug = None
    pcv.params.debug = None
    boundary_header, boundary_data, boundary_img1 = pcv.analyze_bound_vertical(img=img, obj=object_contours,
                                                                               mask=mask, line_position=1000)
    assert boundary_data[3] == 5016


def test_plantcv_analyze_bound_vertical_grayscale_image():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    object_contours = contours_npz['arr_0']
    # Test with a grayscale reference image and debug="plot"
    pcv.params.debug = "plot"
    boundary_header, boundary_data, boundary_img1 = pcv.analyze_bound_vertical(img=img, obj=object_contours,
                                                                               mask=mask, line_position=1000)
    assert boundary_data[3] == 5016


def test_plantcv_analyze_bound_vertical_neg_x():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    object_contours = contours_npz['arr_0']
    # Test with debug="plot", line position that will trigger -x
    pcv.params.debug = "plot"
    boundary_header, boundary_data, boundary_img1 = pcv.analyze_bound_vertical(img=img, obj=object_contours,
                                                                               mask=mask, line_position=2454)
    assert boundary_data[3] == 63632


def test_plantcv_analyze_bound_vertical_small_x():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    object_contours = contours_npz['arr_0']
    # Test with debug='plot', line position that will trigger -x, and two channel object
    pcv.params.debug = "plot"
    boundary_header, boundary_data, boundary_img1 = pcv.analyze_bound_vertical(img=img, obj=object_contours,
                                                                               mask=mask, line_position=1)
    assert boundary_data[3] == 0


def test_plantcv_analyze_color():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_color")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.analyze_color(rgb_img=img, mask=mask, bins=256, hist_plot_type="all")
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.analyze_color(rgb_img=img, mask=mask, bins=256, hist_plot_type='rgb')
    # Test with debug = "plot" and pseudo_bkg = "white"
    _ = pcv.analyze_color(rgb_img=img, mask=mask, bins=256, hist_plot_type='lab')
    _ = pcv.analyze_color(rgb_img=img, mask=mask, bins=256, hist_plot_type='hsv')

    # Test with debug = None
    pcv.params.debug = None
    color_header, color_data, analysis_images = pcv.analyze_color(rgb_img=img, mask=mask, bins=256,
                                                                  hist_plot_type=None)
    assert np.sum(color_data[3]) != 0


def test_plantcv_analyze_color_incorrect_image():
    img_binary = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.analyze_color(rgb_img=img_binary, mask=mask, bins=256, hist_plot_type=None)


# def test_plantcv_analyze_color_incorrect_pseudo_channel():
#     img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
#     mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
#     with pytest.raises(RuntimeError):
#         pcv.params.debug = "plot"
#         _ = pcv.analyze_color(rgb_img=img, mask=mask, bins=256, hist_plot_type=None, pseudo_channel="x",
#                               pseudo_bkg="white", filename=False)
#
#
# def test_plantcv_analyze_color_incorrect_pseudo_background():
#     img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
#     mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
#     with pytest.raises(RuntimeError):
#         pcv.params.debug = "plot"
#         _ = pcv.analyze_color(rgb_img=img, mask=mask, bins=256, hist_plot_type=None, pseudo_channel="v",
#                               pseudo_bkg="black", filename=False)


def test_plantcv_analyze_color_incorrect_hist_plot_type():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    with pytest.raises(RuntimeError):
        pcv.params.debug = "plot"
        _ = pcv.analyze_color(rgb_img=img, mask=mask, bins=256, hist_plot_type="bgr")


def test_plantcv_analyze_nir():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_nir")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.analyze_nir_intensity(gray_img=img, mask=mask, bins=256, histplot=True)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.analyze_nir_intensity(gray_img=img, mask=mask, bins=256, histplot=False)
    # Test with debug = "plot"
    _ = pcv.analyze_nir_intensity(gray_img=img, mask=mask, bins=256, histplot=True)
    # Test with debug = None
    pcv.params.debug = None
    hist_header, hist_data, h_norm = pcv.analyze_nir_intensity(gray_img=img, mask=mask, bins=256, histplot=False)
    assert np.sum(hist_data[3]) == 63632


def test_plantcv_analyze_object():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_object")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    # max_obj = max(obj_contour, key=len)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    # Test with debug = None
    pcv.params.debug = None
    obj_header, obj_data, obj_images = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    assert obj_data[1] != 0


def test_plantcv_analyze_object_grayscale_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_object_grayscale_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    # max_obj = max(obj_contour, key=len)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    obj_header, obj_data, obj_images = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    assert obj_data[1] != 0


def test_plantcv_analyze_object_zero_slope():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_object_zero_slope")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Create a test image
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    img[10:11, 10:40, 0] = 255
    mask = img[:, :, 0]
    obj_contour = np.array([[[10, 10]], [[11, 10]], [[12, 10]], [[13, 10]], [[14, 10]], [[15, 10]], [[16, 10]],
                            [[17, 10]], [[18, 10]], [[19, 10]], [[20, 10]], [[21, 10]], [[22, 10]], [[23, 10]],
                            [[24, 10]], [[25, 10]], [[26, 10]], [[27, 10]], [[28, 10]], [[29, 10]], [[30, 10]],
                            [[31, 10]], [[32, 10]], [[33, 10]], [[34, 10]], [[35, 10]], [[36, 10]], [[37, 10]],
                            [[38, 10]], [[39, 10]], [[38, 10]], [[37, 10]], [[36, 10]], [[35, 10]], [[34, 10]],
                            [[33, 10]], [[32, 10]], [[31, 10]], [[30, 10]], [[29, 10]], [[28, 10]], [[27, 10]],
                            [[26, 10]], [[25, 10]], [[24, 10]], [[23, 10]], [[22, 10]], [[21, 10]], [[20, 10]],
                            [[19, 10]], [[18, 10]], [[17, 10]], [[16, 10]], [[15, 10]], [[14, 10]], [[13, 10]],
                            [[12, 10]], [[11, 10]]], dtype=np.int32)
    # Test with debug = None
    pcv.params.debug = None
    obj_header, obj_data, obj_images = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    assert obj_data[7] == 30


def test_plantcv_analyze_object_longest_axis_2d():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_object_longest_axis_2d")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Create a test image
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    img[0:5, 45:49, 0] = 255
    img[0:5, 0:5, 0] = 255
    mask = img[:, :, 0]
    obj_contour = np.array([[[45,  1]], [[45,  2]], [[45,  3]], [[45,  4]], [[46,  4]], [[47,  4]], [[48,  4]],
                            [[48,  3]], [[48,  2]], [[48,  1]], [[47,  1]], [[46,  1]], [[1,  1]], [[1,  2]],
                            [[1,  3]], [[1,  4]], [[2,  4]], [[3,  4]], [[4,  4]], [[4,  3]], [[4,  2]],
                            [[4,  1]], [[3,  1]], [[2,  1]]], dtype=np.int32)
    # Test with debug = None
    pcv.params.debug = None
    obj_header, obj_data, obj_images = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    assert obj_data[7] == 186


def test_plantcv_analyze_object_longest_axis_2e():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_object_longest_axis_2e")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Create a test image
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    img[10:15, 10:40, 0] = 255
    mask = img[:, :, 0]
    obj_contour = np.array([[[10, 10]], [[10, 11]], [[10, 12]], [[10, 13]], [[10, 14]], [[11, 14]], [[12, 14]],
                            [[13, 14]], [[14, 14]], [[15, 14]], [[16, 14]], [[17, 14]], [[18, 14]], [[19, 14]],
                            [[20, 14]], [[21, 14]], [[22, 14]], [[23, 14]], [[24, 14]], [[25, 14]], [[26, 14]],
                            [[27, 14]], [[28, 14]], [[29, 14]], [[30, 14]], [[31, 14]], [[32, 14]], [[33, 14]],
                            [[34, 14]], [[35, 14]], [[36, 14]], [[37, 14]], [[38, 14]], [[39, 14]], [[39, 13]],
                            [[39, 12]], [[39, 11]], [[39, 10]], [[38, 10]], [[37, 10]], [[36, 10]], [[35, 10]],
                            [[34, 10]], [[33, 10]], [[32, 10]], [[31, 10]], [[30, 10]], [[29, 10]], [[28, 10]],
                            [[27, 10]], [[26, 10]], [[25, 10]], [[24, 10]], [[23, 10]], [[22, 10]], [[21, 10]],
                            [[20, 10]], [[19, 10]], [[18, 10]], [[17, 10]], [[16, 10]], [[15, 10]], [[14, 10]],
                            [[13, 10]], [[12, 10]], [[11, 10]]], dtype=np.int32)
    # Test with debug = None
    pcv.params.debug = None
    obj_header, obj_data, obj_images = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    assert obj_data[7] == 141


def test_plantcv_analyze_object_small_contour():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_object_small_contour")
    os.mkdir(cache_dir)
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    obj_contour = [np.array([[[0, 0]], [[0, 50]], [[50, 50]], [[50, 0]]], dtype=np.int32)]
    # Test with debug = None
    pcv.params.debug = None
    obj_header, obj_data, obj_images = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    assert obj_data is None


def test_plantcv_apply_mask_white():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_apply_mask_white")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.apply_mask(rgb_img=img, mask=mask, mask_color="white")
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.apply_mask(rgb_img=img, mask=mask, mask_color="white")
    # Test with debug = None
    pcv.params.debug = None
    masked_img = pcv.apply_mask(rgb_img=img, mask=mask, mask_color="white")
    assert all([i == j] for i, j in zip(np.shape(masked_img), TEST_COLOR_DIM))


def test_plantcv_apply_mask_black():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_apply_mask_black")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.apply_mask(rgb_img=img, mask=mask, mask_color="black")
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.apply_mask(rgb_img=img, mask=mask, mask_color="black")
    # Test with debug = None
    pcv.params.debug = None
    masked_img = pcv.apply_mask(rgb_img=img, mask=mask, mask_color="black")
    assert all([i == j] for i, j in zip(np.shape(masked_img), TEST_COLOR_DIM))


def test_plantcv_apply_mask_bad_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    with pytest.raises(RuntimeError):
        pcv.params.debug = "plot"
        _ = pcv.apply_mask(rgb_img=img, mask=mask, mask_color="wite")


def test_plantcv_auto_crop():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_auto_crop")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INTPUT_MULTI), -1)
    contours = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_OBJECT), encoding="latin1")
    roi_contours = contours['arr_0']
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.auto_crop(img=img1, objects=roi_contours[1], padding_x=20, padding_y=20, color='black')
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.auto_crop(img=img1, objects=roi_contours[1], padding_x=20, padding_y=20, color='black')
    # Test with debug = None
    pcv.params.debug = None
    cropped = pcv.auto_crop(img=img1, objects=roi_contours[1], padding_x=20, padding_y=20, color='black')
    x, y, z = np.shape(img1)
    x1, y1, z1 = np.shape(cropped)
    assert x > x1


def test_plantcv_auto_crop_grayscale_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_auto_crop_grayscale_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INTPUT_MULTI), -1)
    gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
    contours = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_OBJECT), encoding="latin1")
    roi_contours = contours['arr_0']
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    cropped = pcv.auto_crop(img=gray_img, objects=roi_contours[1], padding_x=20, padding_y=20, color='white')
    x, y = np.shape(gray_img)
    x1, y1 = np.shape(cropped)
    assert x > x1


def test_plantcv_canny_edge_detect():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_canny_edge_detect")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.canny_edge_detect(img=rgb_img, mask=mask, mask_color='white')
    _ = pcv.canny_edge_detect(img=img, mask=mask, mask_color='black')
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.canny_edge_detect(img=img, thickness=2)
    _ = pcv.canny_edge_detect(img=img)
    # Test with debug = None
    pcv.params.debug = None
    edge_img = pcv.canny_edge_detect(img=img)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(edge_img), TEST_BINARY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(edge_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_canny_edge_detect_bad_input():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_canny_edge_detect")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.canny_edge_detect(img=img, mask=mask)



def test_plantcv_cluster_contours():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_cluster_contours")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INTPUT_MULTI), -1)
    roi_objects = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_OBJECT), encoding="latin1")
    hierachy = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_HIERARCHY), encoding="latin1")
    objs = roi_objects['arr_0']
    obj_hierarchy = hierachy['arr_0']
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.cluster_contours(img=img1, roi_objects=objs, roi_obj_hierarchy=obj_hierarchy, nrow=4, ncol=6)
    _ = pcv.cluster_contours(img=img1, roi_objects=objs, roi_obj_hierarchy=obj_hierarchy)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.cluster_contours(img=img1, roi_objects=objs, roi_obj_hierarchy=obj_hierarchy, nrow=4, ncol=6)
    # Test with debug = None
    pcv.params.debug = None
    clusters_i, contours, hierachy = pcv.cluster_contours(img=img1, roi_objects=objs, roi_obj_hierarchy=obj_hierarchy,
                                                          nrow=4, ncol=6)
    lenori = len(objs)
    lenclust = len(clusters_i)
    assert lenori > lenclust


def test_plantcv_cluster_contours_grayscale_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_cluster_contours_grayscale_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INTPUT_MULTI), 0)
    roi_objects = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_OBJECT), encoding="latin1")
    hierachy = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_HIERARCHY), encoding="latin1")
    objs = roi_objects['arr_0']
    obj_hierarchy = hierachy['arr_0']
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.cluster_contours(img=img1, roi_objects=objs, roi_obj_hierarchy=obj_hierarchy, nrow=4, ncol=6)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.cluster_contours(img=img1, roi_objects=objs, roi_obj_hierarchy=obj_hierarchy, nrow=4, ncol=6)
    # Test with debug = None
    pcv.params.debug = None
    clusters_i, contours, hierachy = pcv.cluster_contours(img=img1, roi_objects=objs, roi_obj_hierarchy=obj_hierarchy,
                                                          nrow=4, ncol=6)
    lenori = len(objs)
    lenclust = len(clusters_i)
    assert lenori > lenclust


def test_plantcv_cluster_contours_splitimg():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_cluster_contours_splitimg")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INTPUT_MULTI), -1)
    contours = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_CONTOUR), encoding="latin1")
    clusters = np.load(os.path.join(TEST_DATA, TEST_INPUT_ClUSTER_CONTOUR), encoding="latin1")
    hierachy = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_HIERARCHY), encoding="latin1")
    cluster_names = os.path.join(TEST_DATA, TEST_INPUT_GENOTXT)
    cluster_names_too_many = os.path.join(TEST_DATA, TEST_INPUT_GENOTXT_TOO_MANY)
    roi_contours = contours['arr_0']
    cluster_contours = clusters['arr_0']
    obj_hierarchy = hierachy['arr_0']
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.cluster_contour_splitimg(rgb_img=img1, grouped_contour_indexes=cluster_contours, contours=roi_contours,
                                     hierarchy=obj_hierarchy, outdir=cache_dir, file=None, filenames=None)
    _ = pcv.cluster_contour_splitimg(rgb_img=img1, grouped_contour_indexes=cluster_contours, contours=roi_contours,
                                     hierarchy=obj_hierarchy, outdir=cache_dir, file='multi', filenames=None)

    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.cluster_contour_splitimg(rgb_img=img1, grouped_contour_indexes=cluster_contours, contours=roi_contours,
                                     hierarchy=obj_hierarchy, outdir=None, file=None, filenames=cluster_names)
    _ = pcv.cluster_contour_splitimg(rgb_img=img1, grouped_contour_indexes=cluster_contours, contours=roi_contours,
                                     hierarchy=obj_hierarchy, outdir=None, file=None, filenames=cluster_names_too_many)
    # Test with debug = None
    pcv.params.debug = None
    output_path = pcv.cluster_contour_splitimg(rgb_img=img1, grouped_contour_indexes=cluster_contours,
                                               contours=roi_contours, hierarchy=obj_hierarchy, outdir=None, file=None,
                                               filenames=None)
    assert len(output_path) != 0


def test_plantcv_color_palette():
    # Collect assertions
    truths = []

    # Return one random color
    colors = pcv.color_palette(1)
    # Colors should be a list of length 1, containing a tuple of length 3
    truths.append(len(colors) == 1)
    truths.append(len(colors[0]) == 3)

    # Return ten random colors
    colors = pcv.color_palette(10)
    # Colors should be a list of length 10
    truths.append(len(colors) == 10)
    # All of these should be true for the function to pass testing.
    assert (all(truths))


def test_plantcv_crop_position_mask():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_crop_position_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    nir, path1, filename1 = pcv.readimage(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
    mask_three_channel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK))
    mask_resize = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK_RESIZE), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="top", h_pos="right")
    _ = pcv.crop_position_mask(nir, mask_resize, x=40, y=3, v_pos="top", h_pos="right")
    _ = pcv.crop_position_mask(nir, mask_three_channel, x=40, y=3, v_pos="top", h_pos="right")
    # Test with debug = "print" with bottom
    _ = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="bottom", h_pos="left")
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="top", h_pos="right")
    # Test with debug = "plot" with bottom
    _ = pcv.crop_position_mask(nir, mask, x=45, y=2, v_pos="bottom", h_pos="left")
    # Test with debug = None
    pcv.params.debug = None
    newmask = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="top", h_pos="right")
    assert np.sum(newmask) == 641517


def test_plantcv_crop_position_mask_color():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_crop_position_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    nir, path1, filename1 = pcv.readimage(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
    mask_resize = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK_RESIZE))
    mask_non_binary = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK))
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="top", h_pos="right")
    # Test with debug = "print" with bottom
    _ = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="bottom", h_pos="left")
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="top", h_pos="right")
    # Test with debug = "plot" with bottom
    _ = pcv.crop_position_mask(nir, mask, x=45, y=2, v_pos="bottom", h_pos="left")
    _ = pcv.crop_position_mask(nir, mask_non_binary, x=45, y=2, v_pos="bottom", h_pos="left")
    _ = pcv.crop_position_mask(nir, mask_non_binary, x=45, y=2, v_pos="top", h_pos="left")
    _ = pcv.crop_position_mask(nir, mask_non_binary, x=45, y=2, v_pos="bottom", h_pos="right")
    _ = pcv.crop_position_mask(nir, mask_resize, x=45, y=2, v_pos="top", h_pos="left")

    # Test with debug = None
    pcv.params.debug = None
    newmask = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="top", h_pos="right")
    assert np.sum(newmask) == 641517


def test_plantcv_crop_position_mask_bad_input_x():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_crop_position_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
    # Read in test data
    nir, path1, filename1 = pcv.readimage(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK))
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.crop_position_mask(nir, mask, x=-1, y=-1, v_pos="top", h_pos="right")


def test_plantcv_dilate():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_dilate")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.dilate(gray_img=img, kernel=5, i=1)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.dilate(gray_img=img, kernel=5, i=1)
    # Test with debug = None
    pcv.params.debug = None
    dilate_img = pcv.dilate(gray_img=img, kernel=5, i=1)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(dilate_img), TEST_BINARY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(dilate_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_erode():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_erode")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.erode(gray_img=img, kernel=5, i=1)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.erode(gray_img=img, kernel=5, i=1)
    # Test with debug = None
    pcv.params.debug = None
    erode_img = pcv.erode(gray_img=img, kernel=5, i=1)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(erode_img), TEST_BINARY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(erode_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_distance_transform():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_distance_transform")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_CROPPED_MASK), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.distance_transform(bin_img=mask, distance_type=1, mask_size=3)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.distance_transform(bin_img=mask, distance_type=1, mask_size=3)
    # Test with debug = None
    pcv.params.debug = None
    distance_transform_img = pcv.distance_transform(bin_img=mask, distance_type=1, mask_size=3)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(distance_transform_img), np.shape(mask)))


def test_plantcv_fatal_error():
    # Verify that the fatal_error function raises a RuntimeError
    with pytest.raises(RuntimeError):
        pcv.fatal_error("Test error")


def test_plantcv_fill():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_fill")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.fill(bin_img=img, size=63632)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.fill(bin_img=img, size=63632)
    # Test with debug = None
    pcv.params.debug = None
    fill_img = pcv.fill(bin_img=img, size=63632)
    # Assert that the output image has the dimensions of the input image
    # assert all([i == j] for i, j in zip(np.shape(fill_img), TEST_BINARY_DIM))
    assert np.sum(fill_img) == 0


def test_plantcv_fill_bad_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_fill_bad_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.fill(bin_img=img, size=1)


def test_plantcv_find_objects():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_find_objects")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.find_objects(img=img, mask=mask)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.find_objects(img=img, mask=mask)
    # Test with debug = None
    pcv.params.debug = None
    contours, hierarchy = pcv.find_objects(img=img, mask=mask)
    # Assert the correct number of contours are found
    if cv2.__version__[0] == '2':
        assert len(contours) == 2
    else:
        assert len(contours) == 2


def test_plantcv_find_objects_grayscale_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_find_objects_grayscale_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    contours, hierarchy = pcv.find_objects(img=img, mask=mask)
    # Assert the correct number of contours are found
    if cv2.__version__[0] == '2':
        assert len(contours) == 2
    else:
        assert len(contours) == 2


def test_plantcv_flip():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_flip")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    img_binary = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.flip(img=img, direction="horizontal")
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.flip(img=img, direction="vertical")
    _ = pcv.flip(img=img_binary, direction="vertical")
    # Test with debug = None
    pcv.params.debug = None
    flipped_img = pcv.flip(img=img, direction="horizontal")
    assert all([i == j] for i, j in zip(np.shape(flipped_img), TEST_COLOR_DIM))


def test_plantcv_flip_bad_input():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.flip(img=img, direction="vert")


def test_plantcv_fluor_fvfm():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_fluor_fvfm")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    filename = os.path.join(cache_dir, 'plantcv_fvfm_hist.jpg')
    # Read in test data
    fdark = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FDARK), -1)
    fmin = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMIN), -1)
    fmax = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMAX), -1)
    fmask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMASK), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    outfile = os.path.join(cache_dir, TEST_INPUT_FMAX)
    _ = pcv.fluor_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=fmask, bins=1000)
    _, _, analysis_images = pcv.fluor_fvfm(fdark=fdark+3000, fmin=fmin, fmax=fmax, mask=fmask, bins=1000)
    # Test under updated print and plot function
    hist_img = analysis_images[1]
    pcv.print_image(hist_img, filename)
    pcv.plot_image(hist_img)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.fluor_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=fmask, bins=1000)
    # Test with debug = None
    pcv.params.debug = None
    fvfm_header, fvfm_data, fvfm_images = pcv.fluor_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=fmask,
                                                         bins=1000)
    assert fvfm_data[4] > 0.66


def test_plantcv_fluor_fvfm_bad_input():
    fdark = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    fmin = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMIN), -1)
    fmax = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMAX), -1)
    fmask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMASK), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.fluor_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=fmask, bins=1000)


def test_plantcv_gaussian_blur():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_gaussian_blur")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img_color = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.gaussian_blur(img=img, ksize=(51, 51), sigmax=0, sigmay=None)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.gaussian_blur(img=img, ksize=(51, 51), sigmax=0, sigmay=None)
    _ = pcv.gaussian_blur(img=img_color, ksize=(51, 51), sigmax=0, sigmay=None)
    # Test with debug = None
    pcv.params.debug = None
    gaussian_img = pcv.gaussian_blur(img=img, ksize=(51, 51), sigmax=0, sigmay=None)
    imgavg = np.average(img)
    gavg = np.average(gaussian_img)
    assert gavg != imgavg


def test_plantcv_get_nir_sv():
    nirpath = pcv.get_nir(TEST_DATA, TEST_VIS)
    nirpath1 = os.path.join(TEST_DATA, TEST_NIR)
    assert nirpath == nirpath1


def test_plantcv_get_nir_tv():
    nirpath = pcv.get_nir(TEST_DATA, TEST_VIS_TV)
    nirpath1 = os.path.join(TEST_DATA, TEST_NIR_TV)
    assert nirpath == nirpath1


def test_plantcv_hist_equalization():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hist_equalization")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.hist_equalization(gray_img=img)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.hist_equalization(gray_img=img)
    # Test with debug = None
    pcv.params.debug = None
    hist = pcv.hist_equalization(gray_img=img)
    histavg = np.average(hist)
    imgavg = np.average(img)
    assert histavg != imgavg


def test_plantcv_hist_equalization_bad_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hist_equalization_bad_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), 1)
    # Test with debug = None
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.hist_equalization(gray_img=img)


def test_plantcv_image_add():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_image_add")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.image_add(gray_img1=img1, gray_img2=img2)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.image_add(gray_img1=img1, gray_img2=img2)
    # Test with debug = None
    pcv.params.debug = None
    added_img = pcv.image_add(gray_img1=img1, gray_img2=img2)
    assert all([i == j] for i, j in zip(np.shape(added_img), TEST_BINARY_DIM))


def test_plantcv_image_subtract():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_image_sub")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # read in images
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    # Test with debug = "print"
    pcv.params.debug = 'print'
    _ = pcv.image_subtract(img1, img2)
    # Test with debug = "plot"
    pcv.params.debug = 'plot'
    _ = pcv.image_subtract(img1, img2)
    # Test with debug = None
    pcv.params.debug = None
    new_img = pcv.image_subtract(img1, img2)
    assert np.array_equal(new_img, np.zeros(np.shape(new_img), np.uint8))


def test_plantcv_image_subtract_fail():
    # read in images
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY))
    # test
    with pytest.raises(RuntimeError):
        _ = pcv.image_subtract(img1, img2)


def test_plantcv_invert():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_invert")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.invert(gray_img=img)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.invert(gray_img=img)
    # Test with debug = None
    pcv.params.debug = None
    inverted_img = pcv.invert(gray_img=img)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(inverted_img), TEST_BINARY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(inverted_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_landmark_reference_pt_dist():
    points_rescaled = [(0.0139, 0.2569), (0.2361, 0.2917), (0.3542, 0.3819), (0.3542, 0.4167), (0.375, 0.4236),
                       (0.7431, 0.3681), (0.8958, 0.3542), (0.9931, 0.3125), (0.1667, 0.5139), (0.4583, 0.8889),
                       (0.4931, 0.5903), (0.3889, 0.5694), (0.4792, 0.4306), (0.2083, 0.5417), (0.3194, 0.5278),
                       (0.3889, 0.375), (0.3681, 0.3472), (0.2361, 0.0139), (0.5417, 0.2292), (0.7708, 0.3472),
                       (0.6458, 0.3472), (0.6389, 0.5208), (0.6458, 0.625)]
    centroid_rescaled = (0.4685, 0.4945)
    bottomline_rescaled = (0.4685, 0.2569)
    _ = pcv.landmark_reference_pt_dist(points_r=[], centroid_r=('a', 'b'), bline_r=(0, 0))
    _ = pcv.landmark_reference_pt_dist(points_r=[(10, 1000)], centroid_r=(10, 10), bline_r=(10, 10))
    _ = pcv.landmark_reference_pt_dist(points_r=[], centroid_r=(0, 0), bline_r=(0, 0))
    results = pcv.landmark_reference_pt_dist(points_r=points_rescaled, centroid_r=centroid_rescaled,
                                             bline_r=bottomline_rescaled)
    assert len(results) == 8


def test_plantcv_laplace_filter():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_laplace_filter")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.laplace_filter(gray_img=img, k=1, scale=1)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.laplace_filter(gray_img=img, k=1, scale=1)
    # Test with debug = None
    pcv.params.debug = None
    lp_img = pcv.laplace_filter(gray_img=img, k=1, scale=1)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(lp_img), TEST_GRAY_DIM))


def test_plantcv_logical_and():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_logical_and")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.logical_and(bin_img1=img1, bin_img2=img2)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.logical_and(bin_img1=img1, bin_img2=img2)
    # Test with debug = None
    pcv.params.debug = None
    and_img = pcv.logical_and(bin_img1=img1, bin_img2=img2)
    assert all([i == j] for i, j in zip(np.shape(and_img), TEST_BINARY_DIM))


def test_plantcv_logical_or():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_logical_or")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.logical_or(bin_img1=img1, bin_img2=img2)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.logical_or(bin_img1=img1, bin_img2=img2)
    # Test with debug = None
    pcv.params.debug = None
    or_img = pcv.logical_or(bin_img1=img1, bin_img2=img2)
    assert all([i == j] for i, j in zip(np.shape(or_img), TEST_BINARY_DIM))


def test_plantcv_logical_xor():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_logical_xor")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.logical_xor(bin_img1=img1, bin_img2=img2)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.logical_xor(bin_img1=img1, bin_img2=img2)
    # Test with debug = None
    pcv.params.debug = None
    xor_img = pcv.logical_xor(bin_img1=img1, bin_img2=img2)
    assert all([i == j] for i, j in zip(np.shape(xor_img), TEST_BINARY_DIM))


def test_plantcv_median_blur():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_median_blur")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.median_blur(gray_img=img, ksize=5)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.median_blur(gray_img=img, ksize=5)
    # Test with debug = None
    pcv.params.debug = None
    blur_img = pcv.median_blur(gray_img=img, ksize=5)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(blur_img), TEST_BINARY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(blur_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_median_blur_bad_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_median_blur_bad_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.median_blur(img, 5.)


def test_plantcv_naive_bayes_classifier():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_naive_bayes_classifier")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.naive_bayes_classifier(rgb_img=img, pdf_file=os.path.join(TEST_DATA, TEST_PDFS))
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.naive_bayes_classifier(rgb_img=img, pdf_file=os.path.join(TEST_DATA, TEST_PDFS))
    # Test with debug = None
    pcv.params.debug = None
    mask = pcv.naive_bayes_classifier(rgb_img=img, pdf_file=os.path.join(TEST_DATA, TEST_PDFS))

    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(mask), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(mask), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_naive_bayes_classifier_bad_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.naive_bayes_classifier(rgb_img=img, pdf_file=os.path.join(TEST_DATA, TEST_PDFS_BAD))


def test_plantcv_object_composition():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_object_composition")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS1), encoding="latin1")
    object_contours = contours_npz['arr_0']
    object_hierarchy = contours_npz['arr_1']
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.object_composition(img=img, contours=object_contours, hierarchy=object_hierarchy)
    _ = pcv.object_composition(img=img, contours=[], hierarchy=object_hierarchy)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.object_composition(img=img, contours=object_contours, hierarchy=object_hierarchy)
    # Test with debug = None
    pcv.params.debug = None
    contours, mask = pcv.object_composition(img=img, contours=object_contours, hierarchy=object_hierarchy)
    # Assert that the objects have been combined
    contour_shape = np.shape(contours)  # type: tuple
    assert contour_shape[1] == 1


def test_plantcv_object_composition_grayscale_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_object_composition_grayscale_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS1), encoding="latin1")
    object_contours = contours_npz['arr_0']
    object_hierarchy = contours_npz['arr_1']
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    contours, mask = pcv.object_composition(img=img, contours=object_contours, hierarchy=object_hierarchy)
    # Assert that the objects have been combined
    contour_shape = np.shape(contours)  # type: tuple
    assert contour_shape[1] == 1


def test_plantcv_output_mask():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_output_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    img_color = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.output_mask(img=img, mask=mask, filename='test.png', outdir=cache_dir, mask_only=False)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.output_mask(img=img, mask=mask, filename='test.png', outdir=cache_dir, mask_only=False)
    _ = pcv.output_mask(img=img_color, mask=mask, filename='test.png', mask_only=False)
    # Test with debug = None
    pcv.params.debug = None
    imgpath, maskpath, analysis_images = pcv.output_mask(img=img, mask=mask, filename='test.png', outdir=cache_dir,
                                                         mask_only=False)
    assert all([os.path.exists(imgpath) is True, os.path.exists(maskpath) is True])


def test_plantcv_output_mask_true():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_output_mask")
    pcv.params.debug_outdir = cache_dir
    os.mkdir(cache_dir)
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    img_color = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.output_mask(img=img, mask=mask, filename='test.png', outdir=cache_dir, mask_only=True)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.output_mask(img=img_color, mask=mask, filename='test.png', outdir=cache_dir, mask_only=True)
    pcv.params.debug = None
    imgpath, maskpath, analysis_images = pcv.output_mask(img=img, mask=mask, filename='test.png', outdir=cache_dir,
                                                        mask_only=False)
    assert all([os.path.exists(imgpath) is True, os.path.exists(maskpath) is True])


def test_plantcv_plot_hist():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_plot_hist")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Test in 16-bit image mode
    img16bit = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK), -1)
    _ = pcv.plot_hist(img=img16bit, name=os.path.join(cache_dir, "hist_nir_uint16"))
    # Test in 8-bit image mode
    img8bit = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), -1)
    bins, hist = pcv.plot_hist(img=img8bit, name=os.path.join(cache_dir, "hist_rgb_uint8"))
    assert len(hist) == 256


def test_plantcv_plot_image_matplotlib_input():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_pseudocolor")
    os.mkdir(cache_dir)
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    pimg = pcv.pseudocolor(gray_img=img, mask=mask, min_value=10, max_value=200, path=cache_dir)
    with pytest.raises(RuntimeError):
        pcv.plot_image(pimg)

def test_plantcv_print_image():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_print_image")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img, path, img_name = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    filename = os.path.join(cache_dir, 'plantcv_print_image.jpg')
    pcv.print_image(img=img, filename=filename)
    # Assert that the file was created
    assert os.path.exists(filename) is True


def test_plantcv_print_image_bad_type():
    with pytest.raises(RuntimeError):
        pcv.print_image(img=[], filename="/dev/null")


def test_plantcv_print_results():
    header = ['field1', 'field2', 'field3']
    data = ['value1', 'value2', 'value3']
    pcv.print_results(filename='not_used', header=header, data=data)


def test_plantcv_pseudocolor():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_pseudocolor")
    os.mkdir(cache_dir)
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    filename = os.path.join(cache_dir, 'plantcv_pseudo_image.jpg')
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.pseudocolor(gray_img=img, mask=None, path=cache_dir)
    pimg = pcv.pseudocolor(gray_img=img, mask=mask, min_value=10, max_value=200, path=cache_dir)
    pcv.print_image(pimg, filename)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.pseudocolor(gray_img=img, mask=mask)
    _ = pcv.pseudocolor(gray_img=img, mask=None)
    _ = pcv.pseudocolor(gray_img=img, mask=mask, obj=obj_contour, axes=False, path=cache_dir)
    _ = pcv.pseudocolor(gray_img=img, mask=None, axes=False, path=cache_dir)
    # Test with debug = None
    pcv.params.debug = None
    pseudo_img = pcv.pseudocolor(gray_img=img, mask=mask)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(pseudo_img), TEST_BINARY_DIM)):
        assert 1
    else:
        assert 0


def test_plantcv_pseudocolor_bad_input():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_pseudocolor")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        _ = pcv.pseudocolor(gray_img=img)


def test_plantcv_readimage_native():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_readimage")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    pcv.params.debug = None
    img, path, img_name = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Assert that the image name returned equals the name of the input image
    # Assert that the path of the image returned equals the path of the input image
    # Assert that the dimensions of the returned image equals the expected dimensions
    if img_name == TEST_INPUT_COLOR and path == TEST_DATA:
        if all([i == j] for i, j in zip(np.shape(img), TEST_COLOR_DIM)):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_readimage_grayscale():
    pcv.params.debug = None
    img, path, img_name = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_GRAY), mode="gray")
    assert len(np.shape(img)) == 2


def test_plantcv_readimage_rgb():
    pcv.params.debug = None
    img, path, img_name = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_GRAY), mode="rgb")
    assert len(np.shape(img)) == 3


def test_plantcv_readimage_bad_file():
    with pytest.raises(RuntimeError):
        _ = pcv.readimage(filename=TEST_INPUT_COLOR)


def test_plantcv_readbayer_default_bg():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_readbayer_default_bg")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Test with debug = "print"
    pcv.params.debug = "print"
    _, _, _ = pcv.readbayer(filename=os.path.join(TEST_DATA, TEST_INPUT_BAYER),
                            bayerpattern="BG", alg="default")
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    img, path, img_name = pcv.readbayer(filename=os.path.join(TEST_DATA, TEST_INPUT_BAYER),
                                        bayerpattern="BG", alg="default")
    assert all([i == j] for i, j in zip(np.shape(img), (335, 400, 3)))


def test_plantcv_readbayer_default_gb():
    # Test with debug = None
    pcv.params.debug = None
    img, path, img_name = pcv.readbayer(filename=os.path.join(TEST_DATA, TEST_INPUT_BAYER),
                                        bayerpattern="GB", alg="default")
    assert all([i == j] for i, j in zip(np.shape(img), (335, 400, 3)))


def test_plantcv_readbayer_default_rg():
    # Test with debug = None
    pcv.params.debug = None
    img, path, img_name = pcv.readbayer(filename=os.path.join(TEST_DATA, TEST_INPUT_BAYER),
                                        bayerpattern="RG", alg="default")
    assert all([i == j] for i, j in zip(np.shape(img), (335, 400, 3)))


def test_plantcv_readbayer_default_gr():
    # Test with debug = None
    pcv.params.debug = None
    img, path, img_name = pcv.readbayer(filename=os.path.join(TEST_DATA, TEST_INPUT_BAYER),
                                        bayerpattern="GR", alg="default")
    assert all([i == j] for i, j in zip(np.shape(img), (335, 400, 3)))


def test_plantcv_readbayer_edgeaware_bg():
    # Test with debug = None
    pcv.params.debug = None
    img, path, img_name = pcv.readbayer(filename=os.path.join(TEST_DATA, TEST_INPUT_BAYER),
                                        bayerpattern="BG", alg="edgeaware")
    assert all([i == j] for i, j in zip(np.shape(img), (335, 400, 3)))


def test_plantcv_readbayer_edgeaware_gb():
    # Test with debug = None
    pcv.params.debug = None
    img, path, img_name = pcv.readbayer(filename=os.path.join(TEST_DATA, TEST_INPUT_BAYER),
                                        bayerpattern="GB", alg="edgeaware")
    assert all([i == j] for i, j in zip(np.shape(img), (335, 400, 3)))


def test_plantcv_readbayer_edgeaware_rg():
    # Test with debug = None
    pcv.params.debug = None
    img, path, img_name = pcv.readbayer(filename=os.path.join(TEST_DATA, TEST_INPUT_BAYER),
                                        bayerpattern="RG", alg="edgeaware")
    assert all([i == j] for i, j in zip(np.shape(img), (335, 400, 3)))


def test_plantcv_readbayer_edgeaware_gr():
    # Test with debug = None
    pcv.params.debug = None
    img, path, img_name = pcv.readbayer(filename=os.path.join(TEST_DATA, TEST_INPUT_BAYER),
                                        bayerpattern="GR", alg="edgeaware")
    assert all([i == j] for i, j in zip(np.shape(img), (335, 400, 3)))


def test_plantcv_readbayer_variablenumbergradients_bg():
    # Test with debug = None
    pcv.params.debug = None
    img, path, img_name = pcv.readbayer(filename=os.path.join(TEST_DATA, TEST_INPUT_BAYER),
                                        bayerpattern="BG", alg="variablenumbergradients")
    assert all([i == j] for i, j in zip(np.shape(img), (335, 400, 3)))


def test_plantcv_readbayer_variablenumbergradients_gb():
    # Test with debug = None
    pcv.params.debug = None
    img, path, img_name = pcv.readbayer(filename=os.path.join(TEST_DATA, TEST_INPUT_BAYER),
                                        bayerpattern="GB", alg="variablenumbergradients")
    assert all([i == j] for i, j in zip(np.shape(img), (335, 400, 3)))


def test_plantcv_readbayer_variablenumbergradients_rg():
    # Test with debug = None
    pcv.params.debug = None
    img, path, img_name = pcv.readbayer(filename=os.path.join(TEST_DATA, TEST_INPUT_BAYER),
                                        bayerpattern="RG", alg="variablenumbergradients")
    assert all([i == j] for i, j in zip(np.shape(img), (335, 400, 3)))


def test_plantcv_readbayer_variablenumbergradients_gr():
    # Test with debug = None
    pcv.params.debug = None
    img, path, img_name = pcv.readbayer(filename=os.path.join(TEST_DATA, TEST_INPUT_BAYER),
                                        bayerpattern="GR", alg="variablenumbergradients")
    assert all([i == j] for i, j in zip(np.shape(img), (335, 400, 3)))


def test_plantcv_readbayer_default_bad_input():
    # Test with debug = None
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _, _, _ = pcv.readbayer(filename=os.path.join(TEST_DATA, "no-image.png"), bayerpattern="GR", alg="default")


def test_plantcv_rectangle_mask():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_rectangle_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    img_color = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.rectangle_mask(img=img, p1=(0, 0), p2=(2454, 2056), color="white")
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.rectangle_mask(img=img_color, p1=(0, 0), p2=(2454, 2056), color="gray")
    # Test with debug = None
    pcv.params.debug = None
    masked, hist, contour, heir = pcv.rectangle_mask(img=img, p1=(0, 0), p2=(2454, 2056), color="black")
    maskedsum = np.sum(masked)
    imgsum = np.sum(img)
    assert maskedsum < imgsum


def test_plantcv_report_size_marker_detect():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_report_size_marker_detect")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MARKER), -1)
    # ROI contour
    roi_contour = [np.array([[[3550, 850]], [[3550, 1349]], [[4049, 1349]], [[4049, 850]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)

    # Test with debug = "print"
    pcv.params.debug = "print"
    outfile = os.path.join(cache_dir, TEST_INPUT_MARKER)
    _ = pcv.report_size_marker_area(img=img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy, marker='detect',
                                    objcolor='light', thresh_channel='s', thresh=120, filename=outfile)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.report_size_marker_area(img=img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy, marker='detect',
                                    objcolor='light', thresh_channel='s', thresh=120, filename=False)
    # Test with debug = None
    pcv.params.debug = None
    marker_header, marker_data, images = pcv.report_size_marker_area(img=img, roi_contour=roi_contour,
                                                                     roi_hierarchy=roi_hierarchy, marker='detect',
                                                                     objcolor='light', thresh_channel='s', thresh=120,
                                                                     filename=False)
    assert marker_data[1] > 100


def test_plantcv_report_size_marker_define():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MARKER), -1)
    # ROI contour
    roi_contour = [np.array([[[3550, 850]], [[3550, 1349]], [[4049, 1349]], [[4049, 850]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)

    # Test with debug = None
    pcv.params.debug = None
    marker_header, marker_data, images = pcv.report_size_marker_area(img=img, roi_contour=roi_contour,
                                                                     roi_hierarchy=roi_hierarchy, marker='define',
                                                                     objcolor='light', thresh_channel='s', thresh=120,
                                                                     filename=False)
    assert marker_data[1] == 250000


def test_plantcv_report_size_marker_grayscale_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # ROI contour
    roi_contour = [np.array([[[0, 0]], [[0, 49]], [[49, 49]], [[49, 0]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)

    # Test with debug = None
    pcv.params.debug = None
    marker_header, marker_data, images = pcv.report_size_marker_area(img=img, roi_contour=roi_contour,
                                                                     roi_hierarchy=roi_hierarchy, marker='define',
                                                                     objcolor='light', thresh_channel='s', thresh=120,
                                                                     filename=False)
    if cv2.__version__[0] == '2':
        assert int(marker_data[1]) == 2401
    else:
        assert marker_data[1] == 2500


def test_plantcv_report_size_marker_bad_marker_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MARKER), -1)
    # ROI contour
    roi_contour = [np.array([[[3550, 850]], [[3550, 1349]], [[4049, 1349]], [[4049, 850]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    with pytest.raises(RuntimeError):
        _ = pcv.report_size_marker_area(img=img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy, marker='none',
                                        objcolor='light', thresh_channel='s', thresh=120, filename=False)


def test_plantcv_report_size_marker_bad_threshold_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MARKER), -1)
    # ROI contour
    roi_contour = [np.array([[[3550, 850]], [[3550, 1349]], [[4049, 1349]], [[4049, 850]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    with pytest.raises(RuntimeError):
        _ = pcv.report_size_marker_area(img=img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy, marker='detect',
                                        objcolor='light', thresh_channel=None, thresh=120, filename=False)


def test_plantcv_resize():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_resize")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.resize(img=img, resize_x=0.5, resize_y=0.5)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.resize(img=img, resize_x=0.5, resize_y=0.5)
    # Test with debug = None
    pcv.params.debug = None
    resized_img = pcv.resize(img=img, resize_x=0.5, resize_y=0.5)
    ix, iy, iz = np.shape(img)
    rx, ry, rz = np.shape(resized_img)
    assert ix > rx


def test_plantcv_resize_bad_inputs():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test for fatal error caused by two negative resize values
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.resize(img=img, resize_x=-1, resize_y=-1)


def test_plantcv_rgb2gray_hsv():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_rgb2gray_hsv")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.rgb2gray_hsv(rgb_img=img, channel="s")
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.rgb2gray_hsv(rgb_img=img, channel="s")
    # Test with debug = None
    pcv.params.debug = None
    s = pcv.rgb2gray_hsv(rgb_img=img, channel="s")
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert all([i == j] for i, j in zip(np.shape(s), TEST_GRAY_DIM))


def test_plantcv_rgb2gray_hsv_bad_input():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.rgb2gray_hsv(rgb_img=img, channel="l")


def test_plantcv_rgb2gray_lab():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_rgb2gray_lab")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.rgb2gray_lab(rgb_img=img, channel='b')
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.rgb2gray_lab(rgb_img=img, channel='b')
    # Test with debug = None
    pcv.params.debug = None
    b = pcv.rgb2gray_lab(rgb_img=img, channel='b')
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert all([i == j] for i, j in zip(np.shape(b), TEST_GRAY_DIM))


def test_plantcv_rgb2gray_lab_bad_input():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.rgb2gray_lab(rgb_img=img, channel="v")


def test_plantcv_rgb2gray():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_rgb2gray")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.rgb2gray(rgb_img=img)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.rgb2gray(rgb_img=img)
    # Test with debug = None
    pcv.params.debug = None
    gray = pcv.rgb2gray(rgb_img=img)
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert all([i == j] for i, j in zip(np.shape(gray), TEST_GRAY_DIM))


def test_plantcv_roi_objects():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_roi_objects")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    roi_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_ROI), encoding="latin1")
    roi_contour = roi_npz['arr_0']
    roi_hierarchy = roi_npz['arr_1']
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS1), encoding="latin1")
    object_contours = contours_npz['arr_0']
    object_hierarchy = contours_npz['arr_1']
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.roi_objects(img=img, roi_type="partial", roi_contour=roi_contour, roi_hierarchy=roi_hierarchy,
                        object_contour=object_contours, obj_hierarchy=object_hierarchy)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.roi_objects(img=img, roi_type="partial", roi_contour=roi_contour, roi_hierarchy=roi_hierarchy,
                        object_contour=object_contours, obj_hierarchy=object_hierarchy)
    # Test with debug = None and roi_type = cutto
    pcv.params.debug = None
    _ = pcv.roi_objects(img=img, roi_type="cutto", roi_contour=roi_contour, roi_hierarchy=roi_hierarchy,
                        object_contour=object_contours, obj_hierarchy=object_hierarchy)
    # Test with debug = None
    kept_contours, kept_hierarchy, mask, area = pcv.roi_objects(img=img, roi_type="partial", roi_contour=roi_contour,
                                                                roi_hierarchy=roi_hierarchy,
                                                                object_contour=object_contours,
                                                                obj_hierarchy=object_hierarchy)
    # Assert that the contours were filtered as expected
    assert len(kept_contours) == 1046


def test_plantcv_roi_objects_bad_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    roi_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_ROI), encoding="latin1")
    roi_contour = roi_npz['arr_0']
    roi_hierarchy = roi_npz['arr_1']
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS1), encoding="latin1")
    object_contours = contours_npz['arr_0']
    object_hierarchy = contours_npz['arr_1']
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.roi_objects(img=img, roi_type="cut", roi_contour=roi_contour, roi_hierarchy=roi_hierarchy,
                            object_contour=object_contours, obj_hierarchy=object_hierarchy)


def test_plantcv_roi_objects_grayscale_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_roi_objects_grayscale_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    roi_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_ROI), encoding="latin1")
    roi_contour = roi_npz['arr_0']
    roi_hierarchy = roi_npz['arr_1']
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS1), encoding="latin1")
    object_contours = contours_npz['arr_0']
    object_hierarchy = contours_npz['arr_1']
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    kept_contours, kept_hierarchy, mask, area = pcv.roi_objects(img=img, roi_type="partial", roi_contour=roi_contour,
                                                                roi_hierarchy=roi_hierarchy,
                                                                object_contour=object_contours,
                                                                obj_hierarchy=object_hierarchy)
    # Assert that the contours were filtered as expected
    assert len(kept_contours) == 1046


def test_plantcv_rotate():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_rotate_img")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.rotate(img=img, rotation_deg=45, crop=True)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.rotate(img=img, rotation_deg=45, crop=True)
    # Test with debug = None
    pcv.params.debug = None
    rotated = pcv.rotate(img=img, rotation_deg=45, crop=True)
    imgavg = np.average(img)
    rotateavg = np.average(rotated)
    assert rotateavg != imgavg


def test_plantcv_rotate_gray():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.rotate(img=img, rotation_deg=45, crop=False)
    # Test with debug = None
    pcv.params.debug = None
    rotated = pcv.rotate(img=img, rotation_deg=45, crop=False)
    imgavg = np.average(img)
    rotateavg = np.average(rotated)
    assert rotateavg != imgavg


def test_plantcv_scale_features():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_scale_features")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.scale_features(obj=obj_contour, mask=mask, points=TEST_ACUTE_RESULT, boundary_line=50)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.scale_features(obj=obj_contour, mask=mask, points=TEST_ACUTE_RESULT, boundary_line='NA')
    # Test with debug = None
    pcv.params.debug = None
    points_rescaled, centroid_rescaled, bottomline_rescaled = pcv.scale_features(obj=obj_contour, mask=mask,
                                                                                 points=TEST_ACUTE_RESULT,
                                                                                 boundary_line=50)
    assert len(points_rescaled) == 23


def test_plantcv_scale_features_bad_input():
    mask = np.array([])
    obj_contour = np.array([])
    pcv.params.debug = None
    result = pcv.scale_features(obj=obj_contour, mask=mask, points=TEST_ACUTE_RESULT, boundary_line=50)
    assert all([i == j] for i, j in zip(result, [("NA", "NA"), ("NA", "NA"), ("NA", "NA")]))


def test_plantcv_scharr_filter():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_scharr_filter")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    pcv.params.debug = "print"
    # Test with debug = "print"
    _ = pcv.scharr_filter(img=img, dx=1, dy=0, scale=1)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.scharr_filter(img=img, dx=1, dy=0, scale=1)
    # Test with debug = None
    pcv.params.debug = None
    scharr_img = pcv.scharr_filter(img=img, dx=1, dy=0, scale=1)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(scharr_img), TEST_GRAY_DIM))


def test_plantcv_shift_img():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_shift_img")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.shift_img(img=img, number=300, side="top")
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.shift_img(img=img, number=300, side="top")
    # Test with debug = "plot"
    _ = pcv.shift_img(img=img, number=300, side="bottom")
    # Test with debug = "plot"
    _ = pcv.shift_img(img=img, number=300, side="right")
    # Test with debug = "plot"
    _ = pcv.shift_img(img=mask, number=300, side="left")
    # Test with debug = None
    pcv.params.debug = None
    rotated = pcv.shift_img(img=img, number=300, side="top")
    imgavg = np.average(img)
    shiftavg = np.average(rotated)
    assert shiftavg != imgavg


def test_plantcv_shift_img_bad_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _ = pcv.shift_img(img=img, number=-300, side="top")


def test_plantcv_sobel_filter():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_sobel_filter")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.sobel_filter(gray_img=img, dx=1, dy=0, k=1)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.sobel_filter(gray_img=img, dx=1, dy=0, k=1)
    # Test with debug = None
    pcv.params.debug = None
    sobel_img = pcv.sobel_filter(gray_img=img, dx=1, dy=0, k=1)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(sobel_img), TEST_GRAY_DIM))


def test_plantcv_watershed_segmentation():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_watershed_segmentation")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_CROPPED))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_CROPPED_MASK), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    outfile = os.path.join(cache_dir, TEST_INPUT_CROPPED)
    _ = pcv.watershed_segmentation(rgb_img=img, mask=mask, distance=10)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.watershed_segmentation(rgb_img=img, mask=mask, distance=10)
    # Test with debug = None
    pcv.params.debug = None
    watershed_header, watershed_data, images = pcv.watershed_segmentation(rgb_img=img, mask=mask, distance=10)
    if cv2.__version__[0] == '2':
        assert watershed_data[1] > 9
    else:
        assert watershed_data[1] > 9


def test_plantcv_white_balance_gray_16bit():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_white_balance_gray_16bit")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.white_balance(img=img, mode='hist', roi=(5, 5, 80, 80))
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.white_balance(img=img, mode='max', roi=(5, 5, 80, 80))
    # Test without an ROI
    pcv.params.debug = None
    _ = pcv.white_balance(img=img, mode='hist', roi=None)
    # Test with debug = None
    white_balanced = pcv.white_balance(img=img, roi=(5, 5, 80, 80))
    imgavg = np.average(img)
    balancedavg = np.average(white_balanced)
    assert balancedavg != imgavg


def test_plantcv_white_balance_gray_8bit():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_white_balance_gray_8bit")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.white_balance(img=img, mode='hist', roi=(5, 5, 80, 80))
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.white_balance(img=img, mode='max', roi=(5, 5, 80, 80))
    # Test without an ROI
    pcv.params.debug = None
    _ = pcv.white_balance(img=img, mode='hist', roi=None)
    # Test with debug = None
    white_balanced = pcv.white_balance(img=img, roi=(5, 5, 80, 80))
    imgavg = np.average(img)
    balancedavg = np.average(white_balanced)
    assert balancedavg != imgavg


def test_plantcv_white_balance_rgb():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_white_balance_rgb")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MARKER))
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.white_balance(img=img, mode='hist', roi=(5, 5, 80, 80))
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.white_balance(img=img, mode='max', roi=(5, 5, 80, 80))
    # Test without an ROI
    pcv.params.debug = None
    _ = pcv.white_balance(img=img, mode='hist', roi=None)
    # Test with debug = None
    white_balanced = pcv.white_balance(img=img, roi=(5, 5, 80, 80))
    imgavg = np.average(img)
    balancedavg = np.average(white_balanced)
    assert balancedavg != imgavg


def test_plantcv_white_balance_bad_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK), -1)
    # Test with debug = None
    with pytest.raises(RuntimeError):
        pcv.params.debug = "plot"
        _ = pcv.white_balance(img=img, mode='hist', roi=(5, 5, 5, 5, 5))


def test_plantcv_white_balance_bad_input_int():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK), -1)
    # Test with debug = None
    with pytest.raises(RuntimeError):
        pcv.params.debug = "plot"
        _ = pcv.white_balance(img=img, mode='hist', roi=(5., 5, 5, 5))


def test_plantcv_x_axis_pseudolandmarks():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_x_axis_pseudolandmarks_debug")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    pcv.params.debug = "print"
    _ = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    _ = pcv.x_axis_pseudolandmarks(obj=np.array([[0, 0], [0, 0]]), mask=np.array([[0, 0], [0, 0]]), img=img)
    _ = pcv.x_axis_pseudolandmarks(obj=(), mask=mask, img=img)
    # Test with debug = None
    pcv.params.debug = None
    top, bottom, center_v = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    assert all([all([i == j] for i, j in zip(np.shape(top), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(bottom), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(center_v), (20, 1, 2)))])


def test_plantcv_x_axis_pseudolandmarks_small_obj():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL_PLANT))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL_PLANT), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR_SMALL_PLANT), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    # Test with debug = "print"
    pcv.params.debug = "print"
    _, _, _ = pcv.x_axis_pseudolandmarks(obj=[], mask=mask, img=img)
    _, _, _ = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _, _, _ = pcv.x_axis_pseudolandmarks(obj=[], mask=mask, img=img)
    top, bottom, center_v = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    assert all([all([i == j] for i, j in zip(np.shape(top), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(bottom), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(center_v), (20, 1, 2)))])


def test_plantcv_x_axis_pseudolandmarks_bad_input():
    img = np.array([])
    mask = np.array([])
    obj_contour = np.array([])
    pcv.params.debug = None
    result = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    assert all([i == j] for i, j in zip(result, [("NA", "NA"), ("NA", "NA"), ("NA", "NA")]))


def test_plantcv_x_axis_pseudolandmarks_bad_obj_input():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL_PLANT))
    with pytest.raises(RuntimeError):
        _ = pcv.x_axis_pseudolandmarks(obj=np.array([[-2, -2], [-2, -2]]), mask=np.array([[-2, -2], [-2, -2]]), img=img)


def test_plantcv_y_axis_pseudolandmarks():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_y_axis_pseudolandmarks_debug")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    pcv.params.debug = "print"
    _ = pcv.y_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.y_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    _ = pcv.y_axis_pseudolandmarks(obj=[], mask=mask, img=img)
    _ = pcv.y_axis_pseudolandmarks(obj=(), mask=mask, img=img)
    # Test with debug = None
    pcv.params.debug = None
    left, right, center_h = pcv.y_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    assert all([all([i == j] for i, j in zip(np.shape(left), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(right), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(center_h), (20, 1, 2)))])


def test_plantcv_y_axis_pseudolandmarks_small_obj():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL_PLANT))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL_PLANT), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR_SMALL_PLANT), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    # Test with debug = "print"
    pcv.params.debug = "print"
    _, _, _ = pcv.y_axis_pseudolandmarks(obj=[], mask=mask, img=img)
    _, _, _ = pcv.y_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    left, right, center_h = pcv.y_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    assert all([all([i == j] for i, j in zip(np.shape(left), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(right), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(center_h), (20, 1, 2)))])


def test_plantcv_y_axis_pseudolandmarks_bad_input():
    img = np.array([])
    mask = np.array([])
    obj_contour = np.array([])
    pcv.params.debug = None
    result = pcv.y_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    assert all([i == j] for i, j in zip(result, [("NA", "NA"), ("NA", "NA"), ("NA", "NA")]))


def test_plantcv_y_axis_pseudolandmarks_bad_obj_input():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL_PLANT))
    with pytest.raises(RuntimeError):
        _ = pcv.y_axis_pseudolandmarks(obj=np.array([[-2, -2], [-2, -2]]), mask=np.array([[-2, -2], [-2, -2]]), img=img)


def test_plantcv_background_subtraction():
    # List to hold result of all tests.
    truths = []
    fg_img = cv2.imread(os.path.join(TEST_DATA, TEST_FOREGROUND))
    bg_img = cv2.imread(os.path.join(TEST_DATA, TEST_BACKGROUND))
    big_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Testing if background subtraction is actually still working.
    # This should return an array whose sum is greater than one
    pcv.params.debug = None
    fgmask = pcv.background_subtraction(background_image=bg_img, foreground_image=fg_img)
    truths.append(np.sum(fgmask) > 0)
    fgmask = pcv.background_subtraction(background_image=big_img, foreground_image=bg_img)
    truths.append(np.sum(fgmask) > 0)
    # The same foreground subtracted from itself should be 0
    fgmask = pcv.background_subtraction(background_image=fg_img, foreground_image=fg_img)
    truths.append(np.sum(fgmask) == 0)
    # The same background subtracted from itself should be 0
    fgmask = pcv.background_subtraction(background_image=bg_img, foreground_image=bg_img)
    truths.append(np.sum(fgmask) == 0)
    # All of these should be true for the function to pass testing.
    if cv2.__version__[0] == '2':
        assert (all(truths))
    else:
        assert (all(truths))


def test_plantcv_background_subtraction_debug():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_background_subtraction_debug")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # List to hold result of all tests.
    truths = []
    fg_img = cv2.imread(os.path.join(TEST_DATA, TEST_FOREGROUND))
    bg_img = cv2.imread(os.path.join(TEST_DATA, TEST_BACKGROUND))
    # Test with debug = "print"
    pcv.params.debug = "print"
    fgmask = pcv.background_subtraction(background_image=bg_img, foreground_image=fg_img)
    truths.append(np.sum(fgmask) > 0)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    fgmask = pcv.background_subtraction(background_image=bg_img, foreground_image=fg_img)
    truths.append(np.sum(fgmask) > 0)
    # All of these should be true for the function to pass testing.
    assert (all(truths))


def test_plantcv_background_subtraction_bad_img_type():
    fg_color = cv2.imread(os.path.join(TEST_DATA, TEST_FOREGROUND))
    bg_gray = cv2.imread(os.path.join(TEST_DATA, TEST_BACKGROUND), 0)
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.background_subtraction(background_image=bg_gray, foreground_image=fg_color)


def test_plantcv_background_subtraction_different_sizes():
    fg_img = cv2.imread(os.path.join(TEST_DATA, TEST_FOREGROUND))
    bg_img = cv2.imread(os.path.join(TEST_DATA, TEST_BACKGROUND))
    bg_shp = np.shape(bg_img)  # type: tuple
    bg_img_resized = cv2.resize(bg_img, (int(bg_shp[0] / 2), int(bg_shp[1] / 2)), interpolation=cv2.INTER_AREA)
    pcv.params.debug = None
    fgmask = pcv.background_subtraction(background_image=bg_img_resized, foreground_image=fg_img)
    assert np.sum(fgmask) > 0


# ##############################
# Tests for the learn subpackage
# ##############################


def test_plantcv_learn_naive_bayes():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_learn_naive_bayes")
    os.mkdir(cache_dir)
    # Make image and mask directories in the cache directory
    imgdir = os.path.join(cache_dir, "images")
    maskdir = os.path.join(cache_dir, "masks")
    if not os.path.exists(imgdir):
        os.mkdir(imgdir)
    if not os.path.exists(maskdir):
        os.mkdir(maskdir)
    # Copy and image and mask to the image/mask directories
    shutil.copyfile(os.path.join(TEST_DATA, TEST_VIS_SMALL), os.path.join(imgdir, "image.png"))
    shutil.copyfile(os.path.join(TEST_DATA, TEST_MASK_SMALL), os.path.join(maskdir, "image.png"))
    # Run the naive Bayes training module
    outfile = os.path.join(cache_dir, "naive_bayes_pdfs.txt")
    plantcv.learn.naive_bayes(imgdir=imgdir, maskdir=maskdir, outfile=outfile, mkplots=True)
    assert os.path.exists(outfile)


def test_plantcv_learn_naive_bayes_multiclass():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_learn_naive_bayes_multiclass")
    os.mkdir(cache_dir)
    # Run the naive Bayes multiclass training module
    outfile = os.path.join(cache_dir, "naive_bayes_multiclass_pdfs.txt")
    plantcv.learn.naive_bayes_multiclass(samples_file=os.path.join(TEST_DATA, TEST_SAMPLED_RGB_POINTS), outfile=outfile,
                                         mkplots=True)
    assert os.path.exists(outfile)


# ##############################
# Tests for the roi subpackage
# ##############################

def test_plantcv_roi_from_binary_image():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_roi_from_binary_image")
    os.mkdir(cache_dir)
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Create a binary image
    bin_img = np.zeros(np.shape(rgb_img)[0:2], dtype=np.uint8)
    cv2.rectangle(bin_img, (100, 100), (1000, 1000), 255, -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    pcv.params.debug_outdir = cache_dir
    _, _ = pcv.roi.from_binary_image(bin_img=bin_img, img=rgb_img)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _, _ = pcv.roi.from_binary_image(bin_img=bin_img, img=rgb_img)
    # Test with debug = None
    pcv.params.debug = None
    roi_contour, roi_hierarchy = pcv.roi.from_binary_image(bin_img=bin_img, img=rgb_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi_contour) == (1, 3600, 1, 2)


def test_plantcv_roi_from_binary_image_grayscale_input():
    # Read in a test grayscale image
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Create a binary image
    bin_img = np.zeros(np.shape(gray_img)[0:2], dtype=np.uint8)
    cv2.rectangle(bin_img, (100, 100), (1000, 1000), 255, -1)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    roi_contour, roi_hierarchy = pcv.roi.from_binary_image(bin_img=bin_img, img=gray_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi_contour) == (1, 3600, 1, 2)


def test_plantcv_roi_from_binary_image_bad_binary_input():
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Binary input is required but an RGB input is provided
    with pytest.raises(RuntimeError):
        _, _ = pcv.roi.from_binary_image(bin_img=rgb_img, img=rgb_img)


def test_plantcv_roi_rectangle():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_roi_rectangle")
    os.mkdir(cache_dir)
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    pcv.params.debug = "print"
    pcv.params.debug_outdir = cache_dir
    _, _ = pcv.roi.rectangle(x=100, y=100, h=500, w=500, img=rgb_img)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _, _ = pcv.roi.rectangle(x=100, y=100, h=500, w=500, img=rgb_img)
    # Test with debug = None
    pcv.params.debug = None
    roi_contour, roi_hierarchy = pcv.roi.rectangle(x=100, y=100, h=500, w=500, img=rgb_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi_contour) == (1, 4, 1, 2)


def test_plantcv_roi_rectangle_grayscale_input():
    # Read in a test grayscale image
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    roi_contour, roi_hierarchy = pcv.roi.rectangle(x=100, y=100, h=500, w=500, img=gray_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi_contour) == (1, 4, 1, 2)


def test_plantcv_roi_rectangle_out_of_frame():
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # The resulting rectangle needs to be within the dimensions of the image
    with pytest.raises(RuntimeError):
        _, _ = pcv.roi.rectangle(x=100, y=100, h=500, w=3000, img=rgb_img)


def test_plantcv_roi_circle():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_roi_circle")
    os.mkdir(cache_dir)
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    pcv.params.debug = "print"
    pcv.params.debug_outdir = cache_dir
    _, _ = pcv.roi.circle(x=100, y=100, r=50, img=rgb_img)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _, _ = pcv.roi.circle(x=100, y=100, r=50, img=rgb_img)
    # Test with debug = None
    pcv.params.debug = None
    roi_contour, roi_hierarchy = pcv.roi.circle(x=200, y=225, r=75, img=rgb_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi_contour) == (1, 424, 1, 2)


def test_plantcv_roi_circle_grayscale_input():
    # Read in a test grayscale image
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    roi_contour, roi_hierarchy = pcv.roi.circle(x=200, y=225, r=75, img=gray_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi_contour) == (1, 424, 1, 2)


def test_plantcv_roi_circle_out_of_frame():
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # The resulting rectangle needs to be within the dimensions of the image
    with pytest.raises(RuntimeError):
        _, _ = pcv.roi.circle(x=50, y=225, r=75, img=rgb_img)


def test_plantcv_roi_ellipse():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_roi_ellipse")
    os.mkdir(cache_dir)
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    pcv.params.debug = "print"
    pcv.params.debug_outdir = cache_dir
    _, _ = pcv.roi.ellipse(x=200, y=200, r1=75, r2=50, angle=0, img=rgb_img)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _, _ = pcv.roi.ellipse(x=200, y=200, r1=75, r2=50, angle=0, img=rgb_img)
    # Test with debug = None
    pcv.params.debug = None
    roi_contour, roi_hierarchy = pcv.roi.ellipse(x=200, y=200, r1=75, r2=50, angle=0, img=rgb_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi_contour) == (1, 360, 1, 2)


def test_plantcv_roi_ellipse_grayscale_input():
    # Read in a test grayscale image
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    roi_contour, roi_hierarchy = pcv.roi.ellipse(x=200, y=200, r1=75, r2=50, angle=0, img=gray_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi_contour) == (1, 360, 1, 2)


def test_plantcv_roi_ellipse_out_of_frame():
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # The resulting rectangle needs to be within the dimensions of the image
    with pytest.raises(RuntimeError):
        _, _ = pcv.roi.ellipse(x=50, y=225, r1=75, r2=50, angle=0, img=rgb_img)


# ##############################
# Tests for the transform subpackage
# ##############################


def test_plantcv_transform_get_color_matrix():
    # load in target_matrix
    matrix_file = np.load(os.path.join(TEST_DATA, TEST_TARGET_MATRIX), encoding="latin1")
    matrix_compare = matrix_file['arr_0']
    # Read in rgb_img and gray-scale mask
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_MASK), -1)
    # The result should be a len(np.unique(mask))-1 x 4 matrix
    headers, matrix = pcv.transform.get_color_matrix(rgb_img, mask)
    assert np.array_equal(matrix, matrix_compare)


def test_plantcv_transform_get_color_matrix_img():
    # Read in two gray-scale images
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_MASK), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_MASK), -1)
    # The input for rgb_img needs to be an RGB image
    with pytest.raises(RuntimeError):
        _, _ = pcv.transform.get_color_matrix(rgb_img, mask)


def test_plantcv_transform_get_color_matrix_mask():
    # Read in two gray-scale images
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_MASK))
    # The input for rgb_img needs to be an RGB image
    with pytest.raises(RuntimeError):
        _, _ = pcv.transform.get_color_matrix(rgb_img, mask)


def test_plantcv_transform_get_matrix_m():
    # load in comparison matrices
    matrix_m_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_M1), encoding="latin1")
    matrix_compare_m = matrix_m_file['arr_0']
    matrix_b_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_B1), encoding="latin1")
    matrix_compare_b = matrix_b_file['arr_0']
    # read in matrices
    t_matrix_file = np.load(os.path.join(TEST_DATA, TEST_TARGET_MATRIX), encoding="latin1")
    t_matrix = t_matrix_file['arr_0']
    s_matrix_file = np.load(os.path.join(TEST_DATA, TEST_SOURCE1_MATRIX), encoding="latin1")
    s_matrix = s_matrix_file['arr_0']
    # apply matrices to function
    matrix_a, matrix_m, matrix_b = pcv.transform.get_matrix_m(t_matrix, s_matrix)
    matrix_compare_m = np.rint(matrix_compare_m)
    matrix_compare_b = np.rint(matrix_compare_b)
    matrix_m = np.rint(matrix_m)
    matrix_b = np.rint(matrix_b)
    assert np.array_equal(matrix_m, matrix_compare_m) and np.array_equal(matrix_b, matrix_compare_b)


def test_plantcv_transform_get_matrix_m_unequal_data():
    # load in comparison matrices
    matrix_m_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_M2), encoding="latin1")
    matrix_compare_m = matrix_m_file['arr_0']
    matrix_b_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_B2), encoding="latin1")
    matrix_compare_b = matrix_b_file['arr_0']
    # read in matrices
    t_matrix_file = np.load(os.path.join(TEST_DATA, TEST_TARGET_MATRIX), encoding="latin1")
    t_matrix = t_matrix_file['arr_0']
    s_matrix_file = np.load(os.path.join(TEST_DATA, TEST_SOURCE2_MATRIX), encoding="latin1")
    s_matrix = s_matrix_file['arr_0']
    # apply matrices to function
    matrix_a, matrix_m, matrix_b = pcv.transform.get_matrix_m(t_matrix, s_matrix)
    matrix_compare_m = np.rint(matrix_compare_m)
    matrix_compare_b = np.rint(matrix_compare_b)
    matrix_m = np.rint(matrix_m)
    matrix_b = np.rint(matrix_b)
    assert np.array_equal(matrix_m, matrix_compare_m) and np.array_equal(matrix_b, matrix_compare_b)


def test_plantcv_transform_calc_transformation_matrix():
    # load in comparison matrices
    matrix_file = np.load(os.path.join(TEST_DATA, TEST_TRANSFORM1), encoding="latin1")
    matrix_compare = matrix_file['arr_0']
    # read in matrices
    matrix_m_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_M1), encoding="latin1")
    matrix_m = matrix_m_file['arr_0']
    matrix_b_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_B1), encoding="latin1")
    matrix_b = matrix_b_file['arr_0']
    # apply to function
    _, matrix_t = pcv.transform.calc_transformation_matrix(matrix_m, matrix_b)
    matrix_t = np.rint(matrix_t)
    matrix_compare = np.rint(matrix_compare)
    assert np.array_equal(matrix_t, matrix_compare)


def test_plantcv_transform_calc_transformation_matrix_b_incorrect():
    # read in matrices
    matrix_m_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_M1), encoding="latin1")
    matrix_m = matrix_m_file['arr_0']
    matrix_b_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_B1), encoding="latin1")
    matrix_b = matrix_b_file['arr_0']
    matrix_b = np.asmatrix(matrix_b, float)
    with pytest.raises(RuntimeError):
        _, _ = pcv.transform.calc_transformation_matrix(matrix_m, matrix_b.T)


def test_plantcv_transform_calc_transformation_matrix_not_mult():
    # read in matrices
    matrix_m_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_M1), encoding="latin1")
    matrix_m = matrix_m_file['arr_0']
    matrix_b_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_B1), encoding="latin1")
    matrix_b = matrix_b_file['arr_0']
    with pytest.raises(RuntimeError):
        _, _ = pcv.transform.calc_transformation_matrix(matrix_m, matrix_b[:3])


def test_plantcv_transform_calc_transformation_matrix_not_mat():
    # read in matrices
    matrix_m_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_M1), encoding="latin1")
    matrix_m = matrix_m_file['arr_0']
    matrix_b_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_B1), encoding="latin1")
    matrix_b = matrix_b_file['arr_0']
    with pytest.raises(RuntimeError):
        _, _ = pcv.transform.calc_transformation_matrix(matrix_m[:, 1], matrix_b[:, 1])


def test_plantcv_transform_apply_transformation():
    # load corrected image to compare
    corrected_compare = cv2.imread(os.path.join(TEST_DATA, TEST_S1_CORRECTED))
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform")
    os.mkdir(cache_dir)
    # Make image and mask directories in the cache directory
    imgdir = os.path.join(cache_dir, "images")
    # read in matrices
    matrix_t_file = np.load(os.path.join(TEST_DATA, TEST_TRANSFORM1), encoding="latin1")
    matrix_t = matrix_t_file['arr_0']
    # read in images
    target_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    source_img = cv2.imread(os.path.join(TEST_DATA, TEST_SOURCE1_IMG))
    # Test with debug = "print"
    pcv.params.debug = "print"
    pcv.params.debug_outdir = imgdir
    _ = pcv.transform.apply_transformation_matrix(source_img, target_img, matrix_t)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.transform.apply_transformation_matrix(source_img, target_img, matrix_t)
    # Test with debug = None
    pcv.params.debug = None
    corrected_img = pcv.transform.apply_transformation_matrix(source_img, target_img, matrix_t)
    # assert source and corrected have same shape
    assert np.array_equal(corrected_img, corrected_compare)


def test_plantcv_transform_apply_transformation_incorrect_t():
    # read in matrices
    matrix_t_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_B1), encoding="latin1")
    matrix_t = matrix_t_file['arr_0']
    # read in images
    target_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    source_img = cv2.imread(os.path.join(TEST_DATA, TEST_SOURCE1_IMG))
    with pytest.raises(RuntimeError):
        _ = pcv.transform.apply_transformation_matrix(source_img, target_img, matrix_t)


def test_plantcv_transform_apply_transformation_incorrect_img():
    # read in matrices
    matrix_t_file = np.load(os.path.join(TEST_DATA, TEST_TRANSFORM1), encoding="latin1")
    matrix_t = matrix_t_file['arr_0']
    # read in images
    target_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    source_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_MASK), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.transform.apply_transformation_matrix(source_img, target_img, matrix_t)


def test_plantcv_transform_save_matrix():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform")
    os.mkdir(cache_dir)
    # read in matrix
    matrix_t_file = np.load(os.path.join(TEST_DATA, TEST_TRANSFORM1), encoding="latin1")
    matrix_t = matrix_t_file['arr_0']
    # .npz filename
    filename = os.path.join(cache_dir, 'test.npz')
    pcv.transform.save_matrix(matrix_t, filename)
    assert os.path.exists(filename) is True


def test_plantcv_transform_save_matrix_incorrect_filename():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform")
    os.mkdir(cache_dir)
    # read in matrix
    matrix_t_file = np.load(os.path.join(TEST_DATA, TEST_TRANSFORM1), encoding="latin1")
    matrix_t = matrix_t_file['arr_0']
    # .npz filename
    filename = "test"
    with pytest.raises(RuntimeError):
        pcv.transform.save_matrix(matrix_t, filename)


def test_plantcv_transform_load_matrix():
    # read in matrix_t
    matrix_t_file = np.load(os.path.join(TEST_DATA, TEST_TRANSFORM1), encoding="latin1")
    matrix_t = matrix_t_file['arr_0']
    # test load function with matrix_t
    matrix_t_loaded = pcv.transform.load_matrix(os.path.join(TEST_DATA, TEST_TRANSFORM1))
    assert np.array_equal(matrix_t, matrix_t_loaded)


def test_plantcv_transform_correct_color():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform")
    os.mkdir(cache_dir)
    # load corrected image to compare
    corrected_compare = cv2.imread(os.path.join(TEST_DATA, TEST_S1_CORRECTED))
    # load in comparison matrices
    matrix_file = np.load(os.path.join(TEST_DATA, TEST_TRANSFORM1), encoding="latin1")
    matrix_compare = matrix_file['arr_0']
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform_correct_color")
    os.mkdir(cache_dir)
    # Make image and mask directories in the cache directory
    imgdir = os.path.join(cache_dir, "images")
    matdir = os.path.join(cache_dir, "saved_matrices")
    # Read in target, source, and gray-scale mask
    target_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    source_img = cv2.imread(os.path.join(TEST_DATA, TEST_SOURCE1_IMG))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_MASK), -1)
    output_path = os.path.join(matdir)
    # Test with debug = "print"
    pcv.params.debug = "print"
    pcv.params.debug_outdir = imgdir
    _, _, _, _ = pcv.transform.correct_color(target_img, mask, source_img, mask, cache_dir)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _, _, _, _ = pcv.transform.correct_color(target_img, mask, source_img, mask, output_path)
    # Test with debug = None
    pcv.params.debug = None
    _, _, matrix_t, corrected_img = pcv.transform.correct_color(target_img, mask, source_img, mask, output_path)
    # assert source and corrected have same shape
    assert np.array_equal(corrected_img, corrected_compare) and \
           os.path.exists(os.path.join(output_path, "target_matrix.npz")) is True and \
           os.path.exists(os.path.join(output_path, "source_matrix.npz")) is True and \
           os.path.exists(os.path.join(output_path, "transformation_matrix.npz")) is True


def test_plantcv_transform_correct_color_output_dne():
    # load corrected image to compare
    corrected_compare = cv2.imread(os.path.join(TEST_DATA, TEST_S1_CORRECTED))
    # load in comparison matrices
    matrix_file = np.load(os.path.join(TEST_DATA, TEST_TRANSFORM1), encoding="latin1")
    matrix_compare = matrix_file['arr_0']
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform_correct_color_output_dne")
    os.mkdir(cache_dir)
    # Make image and mask directories in the cache directory
    imgdir = os.path.join(cache_dir, "images")
    # Read in target, source, and gray-scale mask
    target_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    source_img = cv2.imread(os.path.join(TEST_DATA, TEST_SOURCE1_IMG))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_MASK), -1)
    output_path = os.path.join(cache_dir, "saved_matrices_1")  # output_directory that does not currently exist
    # Test with debug = "print"
    pcv.params.debug = "print"
    pcv.params.debug_outdir = imgdir
    _, _, _, _ = pcv.transform.correct_color(target_img, mask, source_img, mask, output_path)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _, _, _, _ = pcv.transform.correct_color(target_img, mask, source_img, mask, output_path)
    # Test with debug = None
    pcv.params.debug = None
    _, _, matrix_t, corrected_img = pcv.transform.correct_color(target_img, mask, source_img, mask, output_path)
    # assert source and corrected have same shape
    assert np.array_equal(corrected_img, corrected_compare) and \
           os.path.exists(os.path.join(output_path, "target_matrix.npz")) is True and \
           os.path.exists(os.path.join(output_path, "source_matrix.npz")) is True and \
           os.path.exists(os.path.join(output_path, "transformation_matrix.npz")) is True


def test_plantcv_transform_create_color_card_mask():
    # Load target image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform_create_color_card_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.transform.create_color_card_mask(rgb_img=rgb_img, radius=6, start_coord=(166, 166),
                                             spacing=(21, 21), nrows=6, ncols=4, exclude=[20, 0])
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.transform.create_color_card_mask(rgb_img=rgb_img, radius=6, start_coord=(166, 166),
                                             spacing=(21, 21), nrows=6, ncols=4, exclude=[20, 0])
    # Test with debug = None
    pcv.params.debug = None
    mask = pcv.transform.create_color_card_mask(rgb_img=rgb_img, radius=6, start_coord=(166, 166),
                                                spacing=(21, 21), nrows=6, ncols=4, exclude=[20, 0])
    assert all([i == j] for i, j in zip(np.unique(mask), np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110,
                                                                   120, 130, 140, 150, 160, 170, 180, 190, 200, 210,
                                                                   220], dtype=np.uint8)))


def test_plantcv_transform_quick_color_check():
    # Load target image
    t_matrix = np.load(os.path.join(TEST_DATA, TEST_TARGET_MATRIX), encoding="latin1")
    target_matrix = t_matrix['arr_0']
    s_matrix = np.load(os.path.join(TEST_DATA, TEST_SOURCE1_MATRIX), encoding="latin1")
    source_matrix = s_matrix['arr_0']
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform_quick_color_check")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Test with debug = "print"
    pcv.params.debug = "print"
    pcv.transform.quick_color_check(target_matrix, source_matrix, num_chips=22)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    pcv.transform.quick_color_check(target_matrix, source_matrix, num_chips=22)
    #Test with debug = None
    pcv.params.debug = None
    pcv.transform.quick_color_check(target_matrix, source_matrix, num_chips=22)
    assert os.path.exists(os.path.join(cache_dir, "color_quick_check.png"))


def test_plantcv_transform_find_color_card():
    # Load rgb image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    img_w_hexagon = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG_COLOR_CARD))
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform_find_color_card")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    df, start, space = pcv.transform.find_color_card(rgb_img=rgb_img, threshold='adaptgauss', blurry=False)
    _, _, _ = pcv.transform.find_color_card(rgb_img=img_w_hexagon, threshold='adaptgauss', blurry=False)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.transform.create_color_card_mask(rgb_img=rgb_img, radius=6, start_coord=start,
                                             spacing=space, nrows=6, ncols=4, exclude=[20, 0])
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.transform.create_color_card_mask(rgb_img=rgb_img, radius=6, start_coord=start,
                                             spacing=space, nrows=6, ncols=4, exclude=[20, 0])
    # Test with debug = None
    pcv.params.debug = None
    mask = pcv.transform.create_color_card_mask(rgb_img=rgb_img, radius=6, start_coord=start,
                                                spacing=space, nrows=6, ncols=4, exclude=[20, 0])
    assert all([i == j] for i, j in zip(np.unique(mask), np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110,
                                                                   120, 130, 140, 150, 160, 170, 180, 190, 200, 210,
                                                                   220], dtype=np.uint8)))


def test_plantcv_transform_find_color_card_optional_parameters():
    # Load rgb image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG_COLOR_CARD))
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform_find_color_card")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Test with threshold ='normal'
    df1, start1, space1 = pcv.transform.find_color_card(rgb_img=rgb_img, threshold='normal', blurry=True,
                                                        background='light')
    _ = pcv.transform.create_color_card_mask(rgb_img=rgb_img, radius=6, start_coord=start1,
                                             spacing=space1, nrows=6, ncols=4, exclude=[20, 0])
    # Test with threshold='otsu'
    df2, start2, space2 = pcv.transform.find_color_card(rgb_img=rgb_img, threshold='otsu', blurry=True)
    _ = pcv.transform.create_color_card_mask(rgb_img=rgb_img, radius=6, start_coord=start2,
                                             spacing=space2, nrows=6, ncols=4, exclude=[20, 0])
    # Test with debug = None
    pcv.params.debug = None
    mask = pcv.transform.create_color_card_mask(rgb_img=rgb_img, radius=6, start_coord=start2,
                                                spacing=space2, nrows=6, ncols=4, exclude=[20, 0])
    assert all([i == j] for i, j in zip(np.unique(mask), np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110,
                                                                   120, 130, 140, 150, 160, 170, 180, 190, 200, 210,
                                                                   220], dtype=np.uint8)))


def test_plantcv_transform_find_color_card_bad_thresh_input():
    # Load rgb image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _, _, _ = pcv.transform.find_color_card(rgb_img=rgb_img, threshold='gaussian')


def test_plantcv_transform_find_color_card_bad_background_input():
    # Load rgb image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _, _, _ = pcv.transform.find_color_card(rgb_img=rgb_img, background='lite')


# ##############################
# Tests for the threshold subpackage
# ##############################
def test_plantcv_threshold_binary():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_threshold_binary")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with object type = dark
    pcv.params.debug = None
    _ = pcv.threshold.binary(gray_img=gray_img, threshold=25, max_value=255, object_type="dark")
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.threshold.binary(gray_img=gray_img, threshold=25, max_value=255, object_type="light")
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.threshold.binary(gray_img=gray_img, threshold=25, max_value=255, object_type="light")
    # Test with debug = None
    pcv.params.debug = None
    binary_img = pcv.threshold.binary(gray_img=gray_img, threshold=25, max_value=255, object_type="light")
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(binary_img), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(binary_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_threshold_binary_incorrect_object_type():
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _ = pcv.threshold.binary(gray_img=gray_img, threshold=25, max_value=255, object_type="lite")


def test_plantcv_threshold_gaussian():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_threshold_gaussian")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with object type = dark
    pcv.params.debug = None
    _ = pcv.threshold.gaussian(gray_img=gray_img, max_value=255, object_type="dark")
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.threshold.gaussian(gray_img=gray_img, max_value=255, object_type="light")
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.threshold.gaussian(gray_img=gray_img, max_value=255, object_type="light")
    # Test with debug = None
    pcv.params.debug = None
    binary_img = pcv.threshold.gaussian(gray_img=gray_img, max_value=255, object_type="light")
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(binary_img), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(binary_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_threshold_gaussian_incorrect_object_type():
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _ = pcv.threshold.gaussian(gray_img=gray_img, max_value=255, object_type="lite")


def test_plantcv_threshold_mean():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_threshold_mean")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with object type = dark
    pcv.params.debug = None
    _ = pcv.threshold.mean(gray_img=gray_img, max_value=255, object_type="dark")
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.threshold.mean(gray_img=gray_img, max_value=255, object_type="light")
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.threshold.mean(gray_img=gray_img, max_value=255, object_type="light")
    # Test with debug = None
    pcv.params.debug = None
    binary_img = pcv.threshold.mean(gray_img=gray_img, max_value=255, object_type="light")
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(binary_img), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(binary_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_threshold_mean_incorrect_object_type():
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _ = pcv.threshold.mean(gray_img=gray_img, max_value=255, object_type="lite")


def test_plantcv_threshold_otsu():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_threshold_otsu")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INTPUT_GREENMAG), -1)
    # Test with object set to light
    pcv.params.debug = None
    _ = pcv.threshold.otsu(gray_img=gray_img, max_value=255, object_type="light")
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.threshold.otsu(gray_img=gray_img, max_value=255, object_type='dark')
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.threshold.otsu(gray_img=gray_img, max_value=255, object_type='dark')
    # Test with debug = None
    pcv.params.debug = None
    binary_img = pcv.threshold.otsu(gray_img=gray_img, max_value=255, object_type='dark')
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(binary_img), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(binary_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_threshold_otsu_incorrect_object_type():
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _ = pcv.threshold.otsu(gray_img=gray_img, max_value=255, object_type="lite")


def test_plantcv_threshold_triangle():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_threshold_triangle")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.threshold.triangle(gray_img=gray_img, max_value=255, object_type="dark", xstep=10)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.threshold.triangle(gray_img=gray_img, max_value=255, object_type="light", xstep=10)
    # Test with debug = None
    pcv.params.debug = None
    binary_img = pcv.threshold.triangle(gray_img=gray_img, max_value=255, object_type="light", xstep=10)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(binary_img), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(binary_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_threshold_triangle_incorrect_object_type():
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _ = pcv.threshold.triangle(gray_img=gray_img, max_value=255, object_type="lite", xstep=10)


def test_plantcv_threshold_texture():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_threshold_texture")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY_SMALL), -1)
    binary_img = pcv.threshold.texture(gray_img, kernel=6, threshold=7, offset=3, texture_method='dissimilarity',
                                       borders='nearest', max_value=255)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(binary_img), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(binary_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0

# ##############################
# Clean up test files
# ##############################
def teardown_function():
    shutil.rmtree(TEST_TMPDIR)
