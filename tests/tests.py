#!/usr/bin/env python

import pytest
import os
import shutil
import numpy as np
import cv2
from plantcv import plantcv as pcv
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


@pytest.mark.parametrize("num,expected", [[100, 35], [30, 33]])
def test_plantcv_visualize_size(num, expected):
    pcv.params.debug = None
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_LEAF_MASK), -1)
    visualization = pcv.visualize.obj_sizes(img=img, mask=img, num_objects=num)
    # Output unique colors are the 32 objects, the gray text, the black background, and white unlabeled leaves
    assert len(np.unique(visualization.reshape(-1, visualization.shape[2]), axis=0)) == expected


# ##############################
# Clean up test files
# ##############################
def teardown_function():
    shutil.rmtree(TEST_TMPDIR)
