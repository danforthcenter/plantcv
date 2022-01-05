#!/usr/bin/env python

import pytest
import os
import shutil
import numpy as np
import cv2
import pandas as pd
from plotnine import ggplot
from plantcv import plantcv as pcv
import plantcv.learn
import plantcv.parallel
import plantcv.utils
# Import matplotlib and use a null Template to block plotting to screen
# This will let us test debug = "plot"
import matplotlib
from skimage import img_as_ubyte

TEST_TMPDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".cache")


# ##########################
# Tests setup function
# ##########################
def setup_function():
    if not os.path.exists(TEST_TMPDIR):
        os.mkdir(TEST_TMPDIR)


# ####################################################################################################################
# ########################################### PLANTCV MAIN PACKAGE ###################################################
matplotlib.use('Template')

TEST_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
HYPERSPECTRAL_TEST_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hyperspectral_data")
HYPERSPECTRAL_DATA = "darkReference"
HYPERSPECTRAL_HDR_SMALL_RANGE = {'description': '{[HEADWALL Hyperspec III]}', 'samples': '800', 'lines': '1',
                                 'bands': '978', 'header offset': '0', 'file type': 'ENVI Standard',
                                 'interleave': 'bil', 'sensor type': 'Unknown', 'byte order': '0',
                                 'default bands': '159,253,520', 'wavelength units': 'nm',
                                 'wavelength': ['379.027', '379.663', '380.3', '380.936', '381.573', '382.209']}
FLUOR_TEST_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photosynthesis_data")
FLUOR_IMG = "PSII_PSD_supopt_temp_btx623_22_rep1.DAT"
TEST_COLOR_DIM = (2056, 2454, 3)
TEST_GRAY_DIM = (2056, 2454)
TEST_BINARY_DIM = TEST_GRAY_DIM
TEST_INPUT_COLOR = "input_color_img.jpg"
TEST_INPUT_GRAY = "input_gray_img.jpg"
TEST_INPUT_GRAY_SMALL = "input_gray_img_small.jpg"
TEST_INPUT_BINARY = "input_binary_img.png"
TEST_INPUT_ROI_CONTOUR = "input_roi_contour.npz"
TEST_INPUT_ROI_HIERARCHY = "input_roi_hierarchy.npz"
TEST_INPUT_CONTOURS = "input_contours.npz"
TEST_INPUT_OBJECT_CONTOURS = "input_object_contours.npz"
TEST_INPUT_OBJECT_HIERARCHY = "input_object_hierarchy.npz"
TEST_VIS = "VIS_SV_0_z300_h1_g0_e85_v500_93054.png"
TEST_NIR = "NIR_SV_0_z300_h1_g0_e15000_v500_93059.png"
TEST_VIS_TV = "VIS_TV_0_z300_h1_g0_e85_v500_93054.png"
TEST_NIR_TV = "NIR_TV_0_z300_h1_g0_e15000_v500_93059.png"
TEST_INPUT_MASK = "input_mask_binary.png"
TEST_INPUT_MASK_OOB = "mask_outbounds.png"
TEST_INPUT_MASK_RESIZE = "input_mask_resize.png"
TEST_INPUT_NIR_MASK = "input_nir.png"
TEST_INPUT_FDARK = "FLUO_TV_dark.png"
TEST_INPUT_FDARK_LARGE = "FLUO_TV_DARK_large"
TEST_INPUT_FMIN = "FLUO_TV_min.png"
TEST_INPUT_FMAX = "FLUO_TV_max.png"
TEST_INPUT_FMASK = "FLUO_TV_MASK.png"
TEST_INPUT_MULTI = "multi_ori_image.jpg"
TEST_INPUT_MULTI_MASK = "multi_ori_mask.jpg"
TEST_INPUT_MULTI_OBJECT = "roi_objects.npz"
TEST_INPUT_MULTI_CONTOUR = "multi_contours.npz"
TEST_INPUT_ClUSTER_CONTOUR = "clusters_i.npz"
TEST_INPUT_MULTI_HIERARCHY = "multi_hierarchy.npz"
TEST_INPUT_VISUALIZE_CONTOUR = "roi_objects_visualize.npz"
TEST_INPUT_VISUALIZE_HIERARCHY = "roi_obj_hierarchy_visualize.npz"
TEST_INPUT_VISUALIZE_CLUSTERS = "clusters_i_visualize.npz"
TEST_INPUT_VISUALIZE_BACKGROUND = "visualize_background_img.png"
TEST_INPUT_GENOTXT = "cluster_names.txt"
TEST_INPUT_GENOTXT_TOO_MANY = "cluster_names_too_many.txt"
TEST_INPUT_CROPPED = 'cropped_img.jpg'
TEST_INPUT_CROPPED_MASK = 'cropped-mask.png'
TEST_INPUT_MARKER = 'seed-image.jpg'
TEST_INPUT_SKELETON = 'input_skeleton.png'
TEST_INPUT_SKELETON_PRUNED = 'input_pruned_skeleton.png'
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
TEST_SKELETON_OBJECTS = "skeleton_objects.npz"
TEST_SKELETON_HIERARCHIES = "skeleton_hierarchies.npz"
TEST_THERMAL_ARRAY = "thermal_img.npz"
TEST_THERMAL_IMG_MASK = "thermal_img_mask.png"
PIXEL_VALUES = "pixel_inspector_rgb_values.txt"
TEST_INPUT_LEAF_MASK = "leaves_mask.png"


# ##########################
# Tests for the main package
# ##########################
def test_plantcv_analyze_color():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test with debug = None
    pcv.params.debug = None
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type="all")
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type=None, label="prefix")
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type=None)
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type='lab')
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type='hsv')
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type=None)

    # Test with debug = "print"
    # pcv.params.debug = "print"
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type="all")
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type=None, label="prefix")

    # Test with debug = "plot"
    # pcv.params.debug = "plot"
    # _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type=None)
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type='lab')
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type='hsv')
    # _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type=None)

    # Test with debug = None
    # pcv.params.debug = None
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type='rgb')
    assert pcv.outputs.observations['default']['hue_median']['value'] == 84.0


def test_plantcv_analyze_color_incorrect_image():
    img_binary = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.analyze_color(rgb_img=img_binary, mask=mask, hist_plot_type=None)
#
#


def test_plantcv_analyze_color_bad_hist_type():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    pcv.params.debug = "plot"
    with pytest.raises(RuntimeError):
        _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type='bgr')


def test_plantcv_analyze_color_incorrect_hist_plot_type():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    with pytest.raises(RuntimeError):
        pcv.params.debug = "plot"
        _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type="bgr")


def test_plantcv_analyze_nir():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test with debug=None
    pcv.params.debug = None
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)

    _ = pcv.analyze_nir_intensity(gray_img=img, mask=mask, bins=256, histplot=True)
    result = len(pcv.outputs.observations['default']['nir_frequencies']['value'])
    assert result == 256


def test_plantcv_analyze_nir_16bit():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test with debug=None
    pcv.params.debug = None
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)

    _ = pcv.analyze_nir_intensity(gray_img=np.uint16(img), mask=mask, bins=256, histplot=True)
    result = len(pcv.outputs.observations['default']['nir_frequencies']['value'])
    assert result == 256


def test_plantcv_analyze_object():
    # Test with debug = None
    pcv.params.debug = None
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    obj_images = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    pcv.outputs.clear()
    assert len(obj_images) != 0


def test_plantcv_analyze_object_grayscale_input():
    # Test with debug = None
    pcv.params.debug = None
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    obj_images = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    assert len(obj_images) != 1


def test_plantcv_analyze_object_zero_slope():
    # Test with debug = None
    pcv.params.debug = None
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
    obj_images = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    assert len(obj_images) != 0


def test_plantcv_analyze_object_longest_axis_2d():
    # Test with debug = None
    pcv.params.debug = None
    # Create a test image
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    img[0:5, 45:49, 0] = 255
    img[0:5, 0:5, 0] = 255
    mask = img[:, :, 0]
    obj_contour = np.array([[[45, 1]], [[45, 2]], [[45, 3]], [[45, 4]], [[46, 4]], [[47, 4]], [[48, 4]],
                            [[48, 3]], [[48, 2]], [[48, 1]], [[47, 1]], [[46, 1]], [[1, 1]], [[1, 2]],
                            [[1, 3]], [[1, 4]], [[2, 4]], [[3, 4]], [[4, 4]], [[4, 3]], [[4, 2]],
                            [[4, 1]], [[3, 1]], [[2, 1]]], dtype=np.int32)
    obj_images = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    assert len(obj_images) != 0


def test_plantcv_analyze_object_longest_axis_2e():
    # Test with debug = None
    pcv.params.debug = None
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
    obj_images = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    assert len(obj_images) != 0


def test_plantcv_analyze_object_small_contour():
    # Test with debug = None
    pcv.params.debug = None
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    obj_contour = [np.array([[[0, 0]], [[0, 50]], [[50, 50]], [[50, 0]]], dtype=np.int32)]
    obj_images = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    assert obj_images is None


def test_plantcv_analyze_thermal_values():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_thermal_values")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    # img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_THERMAL_IMG_MASK), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_THERMAL_ARRAY), encoding="latin1")
    img = contours_npz['arr_0']

    pcv.params.debug = None
    thermal_hist = pcv.analyze_thermal_values(thermal_array=img, mask=mask, histplot=True)
    assert thermal_hist is not None and pcv.outputs.observations['default']['median_temp']['value'] == 33.20922


def test_plantcv_auto_crop():
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    contours = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_OBJECT), encoding="latin1")
    roi_contours = [contours[arr_n] for arr_n in contours]
    # Test with debug = None
    pcv.params.debug = None
    # padding as tuple
    _ = pcv.auto_crop(img=img1, obj=roi_contours[1], padding_x=(20, 10), padding_y=(20, 10), color='black')
    # padding 0 so crop same as image
    _ = pcv.auto_crop(img=img1, obj=roi_contours[1], color='image')
    # padding as int
    cropped = pcv.auto_crop(img=img1, obj=roi_contours[1], padding_x=20, padding_y=20, color='image')
    x, y, z = np.shape(img1)
    x1, y1, z1 = np.shape(cropped)
    assert x > x1


def test_plantcv_auto_crop_grayscale_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_auto_crop_grayscale_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
    contours = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_OBJECT), encoding="latin1")
    roi_contours = [contours[arr_n] for arr_n in contours]
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    cropped = pcv.auto_crop(img=gray_img, obj=roi_contours[1], padding_x=20, padding_y=20, color='white')
    x, y = np.shape(gray_img)
    x1, y1 = np.shape(cropped)
    assert x > x1


def test_plantcv_auto_crop_bad_color_input():
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
    contours = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_OBJECT), encoding="latin1")
    roi_contours = [contours[arr_n] for arr_n in contours]
    with pytest.raises(RuntimeError):
        _ = pcv.auto_crop(img=gray_img, obj=roi_contours[1], padding_x=20, padding_y=20, color='wite')


def test_plantcv_auto_crop_bad_padding_input():
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
    contours = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_OBJECT), encoding="latin1")
    roi_contours = [contours[arr_n] for arr_n in contours]
    with pytest.raises(RuntimeError):
        _ = pcv.auto_crop(img=gray_img, obj=roi_contours[1], padding_x="one", padding_y=20, color='white')


def test_plantcv_canny_edge_detect():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_canny_edge_detect")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    _ = pcv.canny_edge_detect(img=rgb_img, mask=mask, mask_color='white')
    _ = pcv.canny_edge_detect(img=img, mask=mask, mask_color='black')
    _ = pcv.canny_edge_detect(img=img, thickness=2)
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
        _ = pcv.canny_edge_detect(img=img, mask=mask, mask_color="gray")


def test_plantcv_closing():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_closing")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
    bin_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug=None
    pcv.params.debug = None
    _ = pcv.closing(gray_img, np.ones((4, 4), np.uint8))
    filtered_img = pcv.closing(bin_img)
    assert np.sum(filtered_img) == 16261860


def test_plantcv_closing_bad_input():
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.closing(rgb_img)


def test_plantcv_cluster_contours():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_cluster_contours")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    roi_objects = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_OBJECT), encoding="latin1")
    hierarchy = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_HIERARCHY), encoding="latin1")
    objs = [roi_objects[arr_n] for arr_n in roi_objects]
    obj_hierarchy = hierarchy['arr_0']
    # Test with debug = 'plot' to cover plotting logic
    pcv.params.debug = 'plot'
    _ = pcv.cluster_contours(img=img1, roi_objects=objs, roi_obj_hierarchy=obj_hierarchy, show_grid=True)
    # Test with debug = None
    pcv.params.debug = None
    clusters_i, contours, hierarchy = pcv.cluster_contours(img=img1, roi_objects=objs, roi_obj_hierarchy=obj_hierarchy,
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
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), 0)
    roi_objects = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_OBJECT), encoding="latin1")
    hierachy = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_HIERARCHY), encoding="latin1")
    objs = [roi_objects[arr_n] for arr_n in roi_objects]
    obj_hierarchy = hierachy['arr_0']
    # Test with debug = 'plot' to cover plotting logic
    pcv.params.debug = 'plot'
    _ = pcv.cluster_contours(img=img1, roi_objects=objs, roi_obj_hierarchy=obj_hierarchy, show_grid=True)
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
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    contours = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_CONTOUR), encoding="latin1")
    clusters = np.load(os.path.join(TEST_DATA, TEST_INPUT_ClUSTER_CONTOUR), encoding="latin1")
    hierachy = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_HIERARCHY), encoding="latin1")
    cluster_names = os.path.join(TEST_DATA, TEST_INPUT_GENOTXT)
    cluster_names_too_many = os.path.join(TEST_DATA, TEST_INPUT_GENOTXT_TOO_MANY)
    roi_contours = [contours[arr_n] for arr_n in contours]
    cluster_contours = [clusters[arr_n] for arr_n in clusters]
    obj_hierarchy = hierachy['arr_0']
    # Test with debug = None
    pcv.params.debug = None
    _, _, _ = pcv.cluster_contour_splitimg(img=img1, grouped_contour_indexes=cluster_contours,
                                           contours=roi_contours,
                                           hierarchy=obj_hierarchy, outdir=cache_dir, file=None, filenames=None)
    _, _, _ = pcv.cluster_contour_splitimg(img=img1, grouped_contour_indexes=[[0]], contours=[],
                                           hierarchy=np.array([[[1, -1, -1, -1]]]))
    _, _, _ = pcv.cluster_contour_splitimg(img=img1, grouped_contour_indexes=cluster_contours,
                                           contours=roi_contours,
                                           hierarchy=obj_hierarchy, outdir=cache_dir, file='multi', filenames=None)
    _, _, _ = pcv.cluster_contour_splitimg(img=img1, grouped_contour_indexes=cluster_contours,
                                           contours=roi_contours,
                                           hierarchy=obj_hierarchy, outdir=None, file=None, filenames=cluster_names)
    _, _, _ = pcv.cluster_contour_splitimg(img=img1, grouped_contour_indexes=cluster_contours,
                                           contours=roi_contours,
                                           hierarchy=obj_hierarchy, outdir=None, file=None,
                                           filenames=cluster_names_too_many)
    output_path, imgs, masks = pcv.cluster_contour_splitimg(img=img1, grouped_contour_indexes=cluster_contours,
                                                            contours=roi_contours, hierarchy=obj_hierarchy, outdir=None,
                                                            file=None,
                                                            filenames=None)
    assert len(output_path) != 0


def test_plantcv_cluster_contours_splitimg_grayscale():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_cluster_contours_splitimg_grayscale")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), 0)
    contours = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_CONTOUR), encoding="latin1")
    clusters = np.load(os.path.join(TEST_DATA, TEST_INPUT_ClUSTER_CONTOUR), encoding="latin1")
    hierachy = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_HIERARCHY), encoding="latin1")
    roi_contours = [contours[arr_n] for arr_n in contours]
    cluster_contours = [clusters[arr_n] for arr_n in clusters]
    obj_hierarchy = hierachy['arr_0']
    pcv.params.debug = None
    output_path, imgs, masks = pcv.cluster_contour_splitimg(img=img1, grouped_contour_indexes=cluster_contours,
                                                            contours=roi_contours, hierarchy=obj_hierarchy, outdir=None,
                                                            file=None,
                                                            filenames=None)
    assert len(output_path) != 0


def test_plantcv_color_palette():
    # Return a color palette
    colors = pcv.color_palette(num=10, saved=False)
    assert np.shape(colors) == (10, 3)


def test_plantcv_color_palette_random():
    # Return a color palette in random order
    pcv.params.color_sequence = "random"
    colors = pcv.color_palette(num=10, saved=False)
    assert np.shape(colors) == (10, 3)


def test_plantcv_color_palette_saved():
    # Return a color palette that was saved
    pcv.params.saved_color_scale = [[0, 0, 0], [255, 255, 255]]
    colors = pcv.color_palette(num=2, saved=True)
    assert colors == [[0, 0, 0], [255, 255, 255]]


def test_plantcv_crop():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_crop")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img, _, _ = pcv.readimage(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK), 'gray')
    pcv.params.debug = None
    cropped = pcv.crop(img=img, x=10, y=10, h=50, w=50)
    assert np.shape(cropped) == (50, 50)


def test_plantcv_crop_hyperspectral():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_crop_hyperspectral")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = np.ones((2056, 2454))
    img_stacked = cv2.merge((img, img, img, img))
    pcv.params.debug = None
    cropped = pcv.crop(img=img_stacked, x=10, y=10, h=50, w=50)
    assert np.shape(cropped) == (50, 50, 4)


def test_plantcv_crop_position_mask():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_crop_position_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    nir, path1, filename1 = pcv.readimage(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK), 'gray')
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
    mask_three_channel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
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
    assert np.sum(newmask) == 707115


def test_plantcv_crop_position_mask_color():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_crop_position_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    nir, path1, filename1 = pcv.readimage(os.path.join(TEST_DATA, TEST_INPUT_COLOR), mode='native')
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
    assert np.sum(newmask) == 707115


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


def test_plantcv_crop_position_mask_bad_input_vpos():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_crop_position_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
    # Read in test data
    nir, path1, filename1 = pcv.readimage(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK))
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="below", h_pos="right")


def test_plantcv_crop_position_mask_bad_input_hpos():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_crop_position_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
    # Read in test data
    nir, path1, filename1 = pcv.readimage(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK))
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="top", h_pos="starboard")


def test_plantcv_dilate():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_dilate")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    dilate_img = pcv.dilate(gray_img=img, ksize=5, i=1)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(dilate_img), TEST_BINARY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(dilate_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_dilate_small_k():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    with pytest.raises(ValueError):
        _ = pcv.dilate(img, 1, 1)


def test_plantcv_erode():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_erode")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    erode_img = pcv.erode(gray_img=img, ksize=5, i=1)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(erode_img), TEST_BINARY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(erode_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_erode_small_k():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    with pytest.raises(ValueError):
        _ = pcv.erode(img, 1, 1)


def test_plantcv_distance_transform():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_distance_transform")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_CROPPED_MASK), -1)
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
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
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


def test_plantcv_fill_holes():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_fill_holes")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    fill_img = pcv.fill_holes(bin_img=img)
    assert np.sum(fill_img) > np.sum(img)


def test_plantcv_fill_holes_bad_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_fill_holes_bad_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.fill_holes(bin_img=img)


def test_plantcv_find_objects():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_find_objects")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    contours, hierarchy = pcv.find_objects(img=img, mask=mask)
    # Assert the correct number of contours are found
    assert len(contours) == 2


def test_plantcv_find_objects_grayscale_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_find_objects_grayscale_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    contours, hierarchy = pcv.find_objects(img=img, mask=mask)
    # Assert the correct number of contours are found
    assert len(contours) == 2


def test_plantcv_flip():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_flip")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    img_binary = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.flip(img=img_binary, direction="vertical")
    flipped_img = pcv.flip(img=img, direction="horizontal")
    assert all([i == j] for i, j in zip(np.shape(flipped_img), TEST_COLOR_DIM))


def test_plantcv_flip_bad_input():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.flip(img=img, direction="vert")


def test_plantcv_gaussian_blur():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_gaussian_blur")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img_color = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), -1)
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.gaussian_blur(img=img_color, ksize=(51, 51), sigma_x=0, sigma_y=None)
    gaussian_img = pcv.gaussian_blur(img=img, ksize=(51, 51), sigma_x=0, sigma_y=None)
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
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 1)
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
    # Test with debug = None
    pcv.params.debug = None
    added_img = pcv.image_add(gray_img1=img1, gray_img2=img2)
    assert all([i == j] for i, j in zip(np.shape(added_img), TEST_BINARY_DIM))


def test_plantcv_image_fusion():
    # Read in test data
    # 16-bit image
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMAX), -1)
    img2 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMIN))
    # 8-bit image
    img2 = img_as_ubyte(img2)
    fused_img = pcv.image_fusion(img1, img2, [480.0], [550.0, 640.0, 800.0])
    assert str(type(fused_img)) == "<class 'plantcv.plantcv.classes.Spectral_data'>"


def test_plantcv_image_fusion_size_diff():
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), 0)
    img2 = np.copy(img1)
    img2 = img2[0:10, 0:10]
    with pytest.raises(RuntimeError):
        _ = pcv.image_fusion(img1, img2, [480.0, 550.0, 670.0], [480.0, 550.0, 670.0])


def test_plantcv_image_subtract():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_image_sub")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # read in images
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
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
    # Clear previous outputs
    pcv.outputs.clear()
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_landmark_reference")
    os.mkdir(cache_dir)
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
    _ = pcv.landmark_reference_pt_dist(points_r=points_rescaled, centroid_r=centroid_rescaled,
                                       bline_r=bottomline_rescaled, label="prefix")
    assert len(pcv.outputs.observations['prefix'].keys()) == 8


def test_plantcv_laplace_filter():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_laplace_filter")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = None
    pcv.params.debug = None
    lp_img = pcv.laplace_filter(gray_img=img, ksize=1, scale=1)
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
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.median_blur(gray_img=img, ksize=(5, 5))
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
    object_contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_CONTOURS), encoding="latin1")
    object_contours = [object_contours_npz[arr_n] for arr_n in object_contours_npz]
    object_hierarchy_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_HIERARCHY), encoding="latin1")
    object_hierarchy = object_hierarchy_npz['arr_0']
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.object_composition(img=img, contours=[], hierarchy=object_hierarchy)
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
    object_contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_CONTOURS), encoding="latin1")
    object_contours = [object_contours_npz[arr_n] for arr_n in object_contours_npz]
    object_hierarchy_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_HIERARCHY), encoding="latin1")
    object_hierarchy = object_hierarchy_npz['arr_0']
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    contours, mask = pcv.object_composition(img=img, contours=object_contours, hierarchy=object_hierarchy)
    # Assert that the objects have been combined
    contour_shape = np.shape(contours)  # type: tuple
    assert contour_shape[1] == 1


def test_plantcv_within_frame():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_within_frame")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    mask_ib = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
    mask_oob = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK_OOB), -1)
    in_bounds_ib = pcv.within_frame(mask=mask_ib, border_width=1, label="prefix")
    in_bounds_oob = pcv.within_frame(mask=mask_oob, border_width=1)
    assert (in_bounds_ib is True and in_bounds_oob is False)


def test_plantcv_within_frame_bad_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_within_frame")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    grayscale_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    with pytest.raises(RuntimeError):
        _ = pcv.within_frame(grayscale_img)


def test_plantcv_opening():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_closing")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
    bin_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug=None
    pcv.params.debug = None
    _ = pcv.opening(gray_img)
    _ = pcv.opening(bin_img, np.ones((4, 4), np.uint8))
    filtered_img = pcv.opening(bin_img)
    assert np.sum(filtered_img) == 16184595


def test_plantcv_opening_bad_input():
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.opening(rgb_img)


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
    _ = pcv.output_mask(img=img, mask=mask, filename='test.png', outdir=None, mask_only=False)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.output_mask(img=img, mask=mask, filename='test.png', outdir=cache_dir, mask_only=False)
    _ = pcv.output_mask(img=img_color, mask=mask, filename='test.png', outdir=None, mask_only=False)
    # Remove tmp files in working direcctory
    shutil.rmtree("ori-images")
    shutil.rmtree("mask-images")
    # Test with debug = None
    pcv.params.debug = None
    imgpath, maskpath, analysis_images = pcv.output_mask(img=img, mask=mask, filename='test.png',
                                                         outdir=cache_dir, mask_only=False)
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


def test_plantcv_rectangle_mask():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_rectangle_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    img_color = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.rectangle_mask(img=img, p1=(0, 0), p2=(2454, 2056), color="white")
    _ = pcv.rectangle_mask(img=img_color, p1=(0, 0), p2=(2454, 2056), color="gray")
    masked, hist, contour, heir = pcv.rectangle_mask(img=img, p1=(0, 0), p2=(2454, 2056), color="black")
    maskedsum = np.sum(masked)
    imgsum = np.sum(img)
    assert maskedsum < imgsum


def test_plantcv_rectangle_mask_bad_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_rectangle_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = None
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.rectangle_mask(img=img, p1=(0, 0), p2=(2454, 2056), color="whit")


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

    # Test with debug = None
    pcv.params.debug = None
    images = pcv.report_size_marker_area(img=img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy, marker='detect',
                                         objcolor='light', thresh_channel='s', thresh=120)
    pcv.outputs.clear()
    assert len(images) != 0


def test_plantcv_report_size_marker_define():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MARKER), -1)
    # ROI contour
    roi_contour = [np.array([[[3550, 850]], [[3550, 1349]], [[4049, 1349]], [[4049, 850]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)

    # Test with debug = None
    pcv.params.debug = None
    images = pcv.report_size_marker_area(img=img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy, marker='define',
                                         objcolor='light', thresh_channel='s', thresh=120)
    assert len(images) != 0


def test_plantcv_report_size_marker_grayscale_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # ROI contour
    roi_contour = [np.array([[[0, 0]], [[0, 49]], [[49, 49]], [[49, 0]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)

    # Test with debug = None
    pcv.params.debug = None
    images = pcv.report_size_marker_area(img=img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy, marker='define',
                                         objcolor='light', thresh_channel='s', thresh=120)
    assert len(images) != 0


def test_plantcv_report_size_marker_bad_marker_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MARKER), -1)
    # ROI contour
    roi_contour = [np.array([[[3550, 850]], [[3550, 1349]], [[4049, 1349]], [[4049, 850]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    with pytest.raises(RuntimeError):
        _ = pcv.report_size_marker_area(img=img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy, marker='none',
                                        objcolor='light', thresh_channel='s', thresh=120)


def test_plantcv_report_size_marker_bad_threshold_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MARKER), -1)
    # ROI contour
    roi_contour = [np.array([[[3550, 850]], [[3550, 1349]], [[4049, 1349]], [[4049, 850]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    with pytest.raises(RuntimeError):
        _ = pcv.report_size_marker_area(img=img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy, marker='detect',
                                        objcolor='light', thresh_channel=None, thresh=120)


def test_plantcv_rgb2gray_cmyk():
    # Test with debug = None
    pcv.params.debug = None
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    c = pcv.rgb2gray_cmyk(rgb_img=img, channel="c")
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert all([i == j] for i, j in zip(np.shape(c), TEST_GRAY_DIM))


def test_plantcv_rgb2gray_cmyk_bad_channel():
    # Test with debug = None
    pcv.params.debug = None
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        # Channel S is not in CMYK
        _ = pcv.rgb2gray_cmyk(rgb_img=img, channel="s")


def test_plantcv_rgb2gray_hsv():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_rgb2gray_hsv")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
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
    roi_contour_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_ROI_CONTOUR), encoding="latin1")
    roi_contour = [roi_contour_npz[arr_n] for arr_n in roi_contour_npz]
    roi_hierarchy_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_ROI_HIERARCHY), encoding="latin1")
    roi_hierarchy = roi_hierarchy_npz['arr_0']
    object_contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_CONTOURS), encoding="latin1")
    object_contours = [object_contours_npz[arr_n] for arr_n in object_contours_npz]
    object_hierarchy_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_HIERARCHY), encoding="latin1")
    object_hierarchy = object_hierarchy_npz['arr_0']
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.roi_objects(img=img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy,
                        object_contour=object_contours, obj_hierarchy=object_hierarchy, roi_type="largest")
    _ = pcv.roi_objects(img=img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy,
                        object_contour=object_contours, obj_hierarchy=object_hierarchy, roi_type="cutto")
    # Test with debug = None
    kept_contours, kept_hierarchy, mask, area = pcv.roi_objects(img=img, roi_contour=roi_contour,
                                                                roi_hierarchy=roi_hierarchy,
                                                                object_contour=object_contours,
                                                                obj_hierarchy=object_hierarchy, roi_type="partial")
    # Assert that the contours were filtered as expected
    assert len(kept_contours) == 9


def test_plantcv_roi_objects_bad_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    roi_contour_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_ROI_CONTOUR), encoding="latin1")
    roi_contour = [roi_contour_npz[arr_n] for arr_n in roi_contour_npz]
    roi_hierarchy_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_ROI_HIERARCHY), encoding="latin1")
    roi_hierarchy = roi_hierarchy_npz['arr_0']
    object_contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_CONTOURS), encoding="latin1")
    object_contours = [object_contours_npz[arr_n] for arr_n in object_contours_npz]
    object_hierarchy_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_HIERARCHY), encoding="latin1")
    object_hierarchy = object_hierarchy_npz['arr_0']
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
    roi_contour_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_ROI_CONTOUR), encoding="latin1")
    roi_contour = [roi_contour_npz[arr_n] for arr_n in roi_contour_npz]
    roi_hierarchy_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_ROI_HIERARCHY), encoding="latin1")
    roi_hierarchy = roi_hierarchy_npz['arr_0']
    object_contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_CONTOURS), encoding="latin1")
    object_contours = [object_contours_npz[arr_n] for arr_n in object_contours_npz]
    object_hierarchy_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_HIERARCHY), encoding="latin1")
    object_hierarchy = object_hierarchy_npz['arr_0']
    pcv.params.debug = None
    kept_contours, kept_hierarchy, mask, area = pcv.roi_objects(img=img, roi_type="partial", roi_contour=roi_contour,
                                                                roi_hierarchy=roi_hierarchy,
                                                                object_contour=object_contours,
                                                                obj_hierarchy=object_hierarchy)
    # Assert that the contours were filtered as expected
    assert len(kept_contours) == 9


def test_plantcv_scale_features():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_scale_features")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    # test with debug = 'plot' to cover plotting logic
    pcv.params.debug = 'plot'
    _ = pcv.scale_features(obj=obj_contour, mask=mask, points=TEST_ACUTE_RESULT, line_position='NA')
    # Test with debug = None
    pcv.params.debug = None
    points_rescaled, centroid_rescaled, bottomline_rescaled = pcv.scale_features(obj=obj_contour, mask=mask,
                                                                                 points=TEST_ACUTE_RESULT,
                                                                                 line_position=50)
    assert len(points_rescaled) == 23


def test_plantcv_scale_features_bad_input():
    mask = np.array([])
    obj_contour = np.array([])
    pcv.params.debug = None
    result = pcv.scale_features(obj=obj_contour, mask=mask, points=TEST_ACUTE_RESULT, line_position=50)
    assert all([i == j] for i, j in zip(result, [("NA", "NA"), ("NA", "NA"), ("NA", "NA")]))


def test_plantcv_scharr_filter():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_scharr_filter")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
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
    pcv.params.debug = None
    _ = pcv.shift_img(img=img, number=300, side="bottom")
    _ = pcv.shift_img(img=img, number=300, side="right")
    _ = pcv.shift_img(img=mask, number=300, side="left")
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


def test_plantcv_shift_img_bad_side_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _ = pcv.shift_img(img=img, number=300, side="starboard")


def test_plantcv_sobel_filter():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_sobel_filter")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = None
    pcv.params.debug = None
    sobel_img = pcv.sobel_filter(gray_img=img, dx=1, dy=0, ksize=1)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(sobel_img), TEST_GRAY_DIM))


def test_plantcv_stdev_filter():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_sobel_filter")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY_SMALL), -1)
    pcv.params.debug = None
    filter_img = pcv.stdev_filter(img=img, ksize=11)
    assert (np.shape(filter_img) == np.shape(img))


def test_plantcv_watershed_segmentation():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_watershed_segmentation")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_CROPPED))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_CROPPED_MASK), -1)
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.watershed_segmentation(rgb_img=img, mask=mask, distance=10, label='prefix')
    assert pcv.outputs.observations['prefix']['estimated_object_count']['value'] > 9


def test_plantcv_white_balance_gray_16bit():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_white_balance_gray_16bit")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK), -1)
    # Test without an ROI
    pcv.params.debug = None
    _ = pcv.white_balance(img=img, mode='max', roi=None)
    # Test with debug = None
    white_balanced = pcv.white_balance(img=img, mode='hist', roi=(5, 5, 80, 80))
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
    # Test without an ROI
    pcv.params.debug = None
    _ = pcv.white_balance(img=img, mode='max', roi=None)
    # Test with debug = None
    white_balanced = pcv.white_balance(img=img, mode='hist', roi=(5, 5, 80, 80))
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
    pcv.params.debug = None
    # Test without an ROI
    _ = pcv.white_balance(img=img, mode='max', roi=None)
    # Test with debug = None
    white_balanced = pcv.white_balance(img=img, mode='hist', roi=(5, 5, 80, 80))
    imgavg = np.average(img)
    balancedavg = np.average(white_balanced)
    assert balancedavg != imgavg


@pytest.mark.parametrize("mode, roi", [['hist', (5, 5, 5, 5, 5)],  # too many points
                                       ['hist', (5., 5, 5, 5)],  # not all integers
                                       ['histogram', (5, 5, 80, 80)]])  # bad mode
def test_plantcv_white_balance_bad_input(mode, roi):
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK), -1)
    # Test with debug = None
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _ = pcv.white_balance(img=img, mode=mode, roi=roi)


def test_plantcv_x_axis_pseudolandmarks():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_x_axis_pseudolandmarks_debug")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img, label="prefix")
    _ = pcv.x_axis_pseudolandmarks(obj=np.array([[0, 0], [0, 0]]), mask=np.array([[0, 0], [0, 0]]), img=img)
    _ = pcv.x_axis_pseudolandmarks(obj=np.array(([[89, 222]], [[252, 39]], [[89, 207]])),
                                   mask=np.array(([[42, 161]], [[2, 47]], [[211, 222]])), img=img)

    _ = pcv.x_axis_pseudolandmarks(obj=(), mask=mask, img=img)
    top, bottom, center_v = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    pcv.outputs.clear()
    assert all([all([i == j] for i, j in zip(np.shape(top), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(bottom), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(center_v), (20, 1, 2)))])


def test_plantcv_x_axis_pseudolandmarks_small_obj():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL_PLANT))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL_PLANT), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR_SMALL_PLANT), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    # Test with debug = None
    pcv.params.debug = None
    _, _, _ = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
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
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.y_axis_pseudolandmarks(obj=[], mask=mask, img=img)
    _ = pcv.y_axis_pseudolandmarks(obj=(), mask=mask, img=img)
    _ = pcv.y_axis_pseudolandmarks(obj=np.array(([[89, 222]], [[252, 39]], [[89, 207]])),
                                   mask=np.array(([[42, 161]], [[2, 47]], [[211, 222]])), img=img)
    _ = pcv.y_axis_pseudolandmarks(obj=np.array(([[21, 11]], [[159, 155]], [[237, 11]])),
                                   mask=np.array(([[38, 54]], [[144, 169]], [[81, 137]])), img=img)
    left, right, center_h = pcv.y_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    pcv.outputs.clear()
    assert all([all([i == j] for i, j in zip(np.shape(left), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(right), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(center_h), (20, 1, 2)))])


def test_plantcv_y_axis_pseudolandmarks_small_obj():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_y_axis_pseudolandmarks_debug")
    os.mkdir(cache_dir)
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL_PLANT))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL_PLANT), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR_SMALL_PLANT), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    pcv.params.debug = None
    _, _, _ = pcv.y_axis_pseudolandmarks(obj=[], mask=mask, img=img)
    pcv.outputs.clear()
    left, right, center_h = pcv.y_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    pcv.outputs.clear()
    assert all([all([i == j] for i, j in zip(np.shape(left), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(right), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(center_h), (20, 1, 2)))])


def test_plantcv_y_axis_pseudolandmarks_bad_input():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_y_axis_pseudolandmarks_debug")
    os.mkdir(cache_dir)
    img = np.array([])
    mask = np.array([])
    obj_contour = np.array([])
    pcv.params.debug = None
    result = pcv.y_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    pcv.outputs.clear()
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


@pytest.mark.parametrize("alg, min_size, max_size", [['DBSCAN', 10, None],
                                                     ['OPTICS', 100, 5000]]
                         )
def test_plantcv_spatial_clustering(alg, min_size, max_size):
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_spatial_clustering_dbscan")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI_MASK), -1)
    pcv.params.debug = None
    spmask = pcv.spatial_clustering(img, algorithm=alg, min_cluster_size=min_size, max_distance=max_size)
    assert len(spmask[1]) == 2


def test_plantcv_spatial_clustering_badinput():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI_MASK), -1)
    pcv.params.debug = None
    with pytest.raises(NameError):
        _ = pcv.spatial_clustering(img, algorithm="Hydra", min_cluster_size=5, max_distance=100)


# ####################################
# Tests for the morphology subpackage
# ####################################
def test_plantcv_morphology_segment_curvature():
    # Clear previous outputs
    pcv.outputs.clear()
    pcv.params.debug = None
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    _ = pcv.morphology.segment_curvature(segmented_img, seg_objects)
    assert len(pcv.outputs.observations['default']['segment_curvature']['value']) == 22


def test_plantcv_morphology_check_cycles():
    # Clear previous outputs
    pcv.outputs.clear()
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    pcv.params.debug = None
    _ = pcv.morphology.check_cycles(mask)
    assert pcv.outputs.observations['default']['num_cycles']['value'] == 1


def test_plantcv_morphology_find_branch_pts():
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = None
    branches = pcv.morphology.find_branch_pts(skel_img=skeleton, mask=mask, label="prefix")
    assert np.sum(branches) == 9435


def test_plantcv_morphology_find_branch_pts_no_mask():
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = None
    branches = pcv.morphology.find_branch_pts(skel_img=skeleton)
    assert np.sum(branches) == 9435


def test_plantcv_morphology_find_tips():
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = None
    tips = pcv.morphology.find_tips(skel_img=skeleton, mask=mask, label="prefix")
    assert np.sum(tips) == 9435


def test_plantcv_morphology_find_tips_no_mask():
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = None
    tips = pcv.morphology.find_tips(skel_img=skeleton)
    assert np.sum(tips) == 9435


def test_plantcv_morphology_prune():
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = None
    pruned_img, _, _ = pcv.morphology.prune(skel_img=skeleton, size=1, mask=skeleton)
    assert np.sum(pruned_img) < np.sum(skeleton)


def test_plantcv_morphology_prune_no_mask():
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = None
    pruned_img, _, _ = pcv.morphology.prune(skel_img=skeleton, size=3)
    assert np.sum(pruned_img) < np.sum(skeleton)


def test_plantcv_morphology_prune_size0():
    pcv.params.debug = None
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pruned_img, _, _ = pcv.morphology.prune(skel_img=skeleton, size=0)
    assert np.sum(pruned_img) == np.sum(skeleton)


def test_plantcv_morphology_iterative_prune():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_pruned")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pruned_img = pcv.morphology._iterative_prune(skel_img=skeleton, size=3)
    assert np.sum(pruned_img) < np.sum(skeleton)


def test_plantcv_morphology_segment_skeleton():
    pcv.params.debug = None
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    _ = pcv.morphology.segment_skeleton(skel_img=skeleton, mask=mask)
    segmented_img, segment_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    assert len(segment_objects) == 73


def test_plantcv_morphology_fill_segments():
    # Clear previous outputs
    pcv.outputs.clear()
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    obj_dic = np.load(os.path.join(TEST_DATA, TEST_SKELETON_OBJECTS))
    obj = []
    for key, val in obj_dic.items():
        obj.append(val)
    pcv.params.debug = None
    _ = pcv.morphology.fill_segments(mask, obj)
    tests = [pcv.outputs.observations['default']['segment_area']['value'][42] == 5529,
             pcv.outputs.observations['default']['segment_area']['value'][20] == 5057,
             pcv.outputs.observations['default']['segment_area']['value'][49] == 3323]
    assert all(tests)


def test_plantcv_morphology_fill_segments_with_stem():
    # Clear previous outputs
    pcv.outputs.clear()
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    obj_dic = np.load(os.path.join(TEST_DATA, TEST_SKELETON_OBJECTS))
    obj = []
    for key, val in obj_dic.items():
        obj.append(val)

    stem_obj = obj[0:4]
    pcv.params.debug = None
    _ = pcv.morphology.fill_segments(mask, obj, stem_obj)
    num_objects = len(pcv.outputs.observations['default']['leaf_area']['value'])
    assert num_objects == 69


def test_plantcv_morphology_segment_angle():
    # Clear previous outputs
    pcv.outputs.clear()
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    pcv.params.debug = None
    segmented_img, segment_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    _ = pcv.morphology.segment_angle(segmented_img=segmented_img, objects=segment_objects)
    assert len(pcv.outputs.observations['default']['segment_angle']['value']) == 22


def test_plantcv_morphology_segment_angle_overflow():
    # Clear previous outputs
    pcv.outputs.clear()
    # Don't prune, would usually give overflow error without extra if statement in segment_angle
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    segmented_img, segment_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    _ = pcv.morphology.segment_angle(segmented_img, segment_objects)
    assert len(pcv.outputs.observations['default']['segment_angle']['value']) == 73


def test_plantcv_morphology_segment_euclidean_length():
    # Clear previous outputs
    pcv.outputs.clear()
    pcv.params.debug = None
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    segmented_img, segment_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    _ = pcv.morphology.segment_euclidean_length(segmented_img, segment_objects)
    assert len(pcv.outputs.observations['default']['segment_eu_length']['value']) == 22


def test_plantcv_morphology_segment_euclidean_length_bad_input():
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    skel = pcv.morphology.skeletonize(mask=mask)
    pcv.params.debug = None
    segmented_img, segment_objects = pcv.morphology.segment_skeleton(skel_img=skel)
    with pytest.raises(RuntimeError):
        _ = pcv.morphology.segment_euclidean_length(segmented_img, segment_objects)


def test_plantcv_morphology_segment_path_length():
    # Clear previous outputs
    pcv.outputs.clear()
    pcv.params.debug = None
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    segmented_img, segment_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    _ = pcv.morphology.segment_path_length(segmented_img, segment_objects)
    assert len(pcv.outputs.observations['default']['segment_path_length']['value']) == 22


def test_plantcv_morphology_skeletonize():
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    input_skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = None
    skeleton = pcv.morphology.skeletonize(mask=mask)
    arr = np.array(skeleton == input_skeleton)
    assert arr.all()


def test_plantcv_morphology_segment_sort():
    pcv.params.debug = None
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    leaf_obj, stem_obj = pcv.morphology.segment_sort(skeleton, seg_objects, mask=skeleton)
    assert len(leaf_obj) == 36


def test_plantcv_morphology_segment_sort_no_mask():
    pcv.params.debug = None
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    leaf_obj, stem_obj = pcv.morphology.segment_sort(skeleton, seg_objects)
    assert len(leaf_obj) == 36


def test_plantcv_morphology_segment_tangent_angle():
    # Clear previous outputs
    pcv.outputs.clear()
    pcv.params.debug = None
    skel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    objects = np.load(os.path.join(TEST_DATA, TEST_SKELETON_OBJECTS), encoding="latin1")
    objs = [objects[arr_n] for arr_n in objects]
    _ = pcv.morphology.segment_tangent_angle(skel, objs, 2)
    assert len(pcv.outputs.observations['default']['segment_tangent_angle']['value']) == 73


def test_plantcv_morphology_segment_id():
    pcv.params.debug = None
    skel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    objects = np.load(os.path.join(TEST_DATA, TEST_SKELETON_OBJECTS), encoding="latin1")
    objs = [objects[arr_n] for arr_n in objects]
    _, labeled_img = pcv.morphology.segment_id(skel, objs, mask=skel)
    assert np.sum(labeled_img) > np.sum(skel)


def test_plantcv_morphology_segment_id_no_mask():
    pcv.params.debug = None
    skel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    objects = np.load(os.path.join(TEST_DATA, TEST_SKELETON_OBJECTS), encoding="latin1")
    objs = [objects[arr_n] for arr_n in objects]
    _, labeled_img = pcv.morphology.segment_id(skel, objs)
    assert np.sum(labeled_img) > np.sum(skel)


def test_plantcv_morphology_segment_insertion_angle():
    # Clear previous outputs
    pcv.outputs.clear()
    pcv.params.debug = None
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pruned, _, _ = pcv.morphology.prune(skel_img=skeleton, size=6)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=pruned)
    leaf_obj, stem_obj = pcv.morphology.segment_sort(pruned, seg_objects)
    _ = pcv.morphology.segment_insertion_angle(pruned, segmented_img, leaf_obj, stem_obj, 3, label="prefix")
    _ = pcv.morphology.segment_insertion_angle(pruned, segmented_img, leaf_obj, stem_obj, 10)
    assert pcv.outputs.observations['default']['segment_insertion_angle']['value'][:6] == ['NA', 'NA', 'NA',
                                                                                           24.956918822001636,
                                                                                           50.7313343343401,
                                                                                           56.427712102130734]


def test_plantcv_morphology_segment_insertion_angle_bad_stem():
    pcv.params.debug = None
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pruned, _, _ = pcv.morphology.prune(skel_img=skeleton, size=5)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=pruned)
    leaf_obj, stem_obj = pcv.morphology.segment_sort(pruned, seg_objects)
    stem_obj = [leaf_obj[0], leaf_obj[10]]
    with pytest.raises(RuntimeError):
        _ = pcv.morphology.segment_insertion_angle(pruned, segmented_img, leaf_obj, stem_obj, 10)


def test_plantcv_morphology_segment_combine():
    pcv.params.debug = None
    skel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=skel)
    # Test with list of IDs input
    _, new_objects = pcv.morphology.segment_combine([0, 1], seg_objects, skel)
    assert len(new_objects) + 1 == len(seg_objects)


def test_plantcv_morphology_segment_combine_lists():
    pcv.params.debug = None
    skel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=skel)
    # Test with list of lists input
    _, new_objects = pcv.morphology.segment_combine([[0, 1, 2], [3, 4]], seg_objects, skel)
    assert len(new_objects) + 3 == len(seg_objects)


def test_plantcv_morphology_segment_combine_bad_input():
    pcv.params.debug = None
    skel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=skel)
    with pytest.raises(RuntimeError):
        _, new_objects = pcv.morphology.segment_combine([0.5, 1.5], seg_objects, skel)


def test_plantcv_morphology_analyze_stem():
    pcv.params.debug = "plot"
    # Clear previous outputs
    pcv.outputs.clear()
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pruned, segmented_img, _ = pcv.morphology.prune(skel_img=skeleton, size=6)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=pruned)
    leaf_obj, stem_obj = pcv.morphology.segment_sort(pruned, seg_objects)
    _ = pcv.morphology.analyze_stem(rgb_img=segmented_img, stem_objects=stem_obj)
    assert pcv.outputs.observations['default']['stem_angle']['value'] == -12.531776428222656


def test_plantcv_morphology_analyze_stem_bad_angle():
    pcv.params.debug = None
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pruned, _, _ = pcv.morphology.prune(skel_img=skeleton, size=5)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=pruned)
    _, _ = pcv.morphology.segment_sort(pruned, seg_objects)
    # print([stem_obj[3]])
    # stem_obj = [stem_obj[3]]
    stem_obj = [[[[1116, 1728]], [[1116, 1]]]]
    pcv.params.debug = "plot"
    _ = pcv.morphology.analyze_stem(rgb_img=segmented_img, stem_objects=stem_obj)
    assert pcv.outputs.observations['default']['stem_angle']['value'] == 22877334.0


# ########################################
# Tests for the photosynthesis subpackage
# ########################################
def test_plantcv_photosynthesis_read_dat():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_photosynthesis_read_dat")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = "plot"
    fluor_filename = os.path.join(FLUOR_TEST_DATA, FLUOR_IMG)
    _, _, _ = pcv.photosynthesis.read_cropreporter(filename=fluor_filename)
    pcv.params.debug = "print"
    fdark, fmin, fmax = pcv.photosynthesis.read_cropreporter(filename=fluor_filename)
    assert np.sum(fmin) < np.sum(fmax)


def test_plantcv_photosynthesis_analyze_fvfm():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_fvfm")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # filename = os.path.join(cache_dir, 'plantcv_fvfm_hist.png')
    # Read in test data
    fdark = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FDARK), -1)
    fmin = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMIN), -1)
    fmax = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMAX), -1)
    fmask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMASK), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.photosynthesis.analyze_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=fmask, bins=1000, label="prefix")
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    fvfm_images = pcv.photosynthesis.analyze_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=fmask, bins=1000)
    assert len(fvfm_images) != 0


def test_plantcv_photosynthesis_analyze_fvfm_print_analysis_results():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_fvfm")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    fdark = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FDARK), -1)
    fmin = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMIN), -1)
    fmax = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMAX), -1)
    fmask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMASK), -1)
    _ = pcv.photosynthesis.analyze_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=fmask, bins=1000)
    result_file = os.path.join(cache_dir, "results.txt")
    pcv.print_results(result_file)
    pcv.outputs.clear()
    assert os.path.exists(result_file)


def test_plantcv_photosynthesis_analyze_fvfm_bad_fdark():
    # Clear previous outputs
    pcv.outputs.clear()
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_fvfm")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    fdark = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FDARK), -1)
    fmin = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMIN), -1)
    fmax = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMAX), -1)
    fmask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMASK), -1)
    _ = pcv.photosynthesis.analyze_fvfm(fdark=fdark + 3000, fmin=fmin, fmax=fmax, mask=fmask, bins=1000)
    check = pcv.outputs.observations['default']['fdark_passed_qc']['value'] is False
    assert check


def test_plantcv_photosynthesis_analyze_fvfm_bad_input():
    fdark = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    fmin = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMIN), -1)
    fmax = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMAX), -1)
    fmask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMASK), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.photosynthesis.analyze_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=fmask, bins=1000)


# ###################################
# Tests for the visualize subpackage
# ###################################
def test_plantcv_visualize_auto_threshold_methods_bad_input():
    # Test with debug = None
    pcv.params.debug = None
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.auto_threshold_methods(gray_img=img)


def test_plantcv_visualize_auto_threshold_methods():
    # Test with debug = None
    pcv.params.debug = None
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    labeled_imgs = pcv.visualize.auto_threshold_methods(gray_img=img)
    assert len(labeled_imgs) == 5 and np.shape(labeled_imgs[0])[0] == np.shape(img)[0]


@pytest.mark.parametrize("debug,axes", [["print", True], ["plot", False]])
def test_plantcv_visualize_pseudocolor(debug, axes, tmpdir):
    # Create a tmp directory
    cache_dir = tmpdir.mkdir("sub")
    pcv.params.debug_outdir = cache_dir
    # Input image
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    r, c = img.shape
    # generate 200 "bad" pixels
    mask_bad = np.zeros((r, c), dtype=np.uint8)
    mask_bad = np.reshape(mask_bad, (-1, 1))
    mask_bad[0:100] = 255
    mask_bad = np.reshape(mask_bad, (r, c))
    # Debug mode
    pcv.params.debug = debug
    pseudo_img = pcv.visualize.pseudocolor(gray_img=img, mask=None, title="Pseudocolored image", axes=axes,
                                           bad_mask=mask_bad)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(pseudo_img), TEST_BINARY_DIM))


@pytest.mark.parametrize("bkgrd,axes,pad", [["image", True, "auto"], ["white", False, 1], ["black", True, "auto"]])
def test_plantcv_visualize_pseudocolor_mask(bkgrd, axes, pad):
    # Test with debug = None
    pcv.params.debug = None
    # Input image
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Input mask
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Input contours
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    r, c = img.shape
    # generate 200 "bad" pixels
    mask_bad = np.zeros((r, c), dtype=np.uint8)
    mask_bad = np.reshape(mask_bad, (-1, 1))
    mask_bad[0:100] = 255
    mask_bad = np.reshape(mask_bad, (r, c))
    pseudo_img = pcv.visualize.pseudocolor(gray_img=img, obj=obj_contour, mask=mask, background=bkgrd,
                                           bad_mask=mask_bad, title="Pseudocolored image", axes=axes, obj_padding=pad)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(pseudo_img), TEST_BINARY_DIM)):
        assert 1
    else:
        assert 0


def test_plantcv_visualize_pseudocolor_bad_input():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_pseudocolor")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.pseudocolor(gray_img=img)


def test_plantcv_visualize_pseudocolor_bad_background():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_pseudocolor_bad_background")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.pseudocolor(gray_img=img, mask=mask, background="pink")


def test_plantcv_visualize_pseudocolor_bad_padding():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_pseudocolor_bad_background")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.pseudocolor(gray_img=img, mask=mask, obj=obj_contour, obj_padding="pink")


def test_plantcv_visualize_pseudocolor_bad_mask():
    # Test with debug = None
    pcv.params.debug = None


@pytest.mark.parametrize('colors', [['red', 'blue'], [(0, 0, 255), (255, 0, 0)]])
def test_plantcv_visualize_colorize_masks(colors):
    # Test with debug = None
    pcv.params.debug = None
    # Create test data
    mask1 = np.zeros((100, 100), dtype=np.uint8)
    mask2 = np.copy(mask1)
    mask1[0:50, 0:50] = 255
    mask2[50:100, 50:100] = 255
    colored_img = pcv.visualize.colorize_masks(masks=[mask1, mask2], colors=colors)
    # Assert that the output image has the dimensions of the input image
    assert not np.average(colored_img) == 0


def test_plantcv_visualize_colorize_masks_bad_input_empty():
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.colorize_masks(masks=[], colors=[])


def test_plantcv_visualize_colorize_masks_bad_input_mismatch_number():
    # Create test data
    mask1 = np.zeros((100, 100), dtype=np.uint8)
    mask2 = np.copy(mask1)
    mask1[0:50, 0:50] = 255
    mask2[50:100, 50:100] = 255
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.colorize_masks(masks=[mask1, mask2], colors=['red', 'green', 'blue'])


def test_plantcv_visualize_colorize_masks_bad_color_input():
    # Create test data
    mask1 = np.zeros((100, 100), dtype=np.uint8)
    mask2 = np.copy(mask1)
    mask1[0:50, 0:50] = 255
    mask2[50:100, 50:100] = 255
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.colorize_masks(masks=[mask1, mask2], colors=['red', 1.123])


def test_plantcv_visualize_colorize_label_img():
    label_img = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    pcv.params.debug = None
    colored_img = pcv.visualize.colorize_label_img(label_img)
    assert (colored_img.shape[0:-1] == label_img.shape) and colored_img.shape[-1] == 3


@pytest.mark.parametrize("bins,lb,ub,title", [[200, 0, 255, "Include Title"], [100, None, None, None]])
def test_plantcv_visualize_histogram(bins, lb, ub, title):
    # Test with debug = None
    pcv.params.debug = None
    # Read test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    fig_hist, hist_df = pcv.visualize.histogram(img=img, mask=mask, bins=bins, lower_bound=lb, upper_bound=ub,
                                                title=title, hist_data=True)
    assert all([isinstance(fig_hist, ggplot), isinstance(hist_df, pd.core.frame.DataFrame)])


def test_plantcv_visualize_histogram_no_mask():
    # Test with debug = None
    pcv.params.debug = None
    # Read test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    fig_hist = pcv.visualize.histogram(img=img, mask=None)
    assert isinstance(fig_hist, ggplot)


def test_plantcv_visualize_histogram_rgb_img():
    # Test with debug = None
    pcv.params.debug = None
    # Test RGB input image
    img_rgb = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    fig_hist = pcv.visualize.histogram(img=img_rgb)
    assert isinstance(fig_hist, ggplot)


def test_plantcv_visualize_histogram_multispectral_img():
    # Test with debug = None
    pcv.params.debug = None
    # Test multi-spectral image
    img_rgb = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    img_multi = np.concatenate((img_rgb, img_rgb), axis=2)
    fig_hist = pcv.visualize.histogram(img=img_multi)
    assert isinstance(fig_hist, ggplot)


def test_plantcv_visualize_histogram_no_img():
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.histogram(img=None)


def test_plantcv_visualize_histogram_array():
    # Read test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.histogram(img=img[0, :])


@pytest.mark.parametrize("wavelengths", [[], [390, 500, 640, 992, 990]])
def test_plantcv_visualize_hyper_histogram(wavelengths):
    # Test with debug = None
    pcv.params.debug = None

    # Read in test data
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array = pcv.hyperspectral.read_data(filename=spectral_filename)
    mask = np.ones((array.lines, array.samples))

    fig_hist = pcv.visualize.hyper_histogram(array, mask, wvlengths=wavelengths, title="Hyper Histogram Test")
    assert isinstance(fig_hist, ggplot)


def test_plantcv_visualize_hyper_histogram_wv_out_range():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array = pcv.hyperspectral.read_data(filename=spectral_filename)
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.hyper_histogram(array, wvlengths=[200,  550])


def test_plantcv_visualize_hyper_histogram_extreme_wvs():
    # Test with debug = None
    pcv.params.debug = None

    # Read in test data
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array = pcv.hyperspectral.read_data(filename=spectral_filename)
    mask = np.ones((array.lines, array.samples))

    wv_keys = list(array.wavelength_dict.keys())
    wavelengths = [250, 270, 1800, 2500]
    # change first 4 keys
    for (k_, k) in zip(wv_keys[0:5], wavelengths):
        array.wavelength_dict[k] = array.wavelength_dict.pop(k_)
    array.min_wavelength, array.max_wavelength = min(array.wavelength_dict), max(array.wavelength_dict)
    fig_hist = pcv.visualize.hyper_histogram(array, mask, wvlengths=wavelengths)
    assert isinstance(fig_hist, ggplot)


def test_plantcv_visualize_clustered_contours():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_plot_hist")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_VISUALIZE_BACKGROUND), -1)
    roi_objects = np.load(os.path.join(TEST_DATA, TEST_INPUT_VISUALIZE_CONTOUR), encoding="latin1")
    hierarchy = np.load(os.path.join(TEST_DATA, TEST_INPUT_VISUALIZE_HIERARCHY), encoding="latin1")
    cluster_i = np.load(os.path.join(TEST_DATA, TEST_INPUT_VISUALIZE_CLUSTERS), encoding="latin1")
    objs = [roi_objects[arr_n] for arr_n in roi_objects]
    obj_hierarchy = hierarchy['arr_0']
    cluster = [cluster_i[arr_n] for arr_n in cluster_i]
    # Test in plot mode
    pcv.params.debug = "plot"
    # Reset the saved color scale (can be saved between tests)
    pcv.params.saved_color_scale = None
    _ = pcv.visualize.clustered_contours(img=img1, grouped_contour_indices=cluster, roi_objects=objs,
                                         roi_obj_hierarchy=obj_hierarchy, bounding=False)
    # Test in print mode
    pcv.params.debug = "print"
    # Reset the saved color scale (can be saved between tests)
    pcv.params.saved_color_scale = None
    cluster_img = pcv.visualize.clustered_contours(img=img, grouped_contour_indices=cluster, roi_objects=objs,
                                                   roi_obj_hierarchy=obj_hierarchy, nrow=2, ncol=2, bounding=True)
    assert np.sum(cluster_img) > np.sum(img)


def test_plantcv_visualize_colorspaces():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_plot_hist")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    pcv.params.debug = "plot"
    vis_img_small = pcv.visualize.colorspaces(rgb_img=img, original_img=False)
    pcv.params.debug = "print"
    vis_img = pcv.visualize.colorspaces(rgb_img=img)
    assert np.shape(vis_img)[1] > (np.shape(img)[1]) and np.shape(vis_img_small)[1] > (np.shape(img)[1])


def test_plantcv_visualize_colorspaces_bad_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_plot_hist")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.colorspaces(rgb_img=img)


def test_plantcv_visualize_overlay_two_imgs():
    pcv.params.debug = None
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_visualize_overlay_two_imgs")
    os.mkdir(cache_dir)
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    img2 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY))

    pcv.params.debug = None
    out_img = pcv.visualize.overlay_two_imgs(img1=img1, img2=img2)
    sample_pt1 = img1[1445, 1154]
    sample_pt2 = img2[1445, 1154]
    sample_pt3 = out_img[1445, 1154]
    pred_rgb = (sample_pt1 * 0.5) + (sample_pt2 * 0.5)
    pred_rgb = pred_rgb.astype(np.uint8)
    assert np.array_equal(sample_pt3, pred_rgb)


def test_plantcv_visualize_overlay_two_imgs_grayscale():
    pcv.params.debug = None
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_visualize_overlay_two_imgs_grayscale")
    os.mkdir(cache_dir)
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    out_img = pcv.visualize.overlay_two_imgs(img1=img1, img2=img2)
    sample_pt1 = np.array([255, 255, 255], dtype=np.uint8)
    sample_pt2 = np.array([255, 255, 255], dtype=np.uint8)
    sample_pt3 = out_img[1445, 1154]
    pred_rgb = (sample_pt1 * 0.5) + (sample_pt2 * 0.5)
    pred_rgb = pred_rgb.astype(np.uint8)
    assert np.array_equal(sample_pt3, pred_rgb)


def test_plantcv_visualize_overlay_two_imgs_bad_alpha():
    pcv.params.debug = None
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_visualize_overlay_two_imgs_bad_alpha")
    os.mkdir(cache_dir)
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    img2 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY))
    alpha = -1
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.overlay_two_imgs(img1=img1, img2=img2, alpha=alpha)


def test_plantcv_visualize_overlay_two_imgs_size_mismatch():
    pcv.params.debug = None
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_visualize_overlay_two_imgs_size_mismatch")
    os.mkdir(cache_dir)
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    img2 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_CROPPED))
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.overlay_two_imgs(img1=img1, img2=img2)


@pytest.mark.parametrize("num,expected", [[100, 35], [30, 33]])
def test_plantcv_visualize_size(num, expected):
    pcv.params.debug = None
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_LEAF_MASK), -1)
    visualization = pcv.visualize.obj_sizes(img=img, mask=img, num_objects=num)
    # Output unique colors are the 32 objects, the gray text, the black background, and white unlabeled leaves
    assert len(np.unique(visualization.reshape(-1, visualization.shape[2]), axis=0)) == expected


@pytest.mark.parametrize("title", ["Include Title", None])
def test_plantcv_visualize_obj_size_ecdf(title):
    pcv.params.debug = None
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
    fig_ecdf = plantcv.plantcv.visualize.obj_size_ecdf(mask=mask, title=title)
    assert isinstance(fig_ecdf, ggplot)


# ##############################
# Clean up test files
# ##############################
def teardown_function():
    shutil.rmtree(TEST_TMPDIR)
