# warp image

import cv2
import os
import numpy as np
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from plantcv.plantcv import visualize
from plantcv.plantcv.image_subtract import image_subtract
from matplotlib import pyplot as plt
from plantcv.plantcv import color_palette


def warp(img, refimg, pts, refpts, method='default'):
    """Warp an image to another perspective

    Inputs:
    img = grayscale or binary image data to be warped
    refimg = RGB or grayscale image data to be used as reference
    pts = 4 coordinates on img1
    refpts = 4 coordinates on img2
    method = method of finding the transformation. 'default', 'ransac', 'lmeds', 'rho'
    Returns:
    warped_img = warped image

    :param img: numpy.ndarray
    :param refimg: numpy.ndarray
    :param pts: list of tuples
    :param refpts: list of tuples
    :param method: str
    :return warped_img: numpy.ndarray
    """

    params.device += 1

    if len(pts)<4 and len(refpts)<4:
        fatal_error('Please provide 4 pairs of corresponding coordinates.')
    if len(img.shape)>2:
        fatal_error('The input `img` should be grayscale or binary.')

    methods = {
        'default': 0,
        'ransac': cv2.RANSAC,
        'lmeds': cv2.LMEDS,
        'rho': cv2.RHO}


    refshape = refimg.shape
    rows, cols = refshape[0:2]
    # scale marker_size and line_thickness for different resolutions
    res_ratio = int(np.ceil(img.shape[0]/rows)) #ratio never smaller than 1 with np.ceil
    cols = color_palette(len(pts))

    # img2 = img.copy()
    # img2 = cv2.merge((img2, img2, img2))
    # for i, pt in enumerate(pts):
    #     print(type(i))
    #     print(i)
    #     print(cols[i])
    #     cv2.drawMarker(img2, pt, color=[255, 0, 40],
    #                    markerType=cv2.MARKER_CROSS,
    #                    markerSize=params.marker_size*res_ratio,
    #                    thickness=params.line_thickness*res_ratio)

    # refimg2 = refimg.copy()
    # if len(refshape)==2:
    #     refimg2 = cv2.merge((refimg2, refimg2, refimg2))
    # for i, pt in enumerate(refpts):
    #     cv2.drawMarker(refimg2, pt, color=cols[i],
    #                    markerType=cv2.MARKER_CROSS,
    #                    markerSize=params.marker_size,
    #                    thickness=params.line_thickness)

    ptsarr = np.array(pts, dtype='float32')
    refptsarr = np.array(refpts, dtype='float32')

    # M, S = cv2.findHomography(refptsarr, ptsarr, method=methods.get(method))
    M = np.array([[1,0,0],[0,1,0],[0,0,1]])
    warped_img = cv2.warpPerspective(src=img, M=M, dsize=(cols, rows))

    if params.debug != None:
        debug = params.debug
        params.debug = None
        # if len(refimg.shape)==3:
        #     warped_img = cv2.merge((warped_img, warped_img, warped_img))

        # imgsub = cv2.substract(refimg, warped_img)
        # imgblend = cv2.add(refimg, warped_img)
        # imgblend = cv2.addWeighted(refimg, 0.3, warped_img, 0.7, 0)
        params.debug=debug
        if params.debug == 'plot':
            plot_image(img2)
            plot_image(refimg2)
            # plot_image(imgsub)
        if params.debug == 'print':
            print_image(img2, os.path.join(params.debug_outdir, str(params.device) + "_img-to-warp.png"))
            print_image(refimg2, os.path.join(params.debug_outdir, str(params.device) + "_img-ref.png"))
            # print_image(imgsub, os.path.join(params.debug_outdir, str(params.device) + "_warp_overlay.png"))

    return warped_img
