#!/usr/bin/env python

import pytest
import os
import shutil
import numpy as np
import cv2
import plantcv as pcv
import plantcv.learn
# Import matplotlib and use a null Template to block plotting to screen
# This will let us test debug = "plot"
import matplotlib
matplotlib.use('Template')

TEST_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
TEST_TMPDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".cache")
TEST_COLOR_DIM = (2056, 2454, 3)
TEST_GRAY_DIM = (2056, 2454)
TEST_BINARY_DIM = TEST_GRAY_DIM
TEST_INPUT_COLOR = "input_color_img.jpg"
TEST_INPUT_GRAY = "input_gray_img.jpg"
TEST_INPUT_BINARY = "input_binary_img.png"
TEST_INPUT_ROI = "input_roi.npz"
TEST_INPUT_CONTOURS = "input_contours.npz"
TEST_VIS = "VIS_SV_0_z300_h1_g0_e85_v500_93054.png"
TEST_NIR = "NIR_SV_0_z300_h1_g0_e15000_v500_93059.png"
TEST_VIS_TV = "VIS_TV_0_z300_h1_g0_e85_v500_93054.png"
TEST_NIR_TV = "NIR_TV_0_z300_h1_g0_e15000_v500_93059.png"
TEST_INPUT_MASK = "input_mask.png"
TEST_INPUT_NIR_MASK = "input_nir.png"
TEST_INPUT_FDARK = "FLUO_TV_dark.png"
TEST_INPUT_FMIN = "FLUO_TV_min.png"
TEST_INPUT_FMAX = "FLUO_TV_max.png"
TEST_INPUT_FMASK = "FLUO_TV_MASK.png"
TEST_INTPUT_GREENMAG = "input_green-magenta.jpg"
TEST_INTPUT_MULTI = "multi_ori_image.jpg"
TEST_INPUT_MULTI_CONTOUR = "roi_objects.npz"
TEST_INPUT_ClUSTER_CONTOUR = "clusters_i.npz"
TEST_INPUT_CROPPED = 'cropped_img.jpg'
TEST_INPUT_CROPPED_MASK = 'cropped-mask.png'
TEST_INPUT_MARKER = 'seed-image.jpg'
TEST_FOREGROUND = "TEST_FOREGROUND.jpg"
TEST_BACKGROUND = "TEST_BACKGROUND.jpg"
TEST_PDFS = "naive_bayes_pdfs.txt"
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

if not os.path.exists(TEST_TMPDIR):
    os.mkdir(TEST_TMPDIR)

# ##########################
# Tests for the main package
# ##########################


def test_plantcv_acute():
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR))
    obj_contour = contours_npz['arr_0']
    # Test with debug = "print"
    _ = pcv.acute(obj=obj_contour, win=5, thresh=15, mask=mask, device=0, debug="print")
    # Test with debug = None
    device, homology_pts = pcv.acute(obj=obj_contour, win=5, thresh=15, mask=mask, device=0, debug=None)
    assert all([i == j] for i, j in zip(np.shape(homology_pts), (29, 1, 2)))


def test_plantcv_acute_vertex():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL))
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR))
    obj_contour = contours_npz['arr_0']
    # Test with debug = "print"
    _ = pcv.acute_vertex(obj=obj_contour, win=5, thresh=15, sep=5, img=img, device=0, debug="print")
    os.rename("1_acute_vertices.png", os.path.join(TEST_TMPDIR, "1_acute_vertices.png"))
    # Test with debug = "plot"
    _ = pcv.acute_vertex(obj=obj_contour, win=5, thresh=15, sep=5, img=img, device=0, debug="plot")
    # Test with debug = None
    device, acute = pcv.acute_vertex(obj=obj_contour, win=5, thresh=15, sep=5, img=img, device=0, debug=None)
    assert all([i == j] for i, j in zip(np.shape(acute), np.shape(TEST_ACUTE_RESULT)))


def test_plantcv_acute_vertex_bad_obj():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL))
    obj_contour = np.array([])
    result = pcv.acute_vertex(obj=obj_contour, win=5, thresh=15, sep=5, img=img, device=0, debug=None)
    assert all([i == j] for i, j in zip(result, [0, ("NA", "NA")]))


def test_plantcv_adaptive_threshold():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with threshold type = "mean"
    _ = pcv.adaptive_threshold(img=img, maxValue=255, thres_type="mean", object_type="light", device=0, debug=None)
    # Test with debug = "print"
    _ = pcv.adaptive_threshold(img=img, maxValue=255, thres_type="gaussian", object_type="light", device=0,
                               debug="print")
    os.rename("1_adaptive_threshold_gaussian.png", os.path.join(TEST_TMPDIR, "1_adaptive_threshold_gaussian.png"))
    # Test with debug = "plot"
    _ = pcv.adaptive_threshold(img=img, maxValue=255, thres_type="gaussian", object_type="light", device=0,
                               debug="plot")
    # Test with debug = None
    device, binary_img = pcv.adaptive_threshold(img=img, maxValue=255, thres_type="gaussian", object_type="light",
                                                device=0, debug=None)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(binary_img), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(binary_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_adaptive_threshold_incorrect_threshold_type():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.adaptive_threshold(img=img, maxValue=255, thres_type="gauss", object_type="light", device=0, debug=None)


def test_plantcv_adaptive_threshold_incorrect_object_type():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.adaptive_threshold(img=img, maxValue=255, thres_type="mean", object_type="lite", device=0, debug=None)


def test_plantcv_analyze_bound():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS))
    object_contours = contours_npz['arr_0']
    # Test with debug = "print"
    outfile = os.path.join(TEST_TMPDIR, TEST_INPUT_COLOR)
    _ = pcv.analyze_bound(img=img, imgname="img", obj=object_contours[0], mask=mask, line_position=300, device=0,
                          debug="print", filename=outfile)
    os.rename("1_boundary_on_img.jpg", os.path.join(TEST_TMPDIR, "1_boundary_on_img.jpg"))
    os.rename("1_boundary_on_white.jpg", os.path.join(TEST_TMPDIR, "1_boundary_on_white.jpg"))
    # Test with debug = "plot"
    _ = pcv.analyze_bound(img=img, imgname="img", obj=object_contours[0], mask=mask, line_position=300, device=0,
                          debug="plot", filename=False)
    # Test with debug = None
    device, boundary_header, boundary_data, boundary_img1 = pcv.analyze_bound(img=img, imgname="img",
                                                                              obj=object_contours[0], mask=mask,
                                                                              line_position=300, device=0,
                                                                              debug=None, filename=False)
    assert boundary_data[3] == 596347


def test_plantcv_analyze_color():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    outfile = os.path.join(TEST_TMPDIR, TEST_INPUT_COLOR)
    _ = pcv.analyze_color(img=img, imgname="img", mask=mask, bins=256, device=0, debug="print", hist_plot_type="all",
                          pseudo_channel="v", pseudo_bkg="img", resolution=300, filename=outfile)
    os.rename("1_img_pseudocolor.jpg", os.path.join(TEST_TMPDIR, "1_img_pseudocolor.jpg"))
    os.rename("1_all_hist.svg", os.path.join(TEST_TMPDIR, "1_all_hist.svg"))
    # Test with debug = "plot"
    _ = pcv.analyze_color(img=img, imgname="img", mask=mask, bins=256, device=0, debug="plot", hist_plot_type=None,
                          pseudo_channel="v", pseudo_bkg="img", resolution=300, filename=False)
    # Test with debug = "plot" and pseudo_bkg = "white"
    _ = pcv.analyze_color(img=img, imgname="img", mask=mask, bins=256, device=0, debug="plot", hist_plot_type=None,
                          pseudo_channel="v", pseudo_bkg="white", resolution=300, filename=False)
    # Test with debug = None
    device, color_header, color_data, analysis_images = pcv.analyze_color(img=img, imgname="img", mask=mask, bins=256,
                                                                          device=0, debug=None, hist_plot_type=None,
                                                                          pseudo_channel="v", pseudo_bkg="img",
                                                                          resolution=300, filename=False)
    assert np.sum(color_data[3]) != 0


def test_plantcv_analyze_color_incorrect_pseudo_channel():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.analyze_color(img=img, imgname="img", mask=mask, bins=256, device=0, debug="plot", hist_plot_type=None,
                              pseudo_channel="x", pseudo_bkg="white", resolution=300, filename=False)


def test_plantcv_analyze_color_incorrect_pseudo_background():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.analyze_color(img=img, imgname="img", mask=mask, bins=256, device=0, debug="plot", hist_plot_type=None,
                              pseudo_channel="v", pseudo_bkg="black", resolution=300, filename=False)


def test_plantcv_analyze_color_incorrect_hist_plot_type():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.analyze_color(img=img, imgname="img", mask=mask, bins=256, device=0, debug="plot", hist_plot_type="bgr",
                              pseudo_channel="v", pseudo_bkg="white", resolution=300, filename=False)


def test_plantcv_analyze_nir():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    outfile = os.path.join(TEST_TMPDIR, TEST_INPUT_COLOR)
    _ = pcv.analyze_NIR_intensity(img=img, rgbimg=img, mask=mask, bins=256, device=0, histplot=False, debug="print",
                                  filename=outfile)
    os.rename("3_nir_pseudo_plant.jpg", os.path.join(TEST_TMPDIR, "3_nir_pseudo_plant.jpg"))
    os.rename("3_nir_pseudo_plant_back.jpg", os.path.join(TEST_TMPDIR, "3_nir_pseudo_plant_back.jpg"))
    # Test with debug = "plot"
    _ = pcv.analyze_NIR_intensity(img=img, rgbimg=img, mask=mask, bins=256, device=0, histplot=False, debug="plot",
                                  filename=False)
    # Test with debug = None
    device, hist_header, hist_data, h_norm = pcv.analyze_NIR_intensity(img=img, rgbimg=img, mask=mask, bins=256,
                                                                       device=0, histplot=False, debug=None,
                                                                       filename=False)
    assert np.sum(hist_data[3]) == 713986


def test_plantcv_analyze_object():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS))
    obj_contour = contours_npz['arr_0']
    max_obj = max(obj_contour, key=len)
    # Test with debug = "print"
    outfile = os.path.join(TEST_TMPDIR, TEST_INPUT_COLOR)
    _ = pcv.analyze_object(img=img, imgname="img", obj=max_obj, mask=mask, device=0, debug="print", filename=outfile)
    os.rename("1_shapes.jpg", os.path.join(TEST_TMPDIR, "1_shapes.jpg"))
    # Test with debug = "plot"
    _ = pcv.analyze_object(img=img, imgname="img", obj=max_obj, mask=mask, device=0, debug="plot", filename=False)
    # Test with debug = None
    device, obj_header, obj_data, obj_images = pcv.analyze_object(img=img, imgname="img", obj=max_obj, mask=mask,
                                                                  device=0, debug=None, filename=False)
    assert obj_data[1] != 0


def test_plantcv_apply_mask_white():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    _ = pcv.apply_mask(img=img, mask=mask, mask_color="white", device=0, debug="print")
    os.rename("1_wmasked.png", os.path.join(TEST_TMPDIR, "1_wmasked.png"))
    # Test with debug = "plot"
    _ = pcv.apply_mask(img=img, mask=mask, mask_color="white", device=0, debug="plot")
    # Test with debug = None
    device, masked_img = pcv.apply_mask(img=img, mask=mask, mask_color="white", device=0, debug=None)
    assert all([i == j] for i, j in zip(np.shape(masked_img), TEST_COLOR_DIM))


def test_plantcv_apply_mask_black():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    _ = pcv.apply_mask(img=img, mask=mask, mask_color="black", device=0, debug="print")
    os.rename("1_bmasked.png", os.path.join(TEST_TMPDIR, "1_bmasked.png"))
    # Test with debug = "plot"
    _ = pcv.apply_mask(img=img, mask=mask, mask_color="black", device=0, debug="plot")
    # Test with debug = None
    device, masked_img = pcv.apply_mask(img=img, mask=mask, mask_color="black", device=0, debug=None)
    assert all([i == j] for i, j in zip(np.shape(masked_img), TEST_COLOR_DIM))


def test_plantcv_auto_crop():
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INTPUT_MULTI), -1)
    contours = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_CONTOUR))
    roi_contours = contours['arr_0']
    # Test with debug = "print"
    _ = pcv.auto_crop(device=0, img=img1, objects=roi_contours[48], padding_x=20, padding_y=20, color='black',
                      debug="print")
    os.rename("1_crop_area.png", os.path.join(TEST_TMPDIR, "1_crop_area.png"))
    os.rename("1_auto_cropped.png", os.path.join(TEST_TMPDIR, "1_auto_cropped.png"))
    # Test with debug = "plot"
    _ = pcv.auto_crop(device=0, img=img1, objects=roi_contours[48], padding_x=20, padding_y=20, color='black',
                      debug="plot")
    # Test with debug = None
    device, cropped = pcv.auto_crop(device=0, img=img1, objects=roi_contours[48], padding_x=20, padding_y=20,
                                    color='black', debug=None)
    x, y, z = np.shape(img1)
    x1, y1, z1 = np.shape(cropped)
    assert x > x1


def test_plantcv_binary_threshold():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with object type = dark
    _ = pcv.binary_threshold(img=img, threshold=25, maxValue=255, object_type="dark", device=0, debug=None)
    # Test with debug = "print"
    _ = pcv.binary_threshold(img=img, threshold=25, maxValue=255, object_type="light", device=0, debug="print")
    os.rename("1_binary_threshold25.png", os.path.join(TEST_TMPDIR, "1_binary_threshold25.png"))
    # Test with debug = "plot"
    _ = pcv.binary_threshold(img=img, threshold=25, maxValue=255, object_type="light", device=0, debug="plot")
    # Test with debug = None
    device, binary_img = pcv.binary_threshold(img=img, threshold=25, maxValue=255, object_type="light",
                                              device=0, debug=None)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(binary_img), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(binary_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_binary_threshold_incorrect_object_type():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.binary_threshold(img=img, threshold=25, maxValue=255, object_type="lite", device=0, debug=None)


def test_plantcv_cluster_contours():
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INTPUT_MULTI), -1)
    contours = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_CONTOUR))
    roi_contours = contours['arr_0']
    # Test with debug = "print"
    _ = pcv.cluster_contours(device=0, img=img1, roi_objects=roi_contours, nrow=4, ncol=6, debug="print")
    os.rename("1_clusters.png", os.path.join(TEST_TMPDIR, "1_clusters.png"))
    # Test with debug = "plot"
    _ = pcv.cluster_contours(device=0, img=img1, roi_objects=roi_contours, nrow=4, ncol=6, debug="plot")
    # Test with debug = None
    device, clusters_i, contours = pcv.cluster_contours(device=0, img=img1, roi_objects=roi_contours, nrow=4, ncol=6,
                                                        debug=None)
    lenori = len(roi_contours)
    lenclust = len(clusters_i)
    assert lenori > lenclust


def test_plantcv_cluster_contours_splitimg():
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INTPUT_MULTI), -1)
    contours = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_CONTOUR))
    clusters = np.load(os.path.join(TEST_DATA, TEST_INPUT_ClUSTER_CONTOUR))
    roi_contours = contours['arr_0']
    cluster_contours = clusters['arr_0']
    # Test with debug = "print"
    _ = pcv.cluster_contour_splitimg(device=0, img=img1, grouped_contour_indexes=cluster_contours,
                                     contours=roi_contours, outdir=TEST_TMPDIR, file=None, filenames=None,
                                     debug="print")
    for i in range(1, 19):
        os.rename(str(i) + "_clusters.png", os.path.join(TEST_TMPDIR, str(i) + "_clusters.png"))
        os.rename(str(i) + "_wmasked.png", os.path.join(TEST_TMPDIR, str(i) + "_wmasked.png"))
    # Test with debug = "plot"
    _ = pcv.cluster_contour_splitimg(device=0, img=img1, grouped_contour_indexes=cluster_contours,
                                     contours=roi_contours, outdir=None, file=None, filenames=None, debug="plot")
    # Test with debug = None
    device, output_path = pcv.cluster_contour_splitimg(device=0, img=img1, grouped_contour_indexes=cluster_contours,
                                                       contours=roi_contours, outdir=None, file=None,
                                                       filenames=None, debug=None)
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
    nir, path1, filename1 = pcv.readimage(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
    # Test with debug = "print"
    _ = pcv.crop_position_mask(nir, mask, device=0, x=40, y=3, v_pos="top", h_pos="right", debug="print")
    os.rename("1_mask_overlay.png", os.path.join(TEST_TMPDIR, "1_mask_overlay.png"))
    os.rename("1_newmask.png", os.path.join(TEST_TMPDIR, "1_newmask.png"))
    os.rename("1_push-right.png", os.path.join(TEST_TMPDIR, "1_push-right.png"))
    os.rename("1_push-top_.png", os.path.join(TEST_TMPDIR, "1_push-top_.png"))
    # Test with debug = "plot"
    _ = pcv.crop_position_mask(nir, mask, device=0, x=40, y=3, v_pos="top", h_pos="right", debug="plot")
    # Test with debug = None
    device, newmask = pcv.crop_position_mask(nir, mask, device=0, x=40, y=3, v_pos="top", h_pos="right", debug=None)
    assert np.sum(newmask) == 641517


def test_plantcv_define_roi_rectangle():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    _ = pcv.define_roi(img=img, shape="rectangle", device=0, roi=None, roi_input="default", debug="print", adjust=True,
                       x_adj=600, y_adj=300, w_adj=-500, h_adj=-600)
    os.rename("1_roi.png", os.path.join(TEST_TMPDIR, "1_roi.png"))
    # Test with debug = "plot"
    _ = pcv.define_roi(img=img, shape="rectangle", device=0, roi=None, roi_input="default", debug="plot", adjust=True,
                       x_adj=600, y_adj=300, w_adj=-500, h_adj=-600)
    # Test with debug = None
    device, contours, hierarchy = pcv.define_roi(img=img, shape="rectangle", device=0, roi=None, roi_input="default",
                                                 debug=None, adjust=True, x_adj=600, y_adj=500, w_adj=-300, h_adj=-600)
    # Assert the contours and hierarchy lists contain only the ROI
    if len(contours) == 2 and len(hierarchy) == 1:
        assert 1
    else:
        assert 0


def test_plantcv_define_roi_rectangle_no_adjust():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    _ = pcv.define_roi(img=img, shape="rectangle", device=0, roi=None, roi_input="default", debug="print", adjust=False,
                       x_adj=0, y_adj=0, w_adj=0, h_adj=0)
    os.rename("1_roi.png", os.path.join(TEST_TMPDIR, "1_roi.png"))
    # Test with debug = "plot"
    _ = pcv.define_roi(img=img, shape="rectangle", device=0, roi=None, roi_input="default", debug="plot", adjust=False,
                       x_adj=0, y_adj=0, w_adj=0, h_adj=0)
    # Test with debug = None
    device, contours, hierarchy = pcv.define_roi(img=img, shape="rectangle", device=0, roi=None, roi_input="default",
                                                 debug=None, adjust=False, x_adj=0, y_adj=0, w_adj=0, h_adj=0)
    # Assert the contours and hierarchy lists contain only the ROI
    if len(contours) == 2 and len(hierarchy) == 1:
        assert 1
    else:
        assert 0


def test_plantcv_define_roi_circle():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    _ = pcv.define_roi(img=img, shape="circle", device=0, roi=None, roi_input="default", debug="print", adjust=True,
                       x_adj=0, y_adj=300, w_adj=0, h_adj=-900)
    os.rename("1_roi.png", os.path.join(TEST_TMPDIR, "1_roi.png"))
    # Test with debug = "plot"
    _ = pcv.define_roi(img=img, shape="circle", device=0, roi=None, roi_input="default", debug="plot", adjust=True,
                       x_adj=0, y_adj=300, w_adj=0, h_adj=-900)
    # Test with debug = None
    device, contours, hierarchy = pcv.define_roi(img=img, shape="circle", device=0, roi=None, roi_input="default",
                                                 debug=None, adjust=True, x_adj=0, y_adj=300, w_adj=0, h_adj=-900)
    # Assert the contours and hierarchy lists contain only the ROI
    if len(contours) == 1 and len(hierarchy) == 1:
        assert 1
    else:
        assert 0


def test_plantcv_define_roi_circle_no_adjust():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    _ = pcv.define_roi(img=img, shape="circle", device=0, roi=None, roi_input="default", debug="print", adjust=False,
                       x_adj=0, y_adj=0, w_adj=0, h_adj=0)
    os.rename("1_roi.png", os.path.join(TEST_TMPDIR, "1_roi.png"))
    # Test with debug = "plot"
    _ = pcv.define_roi(img=img, shape="circle", device=0, roi=None, roi_input="default", debug="plot", adjust=False,
                       x_adj=0, y_adj=0, w_adj=0, h_adj=0)
    # Test with debug = None
    device, contours, hierarchy = pcv.define_roi(img=img, shape="circle", device=0, roi=None, roi_input="default",
                                                 debug=None, adjust=False, x_adj=0, y_adj=0, w_adj=0, h_adj=0)
    # Assert the contours and hierarchy lists contain only the ROI
    if len(contours) == 1 and len(hierarchy) == 1:
        assert 1
    else:
        assert 0


def test_plantcv_define_roi_ellipse():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    _ = pcv.define_roi(img=img, shape="ellipse", device=0, roi=None, roi_input="default", debug="print", adjust=True,
                       x_adj=0, y_adj=300, w_adj=-1000, h_adj=-900)
    os.rename("1_roi.png", os.path.join(TEST_TMPDIR, "1_roi.png"))
    # Test with debug = "plot"
    _ = pcv.define_roi(img=img, shape="ellipse", device=0, roi=None, roi_input="default", debug="plot", adjust=True,
                       x_adj=0, y_adj=300, w_adj=-1000, h_adj=-900)
    # Test with debug = None
    device, contours, hierarchy = pcv.define_roi(img=img, shape="ellipse", device=0, roi=None, roi_input="default",
                                                 debug=None, adjust=True, x_adj=0, y_adj=300, w_adj=-1000, h_adj=-900)
    # Assert the contours and hierarchy lists contain only the ROI
    if len(contours) == 2 and len(hierarchy) == 1:
        assert 1
    else:
        assert 0


def test_plantcv_define_roi_ellipse_no_adjust():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    _ = pcv.define_roi(img=img, shape="ellipse", device=0, roi=None, roi_input="default", debug="print", adjust=False,
                       x_adj=0, y_adj=0, w_adj=0, h_adj=0)
    os.rename("1_roi.png", os.path.join(TEST_TMPDIR, "1_roi.png"))
    # Test with debug = "plot"
    _ = pcv.define_roi(img=img, shape="ellipse", device=0, roi=None, roi_input="default", debug="plot", adjust=False,
                       x_adj=0, y_adj=0, w_adj=0, h_adj=0)
    # Test with debug = None
    device, contours, hierarchy = pcv.define_roi(img=img, shape="ellipse", device=0, roi=None, roi_input="default",
                                                 debug=None, adjust=False, x_adj=0, y_adj=0, w_adj=0, h_adj=0)
    # Assert the contours and hierarchy lists contain only the ROI
    if len(contours) == 2 and len(hierarchy) == 1:
        assert 1
    else:
        assert 0


def test_plantcv_define_roi_bad_adjust_values():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        _ = pcv.define_roi(img=img, shape="rectangle", device=0, roi=None, roi_input="default", debug=None, adjust=True,
                           x_adj=1, y_adj=0, w_adj=1, h_adj=0)


def test_plantcv_define_roi_bad_roi_input():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        _ = pcv.define_roi(img=img, shape="rectangle", device=0, roi=None, roi_input="test", debug=None, adjust=True,
                           x_adj=0, y_adj=0, w_adj=0, h_adj=0)


def test_plantcv_dilate():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    _ = pcv.dilate(img=img, kernel=5, i=1, device=0, debug="print")
    os.rename("1_dil_image_itr_1.png", os.path.join(TEST_TMPDIR, "1_dil_image_itr_1.png"))
    # Test with debug = "plot"
    _ = pcv.dilate(img=img, kernel=5, i=1, device=0, debug="plot")
    # Test with debug = None
    device, dilate_img = pcv.dilate(img=img, kernel=5, i=1, device=0, debug=None)
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
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    _ = pcv.erode(img=img, kernel=5, i=1, device=0, debug="print")
    os.rename("1_er_image_itr_1.png", os.path.join(TEST_TMPDIR, "1_er_image_itr_1.png"))
    # Test with debug = "plot"
    _ = pcv.erode(img=img, kernel=5, i=1, device=0, debug="plot")
    # Test with debug = None
    device, erode_img = pcv.erode(img=img, kernel=5, i=1, device=0, debug=None)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(erode_img), TEST_BINARY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(erode_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_fatal_error():
    # Verify that the fatal_error function raises a RuntimeError
    with pytest.raises(RuntimeError):
        pcv.fatal_error("Test error")


def test_plantcv_fill():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    mask = np.copy(img)
    _ = pcv.fill(img=img, mask=mask, size=1, device=0, debug="print")
    os.rename("1_fill1.png", os.path.join(TEST_TMPDIR, "1_fill1.png"))
    # Test with debug = "plot"
    mask = np.copy(img)
    _ = pcv.fill(img=img, mask=mask, size=1, device=0, debug="plot")
    # Test with debug = None
    mask = np.copy(img)
    device, fill_img = pcv.fill(img=img, mask=mask, size=1, device=0, debug=None)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(fill_img), TEST_BINARY_DIM))


def test_plantcv_find_objects():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    _ = pcv.find_objects(img=img, mask=mask, device=0, debug="print")
    os.rename("1_id_objects.png", os.path.join(TEST_TMPDIR, "1_id_objects.png"))
    # Test with debug = "plot"
    _ = pcv.find_objects(img=img, mask=mask, device=0, debug="plot")
    # Test with debug = None
    device, contours, hierarchy = pcv.find_objects(img=img, mask=mask, device=0, debug=None)
    # Assert the correct number of contours are found
    assert len(contours) == 7341


def test_plantcv_flip():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    _ = pcv.flip(img=img, direction="horizontal", device=0, debug="print")
    os.rename("1_flipped.png", os.path.join(TEST_TMPDIR, "1_flipped.png"))
    # Test with debug = "plot"
    _ = pcv.flip(img=img, direction="vertical", device=0, debug="plot")
    # Test with debug = None
    device, flipped_img = pcv.flip(img=img, direction="horizontal", device=0, debug=None)
    assert all([i == j] for i, j in zip(np.shape(flipped_img), TEST_COLOR_DIM))


def test_plantcv_flip_bad_input():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        _ = pcv.flip(img=img, direction="vert", device=0, debug=None)


def test_plantcv_fluor_fvfm():
    fdark = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FDARK), -1)
    fmin = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMIN), -1)
    fmax = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMAX), -1)
    fmask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMASK), -1)
    # Test with debug = "print"
    outfile = os.path.join(TEST_TMPDIR, TEST_INPUT_FMAX)
    _ = pcv.fluor_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=fmask, device=0, filename=outfile, bins=1000,
                       debug="print")
    os.rename("1_fmin_mask.png", os.path.join(TEST_TMPDIR, "1_fmin_mask.png"))
    os.rename("1_fmax_mask.png", os.path.join(TEST_TMPDIR, "1_fmax_mask.png"))
    os.rename("1_fv_convert.png", os.path.join(TEST_TMPDIR, "1_fv_convert.png"))
    # Test with debug = "plot"
    _ = pcv.fluor_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=fmask, device=0, filename=False, bins=1000, debug="plot")
    # Test with debug = None
    device, fvfm_header, fvfm_data = pcv.fluor_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=fmask, device=0,
                                                    filename=False, bins=1000, debug=None)
    assert fvfm_data[4] > 0.66


def test_plantcv_gaussian_blur():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    _ = pcv.gaussian_blur(device=0, img=img, ksize=(51, 51), sigmax=0, sigmay=None, debug="print")
    os.rename("1_gaussian_blur.png", os.path.join(TEST_TMPDIR, "1_gaussian_blur.png"))
    # Test with debug = "plot"
    _ = pcv.gaussian_blur(device=0, img=img, ksize=(51, 51), sigmax=0, sigmay=None, debug="plot")
    # Test with debug = None
    device, gaussian_img = pcv.gaussian_blur(device=0, img=img, ksize=(51, 51), sigmax=0, sigmay=None, debug=None)
    imgavg = np.average(img)
    gavg = np.average(gaussian_img)
    assert gavg != imgavg


def test_plantcv_get_nir_sv():
    device, nirpath = pcv.get_nir(TEST_DATA, TEST_VIS, device=0, debug=None)
    nirpath1 = os.path.join(TEST_DATA, TEST_NIR)
    assert nirpath == nirpath1


def test_plantcv_get_nir_tv():
    device, nirpath = pcv.get_nir(TEST_DATA, TEST_VIS_TV, device=0, debug=None)
    nirpath1 = os.path.join(TEST_DATA, TEST_NIR_TV)
    assert nirpath == nirpath1


def test_plantcv_hist_equalization():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "print"
    _ = pcv.hist_equalization(img=img, device=0, debug="print")
    os.rename("1_hist_equal_img.png", os.path.join(TEST_TMPDIR, "1_hist_equal_img.png"))
    # Test with debug = "plot"
    _ = pcv.hist_equalization(img=img, device=0, debug="plot")
    # Test with debug = None
    device, hist = pcv.hist_equalization(img=img, device=0, debug=None)
    histavg = np.average(hist)
    imgavg = np.average(img)
    assert histavg != imgavg


def test_plantcv_image_add():
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    # Test with debug = "print"
    _ = pcv.image_add(img1=img1, img2=img2, device=0, debug="print")
    os.rename("1_added.png", os.path.join(TEST_TMPDIR, "1_added.png"))
    # Test with debug = "plot"
    _ = pcv.image_add(img1=img1, img2=img2, device=0, debug="plot")
    # Test with debug = None
    device, added_img = pcv.image_add(img1=img1, img2=img2, device=0, debug=None)
    assert all([i == j] for i, j in zip(np.shape(added_img), TEST_BINARY_DIM))


def test_plantcv_image_subtract():
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    # Test with debug = "print"
    _ = pcv.image_subtract(img1=img1, img2=img2, device=0, debug="print")
    os.rename("1_subtracted.png", os.path.join(TEST_TMPDIR, "1_subtracted.png"))
    # Test with debug = "plot"
    _ = pcv.image_subtract(img1=img1, img2=img2, device=0, debug="plot")
    # Test with debug = None
    device, subtract_img = pcv.image_subtract(img1=img1, img2=img2, device=0, debug=None)
    assert all([i == j] for i, j in zip(np.shape(subtract_img), TEST_BINARY_DIM))


def test_plantcv_invert():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    _ = pcv.invert(img=img, device=0, debug="print")
    os.rename("1_invert.png", os.path.join(TEST_TMPDIR, "1_invert.png"))
    # Test with debug = "plot"
    _ = pcv.invert(img=img, device=0, debug="plot")
    # Test with debug = None
    device, inverted_img = pcv.invert(img=img, device=0, debug=None)
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
    results = pcv.landmark_reference_pt_dist(points_r=points_rescaled, centroid_r=centroid_rescaled,
                                             bline_r=bottomline_rescaled, device=0, debug=None)
    assert len(results) == 9


def test_plantcv_laplace_filter():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "print"
    _ = pcv.laplace_filter(img=img, k=1, scale=1, device=0, debug="print")
    os.rename("1_lp_out_k1_scale1.png", os.path.join(TEST_TMPDIR, "1_lp_out_k1_scale1.png"))
    # Test with debug = "plot"
    _ = pcv.laplace_filter(img=img, k=1, scale=1, device=0, debug="plot")
    # Test with debug = None
    device, lp_img = pcv.laplace_filter(img=img, k=1, scale=1, device=0, debug=None)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(lp_img), TEST_GRAY_DIM))


def test_plantcv_logical_and():
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    # Test with debug = "print"
    _ = pcv.logical_and(img1=img1, img2=img2, device=0, debug="print")
    os.rename("1_and_joined.png", os.path.join(TEST_TMPDIR, "1_and_joined.png"))
    # Test with debug = "plot"
    _ = pcv.logical_and(img1=img1, img2=img2, device=0, debug="plot")
    # Test with debug = None
    device, and_img = pcv.logical_and(img1=img1, img2=img2, device=0, debug=None)
    assert all([i == j] for i, j in zip(np.shape(and_img), TEST_BINARY_DIM))


def test_plantcv_logical_or():
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    # Test with debug = "print"
    _ = pcv.logical_or(img1=img1, img2=img2, device=0, debug="print")
    os.rename("1_or_joined.png", os.path.join(TEST_TMPDIR, "1_or_joined.png"))
    # Test with debug = "plot"
    _ = pcv.logical_or(img1=img1, img2=img2, device=0, debug="plot")
    # Test with debug = None
    device, or_img = pcv.logical_or(img1=img1, img2=img2, device=0, debug=None)
    assert all([i == j] for i, j in zip(np.shape(or_img), TEST_BINARY_DIM))


def test_plantcv_logical_xor():
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    # Test with debug = "print"
    _ = pcv.logical_xor(img1=img1, img2=img2, device=0, debug="print")
    os.rename("1_xor_joined.png", os.path.join(TEST_TMPDIR, "1_xor_joined.png"))
    # Test with debug = "plot"
    _ = pcv.logical_xor(img1=img1, img2=img2, device=0, debug="plot")
    # Test with debug = None
    device, xor_img = pcv.logical_xor(img1=img1, img2=img2, device=0, debug=None)
    assert all([i == j] for i, j in zip(np.shape(xor_img), TEST_BINARY_DIM))


def test_plantcv_median_blur():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    _ = pcv.median_blur(img=img, ksize=5, device=0, debug="print")
    os.rename("1_median_blur5.png", os.path.join(TEST_TMPDIR, "1_median_blur5.png"))
    # Test with debug = "plot"
    _ = pcv.median_blur(img=img, ksize=5, device=0, debug="plot")
    # Test with debug = None
    device, blur_img = pcv.median_blur(img=img, ksize=5, device=0, debug=None)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(blur_img), TEST_BINARY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(blur_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_naive_bayes_classifier():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    _ = pcv.naive_bayes_classifier(img=img, pdf_file=os.path.join(TEST_DATA, TEST_PDFS), device=0, debug="print")
    os.rename("1_naive_bayes_plant_mask.jpg", os.path.join(TEST_TMPDIR, "1_naive_bayes_plant_mask.jpg"))
    os.rename("1_naive_bayes_background_mask.jpg", os.path.join(TEST_TMPDIR, "1_naive_bayes_background_mask.jpg"))
    # Test with debug = "plot"
    _ = pcv.naive_bayes_classifier(img=img, pdf_file=os.path.join(TEST_DATA, TEST_PDFS), device=0, debug="plot")
    # Test with debug = None
    device, mask = pcv.naive_bayes_classifier(img=img, pdf_file=os.path.join(TEST_DATA, TEST_PDFS), device=0,
                                              debug=None)

    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(mask), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(mask), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_object_composition():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS))
    object_contours = contours_npz['arr_0']
    object_hierarchy = contours_npz['arr_1']
    # Test with debug = "print"
    _ = pcv.object_composition(img=img, contours=object_contours, hierarchy=object_hierarchy, device=0, debug="print")
    os.rename("1_objcomp.png", os.path.join(TEST_TMPDIR, "1_objcomp.png"))
    os.rename("1_objcomp_mask.png", os.path.join(TEST_TMPDIR, "1_objcomp_mask.png"))
    # Test with debug = "plot"
    _ = pcv.object_composition(img=img, contours=object_contours, hierarchy=object_hierarchy, device=0, debug="plot")
    # Test with debug = None
    device, contours, mask = pcv.object_composition(img=img, contours=object_contours, hierarchy=object_hierarchy,
                                                    device=0, debug=None)
    # Assert that the objects have been combined
    contour_shape = np.shape(contours)
    assert contour_shape[1] == 1


def test_plantcv_otsu_threshold():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INTPUT_GREENMAG), -1)
    # Test with object set to light
    _ = pcv.otsu_auto_threshold(img=img, maxValue=255, object_type="light", device=0, debug=None)
    # Test with debug = "print"
    _ = pcv.otsu_auto_threshold(img=img, maxValue=255, object_type='dark', device=0, debug="print")
    os.rename("1_otsu_auto_threshold_125.0_inv.png", os.path.join(TEST_TMPDIR, "1_otsu_auto_threshold_125.0_inv.png"))
    # Test with debug = "plot"
    _ = pcv.otsu_auto_threshold(img=img, maxValue=255, object_type='dark', device=0, debug="plot")
    # Test with debug = None
    device, threshold_otsu = pcv.otsu_auto_threshold(img=img, maxValue=255, object_type='dark', device=0, debug=None)
    assert np.max(threshold_otsu) == 255


def test_plantcv_output_mask():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    _ = pcv.output_mask(device=0, img=img, mask=mask, filename='test.png', outdir=TEST_TMPDIR, mask_only=False,
                        debug="print")
    os.rename("1_mask-img.png", os.path.join(TEST_TMPDIR, "1_mask-img.png"))
    os.rename("1_ori-img.png", os.path.join(TEST_TMPDIR, "1_ori-img.png"))
    # Test with debug = "plot"
    _ = pcv.output_mask(device=0, img=img, mask=mask, filename='test.png', outdir=TEST_TMPDIR, mask_only=False,
                        debug="plot")
    # Test with debug = None
    device, imgpath, maskpath, analysis_images = pcv.output_mask(device=0, img=img, mask=mask, filename='test.png',
                                                                 outdir=TEST_TMPDIR, mask_only=False, debug=None)
    assert all([os.path.exists(imgpath) is True, os.path.exists(maskpath) is True])


def test_plantcv_plot_hist():
    # Test in 16-bit image mode
    img16bit = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK), -1)
    _ = pcv.plot_hist(img=img16bit, name=os.path.join(TEST_TMPDIR, "hist_nir_uint16"))
    # Test in 8-bit image mode
    img8bit = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), -1)
    bins, hist = pcv.plot_hist(img=img8bit, name=os.path.join(TEST_TMPDIR, "hist_rgb_uint8"))
    assert len(hist) == 256


def test_plantcv_print_image():
    img, path, img_name = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    filename = os.path.join(TEST_TMPDIR, 'plantcv_print_image.jpg')
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


def test_plantcv_readimage():
    # Test with debug = "print"
    _ = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_COLOR), debug="print")
    os.rename("input_image.png", os.path.join(TEST_TMPDIR, "input_image.png"))
    # Test with debug = "plot"
    _ = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_COLOR), debug="plot")
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


def test_plantcv_readimage_bad_file():
    with pytest.raises(RuntimeError):
        _ = pcv.readimage(filename=TEST_INPUT_COLOR)


def test_plantcv_rectangle_mask():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "print"
    _ = pcv.rectangle_mask(img=img, p1=(0, 0), p2=(2454, 2056), device=0, debug="print", color="white")
    os.rename("1_roi.png", os.path.join(TEST_TMPDIR, "1_roi.png"))
    # Test with debug = "plot"
    _ = pcv.rectangle_mask(img=img, p1=(0, 0), p2=(2454, 2056), device=0, debug="plot", color="gray")
    # Test with debug = None
    device, masked, hist, contour, heir = pcv.rectangle_mask(img=img, p1=(0, 0), p2=(2454, 2056), device=0, debug=None,
                                                             color="black")
    maskedsum = np.sum(masked)
    imgsum = np.sum(img)
    assert maskedsum < imgsum


def test_plantcv_report_size_marker():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MARKER), -1)
    # Test with debug = "print"
    outfile = os.path.join(TEST_TMPDIR, TEST_INPUT_MARKER)
    _ = pcv.report_size_marker_area(img=img, shape='rectangle', device=0, debug="print", marker='detect', x_adj=3500,
                                    y_adj=600, w_adj=-100, h_adj=-1500, base='white', objcolor='light',
                                    thresh_channel='s', thresh=120, filename=outfile)
    for filename in ["1_marker_roi.png", "2_hsv_saturation.png", "3_binary_threshold120.png", "4_id_objects.png",
                     "5_roi.png", "6_obj_on_img.png", "6_roi_mask.png", "6_roi_objects.png", "7_marker_shape.png",
                     "7_objcomp.png", "7_objcomp_mask.png"]:
        os.rename(filename, os.path.join(TEST_TMPDIR, filename))

    # Test with debug = "plot"
    _ = pcv.report_size_marker_area(img=img, shape='rectangle', device=0, debug="plot", marker='detect', x_adj=3500,
                                    y_adj=600, w_adj=-100, h_adj=-1500, base='white', objcolor='light',
                                    thresh_channel='s', thresh=120, filename=False)
    # Test with debug = None
    device, marker_header, marker_data, images = pcv.report_size_marker_area(img=img, shape='rectangle', device=0,
                                                                             debug=None, marker='detect', x_adj=3500,
                                                                             y_adj=600, w_adj=-100, h_adj=-1500,
                                                                             base='white', objcolor='light',
                                                                             thresh_channel='s', thresh=120,
                                                                             filename=False)
    assert marker_data[1] > 100


def test_plantcv_resize():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    _ = pcv.resize(img=img, resize_x=0.5, resize_y=0.5, device=0, debug="print")
    os.rename("1_resize1.png", os.path.join(TEST_TMPDIR, "1_resize1.png"))
    # Test with debug = "plot"
    _ = pcv.resize(img=img, resize_x=0.5, resize_y=0.5, device=0, debug="plot")
    # Test with debug = None
    device, resized_img = pcv.resize(img=img, resize_x=0.5, resize_y=0.5, device=0, debug=None)
    ix, iy, iz = np.shape(img)
    rx, ry, rz = np.shape(resized_img)
    assert ix > rx


def test_plantcv_rgb2gray_hsv():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    _ = pcv.rgb2gray_hsv(img=img, channel="s", device=0, debug="print")
    os.rename("1_hsv_saturation.png", os.path.join(TEST_TMPDIR, "1_hsv_saturation.png"))
    # Test with debug = "plot"
    _ = pcv.rgb2gray_hsv(img=img, channel="s", device=0, debug="plot")
    # Test with debug = None
    device, s = pcv.rgb2gray_hsv(img=img, channel="s", device=0, debug=None)
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert all([i == j] for i, j in zip(np.shape(s), TEST_GRAY_DIM))


def test_plantcv_rgb2gray_lab():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    _ = pcv.rgb2gray_lab(img=img, channel='b', device=0, debug="print")
    os.rename("1_lab_blue-yellow.png", os.path.join(TEST_TMPDIR, "1_lab_blue-yellow.png"))
    # Test with debug = "plot"
    _ = pcv.rgb2gray_lab(img=img, channel='b', device=0, debug="plot")
    # Test with debug = None
    device, b = pcv.rgb2gray_lab(img=img, channel='b', device=0, debug=None)
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert all([i == j] for i, j in zip(np.shape(b), TEST_GRAY_DIM))


def test_plantcv_rgb2gray():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    _ = pcv.rgb2gray(img=img, device=0, debug="print")
    os.rename("1_gray.png", os.path.join(TEST_TMPDIR, "1_gray.png"))
    # Test with debug = "plot"
    _ = pcv.rgb2gray(img=img, device=0, debug="plot")
    # Test with debug = None
    device, gray = pcv.rgb2gray(img=img, device=0, debug=None)
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert all([i == j] for i, j in zip(np.shape(gray), TEST_GRAY_DIM))


def test_plantcv_roi_objects():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    roi_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_ROI))
    roi_contour = roi_npz['arr_0']
    roi_hierarchy = roi_npz['arr_1']
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS))
    object_contours = contours_npz['arr_0']
    object_hierarchy = contours_npz['arr_1']
    # Test with debug = "print"
    _ = pcv.roi_objects(img=img, roi_type="partial", roi_contour=roi_contour, roi_hierarchy=roi_hierarchy,
                        object_contour=object_contours, obj_hierarchy=object_hierarchy, device=0, debug="print")
    os.rename("1_obj_on_img.png", os.path.join(TEST_TMPDIR, "1_obj_on_img.png"))
    os.rename("1_roi_mask.png", os.path.join(TEST_TMPDIR, "1_roi_mask.png"))
    os.rename("1_roi_objects.png", os.path.join(TEST_TMPDIR, "1_roi_objects.png"))
    # Test with debug = "plot"
    _ = pcv.roi_objects(img=img, roi_type="partial", roi_contour=roi_contour, roi_hierarchy=roi_hierarchy,
                        object_contour=object_contours, obj_hierarchy=object_hierarchy, device=0, debug="plot")
    # Test with debug = None and roi_type = cutto
    _ = pcv.roi_objects(img=img, roi_type="cutto", roi_contour=roi_contour, roi_hierarchy=roi_hierarchy,
                        object_contour=object_contours, obj_hierarchy=object_hierarchy, device=0, debug=None)
    # Test with debug = None
    device, kept_contours, kept_hierarchy, mask, area = pcv.roi_objects(img=img, roi_type="partial",
                                                                        roi_contour=roi_contour,
                                                                        roi_hierarchy=roi_hierarchy,
                                                                        object_contour=object_contours,
                                                                        obj_hierarchy=object_hierarchy,
                                                                        device=0, debug=None)
    # Assert that the contours were filtered as expected
    assert len(kept_contours) == 1046


def test_plantcv_rotate_img():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    _ = pcv.rotate_img(img=img, rotation_deg=45, device=0, debug="print")
    os.rename("1_rotated_img.png", os.path.join(TEST_TMPDIR, "1_rotated_img.png"))
    # Test with debug = "plot"
    _ = pcv.rotate_img(img=img, rotation_deg=45, device=0, debug="plot")
    # Test with debug = None
    device, rotated = pcv.rotate_img(img=img, rotation_deg=45, device=0, debug=None)
    imgavg = np.average(img)
    rotateavg = np.average(rotated)
    assert rotateavg != imgavg


def test_plantcv_rotate_img_gray():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "plot"
    _ = pcv.rotate_img(img=img, rotation_deg=45, device=0, debug="plot")
    # Test with debug = None
    device, rotated = pcv.rotate_img(img=img, rotation_deg=45, device=0, debug=None)
    imgavg = np.average(img)
    rotateavg = np.average(rotated)
    assert rotateavg != imgavg


def test_plantcv_scale_features():
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR))
    obj_contour = contours_npz['arr_0']
    # Test with debug = "print"
    _ = pcv.scale_features(obj=obj_contour, mask=mask, points=TEST_ACUTE_RESULT, boundary_line=50, device=0,
                           debug="print")
    os.rename("1_feature_scaled.png", os.path.join(TEST_TMPDIR, "1_feature_scaled.png"))
    # Test with debug = "plot"
    _ = pcv.scale_features(obj=obj_contour, mask=mask, points=TEST_ACUTE_RESULT, boundary_line=50, device=0,
                           debug="plot")
    # Test with debug = None
    device, points_rescaled, centroid_rescaled, bottomline_rescaled = pcv.scale_features(obj=obj_contour, mask=mask,
                                                                                         points=TEST_ACUTE_RESULT,
                                                                                         boundary_line=50, device=0,
                                                                                         debug=None)
    assert len(points_rescaled) == 23


def test_plantcv_scale_features_bad_input():
    mask = np.array([])
    obj_contour = np.array([])
    result = pcv.scale_features(obj=obj_contour, mask=mask, points=TEST_ACUTE_RESULT, boundary_line=50, device=0,
                                debug=None)
    assert all([i == j] for i, j in zip(result, [0, ("NA", "NA"), ("NA", "NA"), ("NA", "NA")]))


def test_plantcv_scharr_filter():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "print"
    _ = pcv.scharr_filter(img=img, dX=1, dY=0, scale=1, device=0, debug="print")
    os.rename("1_sr_img_dx1_dy0_scale1.png", os.path.join(TEST_TMPDIR, "1_sr_img_dx1_dy0_scale1.png"))
    # Test with debug = "plot"
    _ = pcv.scharr_filter(img=img, dX=1, dY=0, scale=1, device=0, debug="plot")
    # Test with debug = None
    device, scharr_img = pcv.scharr_filter(img=img, dX=1, dY=0, scale=1, device=0, debug=None)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(scharr_img), TEST_GRAY_DIM))


def test_plantcv_shift_img():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    _ = pcv.shift_img(img=img, device=0, number=300, side="top", debug="print")
    os.rename("1_shifted_img.png", os.path.join(TEST_TMPDIR, "1_shifted_img.png"))
    # Test with debug = "plot"
    _ = pcv.shift_img(img=img, device=0, number=300, side="top", debug="plot")
    # Test with debug = None
    device, rotated = pcv.shift_img(img=img, device=0, number=300, side="top", debug=None)
    imgavg = np.average(img)
    shiftavg = np.average(rotated)
    assert shiftavg != imgavg


def test_plantcv_sobel_filter():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "print"
    _ = pcv.sobel_filter(img=img, dx=1, dy=0, k=1, device=0, debug="print")
    os.rename("1_sb_img_dx1_dy0_k1.png", os.path.join(TEST_TMPDIR, "1_sb_img_dx1_dy0_k1.png"))
    # Test with debug = "plot"
    _ = pcv.sobel_filter(img=img, dx=1, dy=0, k=1, device=0, debug="plot")
    # Test with debug = None
    device, sobel_img = pcv.sobel_filter(img=img, dx=1, dy=0, k=1, device=0, debug=None)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(sobel_img), TEST_GRAY_DIM))


def test_plantcv_triangle_threshold():
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "print"
    _ = pcv.triangle_auto_threshold(device=0, img=img1, maxvalue=255, object_type="light", xstep=10, debug="print")
    os.rename("1_triangle_thresh_hist_30.0.png", os.path.join(TEST_TMPDIR, "1_triangle_thresh_hist_30.0.png"))
    os.rename("1_triangle_thresh_img_30.0.png", os.path.join(TEST_TMPDIR, "1_triangle_thresh_img_30.0.png"))
    # Test with debug = "plot"
    _ = pcv.triangle_auto_threshold(device=0, img=img1, maxvalue=255, object_type="light", xstep=10, debug="plot")
    # Test with debug = None
    device, thresholded = pcv.triangle_auto_threshold(device=0, img=img1, maxvalue=255, object_type="light", xstep=10,
                                                      debug=None)
    thresholdedavg = np.average(thresholded)
    imgavg = np.average(img1)
    assert thresholdedavg > imgavg


def test_plantcv_watershed_segmentation():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_CROPPED))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_CROPPED_MASK), -1)
    # Test with debug = "print"
    outfile = os.path.join(TEST_TMPDIR, TEST_INPUT_CROPPED)
    _ = pcv.watershed_segmentation(device=0, img=img, mask=mask, distance=10, filename=outfile, debug="print")
    os.rename("1_watershed_dist_img.png", os.path.join(TEST_TMPDIR, "1_watershed_dist_img.png"))
    os.rename("1_watershed_img.png", os.path.join(TEST_TMPDIR, "1_watershed_img.png"))
    # Test with debug = "plot"
    _ = pcv.watershed_segmentation(device=0, img=img, mask=mask, distance=10, filename=False, debug="plot")
    # Test with debug = None
    device, watershed_header, watershed_data, images = pcv.watershed_segmentation(device=0, img=img, mask=mask,
                                                                                  distance=10, filename=False,
                                                                                  debug=None)
    assert watershed_data[1] > 9


def test_plantcv_white_balance_gray_16bit():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK), -1)
    # Test with debug = "print"
    _ = pcv.white_balance(device=0, img=img, debug="print", roi=(5, 5, 80, 80))
    os.rename("1_whitebalance_roi.png", os.path.join(TEST_TMPDIR, "1_whitebalance_roi.png"))
    os.rename("1_whitebalance.png", os.path.join(TEST_TMPDIR, "1_whitebalance.png"))
    # Test with debug = "plot"
    _ = pcv.white_balance(device=0, img=img, debug="plot", roi=(5, 5, 80, 80))
    # Test without an ROI
    _ = pcv.white_balance(device=0, img=img, debug=None, roi=None)
    # Test with debug = None
    device, white_balanced = pcv.white_balance(device=0, img=img, debug=None, roi=(5, 5, 80, 80))
    imgavg = np.average(img)
    balancedavg = np.average(white_balanced)
    assert balancedavg != imgavg


def test_plantcv_white_balance_gray_8bit():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Test with debug = "print"
    _ = pcv.white_balance(device=0, img=img, debug="print", roi=(5, 5, 80, 80))
    os.rename("1_whitebalance_roi.png", os.path.join(TEST_TMPDIR, "1_whitebalance_roi.png"))
    os.rename("1_whitebalance.png", os.path.join(TEST_TMPDIR, "1_whitebalance.png"))
    # Test with debug = "plot"
    _ = pcv.white_balance(device=0, img=img, debug="plot", roi=(5, 5, 80, 80))
    # Test without an ROI
    _ = pcv.white_balance(device=0, img=img, debug=None, roi=None)
    # Test with debug = None
    device, white_balanced = pcv.white_balance(device=0, img=img, debug=None, roi=(5, 5, 80, 80))
    imgavg = np.average(img)
    balancedavg = np.average(white_balanced)
    assert balancedavg != imgavg


def test_plantcv_white_balance_rgb():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MARKER))
    # Test with debug = "print"
    _ = pcv.white_balance(device=0, img=img, debug="print", roi=(5, 5, 80, 80))
    os.rename("1_whitebalance_roi.png", os.path.join(TEST_TMPDIR, "1_whitebalance_roi.png"))
    os.rename("1_whitebalance.png", os.path.join(TEST_TMPDIR, "1_whitebalance.png"))
    # Test with debug = "plot"
    _ = pcv.white_balance(device=0, img=img, debug="plot", roi=(5, 5, 80, 80))
    # Test without an ROI
    _ = pcv.white_balance(device=0, img=img, debug=None, roi=None)
    # Test with debug = None
    device, white_balanced = pcv.white_balance(device=0, img=img, debug=None, roi=(5, 5, 80, 80))
    imgavg = np.average(img)
    balancedavg = np.average(white_balanced)
    assert balancedavg != imgavg


def test_plantcv_x_axis_pseudolandmarks():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR))
    obj_contour = contours_npz['arr_0']
    # Test with debug = "plot"
    _ = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img, device=0, debug="plot")
    # Test with debug = None
    device, top, bottom, center_v = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img, device=0,
                                                               debug=None)
    assert all([all([i == j] for i, j in zip(np.shape(top), (20, 1, 2))),
               all([i == j] for i, j in zip(np.shape(bottom), (20, 1, 2))),
               all([i == j] for i, j in zip(np.shape(center_v), (20, 1, 2)))])


def test_plantcv_x_axis_pseudolandmarks_small_obj():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL_PLANT))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL_PLANT), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR_SMALL_PLANT))
    obj_contour = contours_npz['arr_0']
    # Test with debug = "plot"
    device, top, bottom, center_v = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img, device=0,
                                                               debug="plot")
    assert all([all([i == j] for i, j in zip(np.shape(top), (20, 1, 2))),
               all([i == j] for i, j in zip(np.shape(bottom), (20, 1, 2))),
               all([i == j] for i, j in zip(np.shape(center_v), (20, 1, 2)))])


def test_plantcv_x_axis_pseudolandmarks_bad_input():
    img = np.array([])
    mask = np.array([])
    obj_contour = np.array([])
    result = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img, device=0, debug=None)
    assert all([i == j] for i, j in zip(result, [0, ("NA", "NA"), ("NA", "NA"), ("NA", "NA")]))


def test_plantcv_y_axis_pseudolandmarks():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR))
    obj_contour = contours_npz['arr_0']
    # Test with debug = "plot"
    _ = pcv.y_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img, device=0, debug="plot")
    # Test with debug = None
    device, left, right, center_h = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img, device=0,
                                                               debug=None)
    assert all([all([i == j] for i, j in zip(np.shape(left), (20, 1, 2))),
               all([i == j] for i, j in zip(np.shape(right), (20, 1, 2))),
               all([i == j] for i, j in zip(np.shape(center_h), (20, 1, 2)))])


def test_plantcv_y_axis_pseudolandmarks_small_obj():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL_PLANT))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL_PLANT), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR_SMALL_PLANT))
    obj_contour = contours_npz['arr_0']
    # Test with debug = "plot"
    device, left, right, center_h = pcv.y_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img, device=0,
                                                               debug="plot")
    assert all([all([i == j] for i, j in zip(np.shape(left), (20, 1, 2))),
               all([i == j] for i, j in zip(np.shape(right), (20, 1, 2))),
               all([i == j] for i, j in zip(np.shape(center_h), (20, 1, 2)))])


def test_plantcv_y_axis_pseudolandmarks_bad_input():
    img = np.array([])
    mask = np.array([])
    obj_contour = np.array([])
    result = pcv.y_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img, device=0, debug=None)
    assert all([i == j] for i, j in zip(result, [0, ("NA", "NA"), ("NA", "NA"), ("NA", "NA")]))


def test_plantcv_background_subtraction():
    # List to hold result of all tests.
    truths = []
    fg_img = cv2.imread(os.path.join(TEST_DATA, TEST_FOREGROUND))
    bg_img = cv2.imread(os.path.join(TEST_DATA, TEST_BACKGROUND))
    # Testing if background subtraction is actually still working.
    # This should return an array whose sum is greater than one
    device, fgmask = pcv.background_subtraction(background_image=bg_img, foreground_image=fg_img, device=0, debug=None)
    truths.append(np.sum(fgmask) > 0)
    # The same foreground subtracted from itself should be 0
    device, fgmask = pcv.background_subtraction(background_image=fg_img, foreground_image=fg_img, device=0, debug=None)
    truths.append(np.sum(fgmask) == 0)
    # The same background subtracted from itself should be 0
    device, fgmask = pcv.background_subtraction(background_image=bg_img, foreground_image=bg_img, device=0, debug=None)
    truths.append(np.sum(fgmask) == 0)
    # All of these should be true for the function to pass testing.
    assert (all(truths))


def test_plantcv_background_subtraction_debug():
    # List to hold result of all tests.
    truths = []
    fg_img = cv2.imread(os.path.join(TEST_DATA, TEST_FOREGROUND))
    bg_img = cv2.imread(os.path.join(TEST_DATA, TEST_BACKGROUND))
    # Test with debug = "print"
    device, fgmask = pcv.background_subtraction(background_image=bg_img, foreground_image=fg_img, device=0,
                                                debug="print")
    truths.append(np.sum(fgmask) > 0)
    os.rename("1_background_subtraction.png", os.path.join(TEST_TMPDIR, "1_background_subtraction.png"))
    # Test with debug = "plot"
    device, fgmask = pcv.background_subtraction(background_image=bg_img, foreground_image=fg_img, device=0,
                                                debug="plot")
    truths.append(np.sum(fgmask) > 0)
    # All of these should be true for the function to pass testing.
    assert (all(truths))


def test_plantcv_background_subtraction_bad_img_type():
    fg_color = cv2.imread(os.path.join(TEST_DATA, TEST_FOREGROUND))
    bg_gray = cv2.imread(os.path.join(TEST_DATA, TEST_BACKGROUND), 0)
    with pytest.raises(RuntimeError):
        _ = pcv.background_subtraction(background_image=bg_gray, foreground_image=fg_color, device=0, debug=None)


def test_plantcv_background_subtraction_different_sizes():
    fg_img = cv2.imread(os.path.join(TEST_DATA, TEST_FOREGROUND))
    bg_img = cv2.imread(os.path.join(TEST_DATA, TEST_BACKGROUND))
    bg_shp = np.shape(bg_img)
    bg_img_resized = cv2.resize(bg_img, (bg_shp[0] / 2, bg_shp[1] / 2), interpolation=cv2.INTER_AREA)
    device, fgmask = pcv.background_subtraction(background_image=bg_img_resized, foreground_image=fg_img, device=0,
                                                debug=None)
    assert np.sum(fgmask > 0)

# ##############################
# Tests for the learn subpackage
# ##############################


def test_plantcv_learn_naive_bayes():
    # Make image and mask directories in the cache directory
    imgdir = os.path.join(TEST_TMPDIR, "images")
    maskdir = os.path.join(TEST_TMPDIR, "masks")
    if not os.path.exists(imgdir):
        os.mkdir(imgdir)
    if not os.path.exists(maskdir):
        os.mkdir(maskdir)
    # Copy and image and mask to the image/mask directories
    shutil.copyfile(os.path.join(TEST_DATA, TEST_VIS_SMALL), os.path.join(imgdir, "image.png"))
    shutil.copyfile(os.path.join(TEST_DATA, TEST_MASK_SMALL), os.path.join(maskdir, "image.png"))
    # Run the naive Bayes training module
    outfile = os.path.join(TEST_TMPDIR, "naive_bayes_pdfs.txt")
    plantcv.learn.naive_bayes(imgdir=imgdir, maskdir=maskdir, outfile=outfile, mkplots=True)
    assert os.path.exists(outfile)


def test_plantcv_learn_naive_bayes_multiclass():
    # Run the naive Bayes multiclass training module
    outfile = os.path.join(TEST_TMPDIR, "naive_bayes_multiclass_pdfs.txt")
    plantcv.learn.naive_bayes_multiclass(samples_file=os.path.join(TEST_DATA, TEST_SAMPLED_RGB_POINTS), outfile=outfile,
                                         mkplots=True)
    assert os.path.exists(outfile)
