#!/usr/bin/env python

import pytest
import os
import numpy as np
import cv2
import plantcv as pcv

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
TEST_INPUT_MASK="input_mask.png"
TEST_INPUT_NIR_MASK="input_nir.png"


if not os.path.exists(TEST_TMPDIR):
    os.mkdir(TEST_TMPDIR)


def test_plantcv_adaptive_threshold():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
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

def test_plantcv_analyze_bound():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS))
    object_contours = contours_npz['arr_0']
    device, boundary_header, boundary_data, boundary_img1 = pcv.analyze_bound(img, "img", object_contours[0], mask, 300, 0, None)
    assert boundary_data[3]==596347


def test_plantcv_analyze_color():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    device, color_header, color_data, analysis_images = pcv.analyze_color(img, "img", mask, 256, 0, None, None)
    assert np.sum(color_data[3])!=0


def test_plantcv_analyze_nir():
    img=cv2.imread(os.path.join(TEST_DATA,TEST_INPUT_COLOR),0)
    mask=cv2.imread(os.path.join(TEST_DATA,TEST_INPUT_BINARY),-1)
    device, hist_header, hist_data, h_norm = pcv.analyze_NIR_intensity(img, "img", mask, 256, 0, False, None)
    assert np.sum(hist_data[2])==718858.0


def test_plantcv_analyze_object():
    img=cv2.imread(os.path.join(TEST_DATA,TEST_INPUT_COLOR))
    mask=cv2.imread(os.path.join(TEST_DATA,TEST_INPUT_BINARY),-1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS))
    obj_contour = contours_npz['arr_0']
    max_obj = max(obj_contour, key=len)
    device, obj_header, obj_data, obj_images = pcv.analyze_object(img, "img", max_obj,mask, 0, None)
    assert np.sum(obj_data[1])==718861.0


def test_plantcv_apply_mask():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    device, masked_img = pcv.apply_mask(img=img, mask=mask, mask_color="white", device=0, debug=None)
    assert all([i == j] for i, j in zip(np.shape(masked_img), TEST_COLOR_DIM))


def test_plantcv_binary_threshold():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
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


def test_crop_position_mask():
    nir, path1, filename1 = pcv.readimage(os.path.join(TEST_DATA,TEST_INPUT_NIR_MASK))
    mask= cv2.imread(os.path.join(TEST_DATA,TEST_INPUT_MASK),-1)
    device, newmask=pcv.crop_position_mask(nir,mask, device=0, x=40,y=3,v_pos="top",h_pos="right",debug=None)
    assert np.sum(newmask)==641517


def test_plantcv_define_roi():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    device, contours, hierarchy = pcv.define_roi(img=img, shape="rectangle", device=0, roi=None, roi_input="default",
                                                 debug=None, adjust=True, x_adj=600, y_adj=300, w_adj=-300, h_adj=-600)
    # Assert the contours and hierarchy lists contain only the ROI
    if len(contours) == 2 and len(hierarchy) == 1:
        assert 1
    else:
        assert 0


def test_plantcv_dilate():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
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
    mask = np.copy(img)
    device, fill_img = pcv.fill(img=img, mask=mask, size=1, device=0, debug=None)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(fill_img), TEST_BINARY_DIM))


def test_plantcv_find_objects():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    device, contours, hierarchy = pcv.find_objects(img=img, mask=mask, device=0, debug=None)
    # Assert the correct number of contours are found
    assert len(contours) == 7341


def test_plantcv_flip():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    device, flipped_img = pcv.flip(img=img, direction="horizontal", device=0, debug=None)
    assert all([i == j] for i, j in zip(np.shape(flipped_img), TEST_COLOR_DIM))


def test_get_nir():
    device, nirpath = pcv.get_nir(TEST_DATA, TEST_VIS, device=0, debug=None)
    nirpath1 = os.path.join(TEST_DATA,TEST_NIR)
    assert nirpath == nirpath1


def test_plantcv_image_add():
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    device, added_img = pcv.image_add(img1=img1, img2=img2, device=0, debug=None)
    assert all([i == j] for i, j in zip(np.shape(added_img), TEST_BINARY_DIM))


def test_plantcv_image_subtract():
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    device, subtract_img = pcv.image_subtract(img1=img1, img2=img2, device=0, debug=None)
    assert all([i == j] for i, j in zip(np.shape(subtract_img), TEST_BINARY_DIM))


def test_plantcv_invert():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
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

def test_plantcv_laplace_filter():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    device, lp_img = pcv.laplace_filter(img=img, k=1, scale=1, device=0, debug=None)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(lp_img), TEST_GRAY_DIM))


def test_plantcv_logical_and():
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    device, and_img = pcv.logical_and(img1=img1, img2=img2, device=0, debug=None)
    assert all([i == j] for i, j in zip(np.shape(and_img), TEST_BINARY_DIM))


def test_plantcv_logical_or():
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    device, or_img = pcv.logical_or(img1=img1, img2=img2, device=0, debug=None)
    assert all([i == j] for i, j in zip(np.shape(or_img), TEST_BINARY_DIM))


def test_plantcv_logical_xor():
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    device, xor_img = pcv.logical_xor(img1=img1, img2=img2, device=0, debug=None)
    assert all([i == j] for i, j in zip(np.shape(xor_img), TEST_BINARY_DIM))


def test_plantcv_median_blur():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
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


def test_plantcv_object_composition():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS))
    object_contours = contours_npz['arr_0']
    object_hierarchy = contours_npz['arr_1']
    device, contours, mask = pcv.object_composition(img=img, contours=object_contours, hierarchy=object_hierarchy,
                                                    device=0, debug=None)
    # Assert that the objects have been combined
    contour_shape = np.shape(contours)
    assert contour_shape[1] == 1


def test_plantcv_print_image():
    img, path, img_name = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    filename = os.path.join(TEST_TMPDIR, 'plantcv_print_image.jpg')
    pcv.print_image(img=img, filename=filename)
    # Assert that the file was created
    assert os.path.exists(filename) is True


def test_plantcv_print_results():
    header = ['field1', 'field2', 'field3']
    data = ['value1', 'value2', 'value3']
    pcv.print_results(filename='not_used', header=header, data=data)


def test_plantcv_readimage():
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


def test_plantcv_resize():
    img=cv2.imread(os.path.join(TEST_DATA,TEST_INPUT_COLOR))
    device, resized_img=pcv.resize(img,0.5,0.5,device=0,debug=None)
    ix,iy,iz=np.shape(img)
    rx,ry,rz=np.shape(resized_img)
    assert ix>rx

def test_plantcv_rgb2gray_hsv():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    device, s = pcv.rgb2gray_hsv(img=img, channel='s', device=0, debug=None)
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert all([i == j] for i, j in zip(np.shape(s), TEST_GRAY_DIM))


def test_plantcv_rgb2gray_lab():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    device, b = pcv.rgb2gray_lab(img=img, channel='b', device=0, debug=None)
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert all([i == j] for i, j in zip(np.shape(b), TEST_GRAY_DIM))


def test_plantcv_rgb2gray():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
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
    device, kept_contours, kept_hierarchy, mask, area = pcv.roi_objects(img=img, roi_type="partial",
                                                                        roi_contour=roi_contour,
                                                                        roi_hierarchy=roi_hierarchy,
                                                                        object_contour=object_contours,
                                                                        obj_hierarchy=object_hierarchy,
                                                                        device=0, debug=None)
    # Assert that the contours were filtered as expected
    assert len(kept_contours) == 1046


def test_plantcv_rotate_img():
    img=cv2.imread(os.path.join(TEST_DATA,TEST_INPUT_COLOR))
    device, rotated=pcv.rotate_img(img,45,device=0,debug=None)
    imgavg=np.average(img)
    rotateavg=np.average(rotated)
    assert rotateavg!=imgavg


def test_plantcv_scharr_filter():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    device, scharr_img = pcv.scharr_filter(img=img, dX=1, dY=0, scale=1, device=0, debug=None)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(scharr_img), TEST_GRAY_DIM))

def test_plantcv_shift_img():
    img=cv2.imread(os.path.join(TEST_DATA,TEST_INPUT_COLOR))
    device, rotated=pcv.shift_img(img,device=0,number=300,side="top",debug=None)
    imgavg=np.average(img)
    shiftavg=np.average(rotated)
    assert shiftavg!=imgavg


def test_plantcv_sobel_filter():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    device, sobel_img = pcv.sobel_filter(img=img, dx=1, dy=0, k=1, scale=1, device=0, debug=None)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(sobel_img), TEST_GRAY_DIM))


def test_plantcv_white_balance():
    img=cv2.imread(os.path.join(TEST_DATA,TEST_INPUT_NIR_MASK),-1)
    device, white_balanced=pcv.white_balance(0, img, debug=None,roi=(5,5,80,80))
    imgavg=np.average(img)
    balancedavg=np.average(white_balanced)
    assert balancedavg!=imgavg
