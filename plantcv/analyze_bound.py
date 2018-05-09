# User-Input Boundary Line

import cv2
import sys
import numpy as np
from . import print_image
from . import plot_image
from . import analyze_bound_horizontal

def analyze_bound(img, imgname, obj, mask, line_position, device, debug=None, filename=False):
    """User-input boundary line tool

    Inputs:
    img             = image
    imgname         = name of input image
    obj             = single or grouped contour object
    mask            = mask made from selected contours
    shape_header    = pass shape header data to function
    shape_data      = pass shape data so that analyze_bound data can be appended to it
    line_position   = position of boundry line (a value of 0 would draw the line through the bottom of the image)
    device          = device number. Used to count steps in the pipeline
    debug           = None, print, or plot. Print = save to file, Plot = print to screen.
    filename        = False or image name. If defined print image.

    Returns:
    device          = device number
    bound_header    = data table column headers
    bound_data      = boundary data table
    analysis_images = output image filenames

    :param img: numpy array
    :param imgname: str
    :param obj: list
    :param mask: numpy array
    :param line_position: int
    :param device: int
    :param debug: str
    :param filename: str
    :return device: int
    :return bound_header: tuple
    :return bound_data: tuple
    :return analysis_images: list
    """

    # Note analyze_bound is now a wrapper for newer function analyze_bound Horizontal
    sys.stderr.write(
        'analyze_bound function will be depricated in the near future, please use analyze_bound_horizontal, which has the same functionality\n')

    device, bound_header, bound_data, analysis_images = analyze_bound_horizontal(img, obj, mask, line_position, device, debug, filename)

    return device, bound_header, bound_data, analysis_images

    # device += 1
    # ori_img = np.copy(img)
    #
    # # Draw line horizontal line through bottom of image, that is adjusted to user input height
    # if len(np.shape(ori_img)) == 3:
    #     iy, ix, iz = np.shape(ori_img)
    # else:
    #     iy, ix = np.shape(ori_img)
    # size = (iy, ix)
    # size1 = (iy, ix, 3)
    # background = np.zeros(size, dtype=np.uint8)
    # wback = (np.zeros(size1, dtype=np.uint8)) + 255
    # x_coor = int(ix)
    # y_coor = int(iy) - int(line_position)
    # rec_corner = int(iy - 2)
    # rec_point1 = (1, rec_corner)
    # rec_point2 = (x_coor - 2, y_coor - 2)
    # cv2.rectangle(background, rec_point1, rec_point2, (255), 1)
    # below_contour, below_hierarchy = cv2.findContours(background, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    #
    # x, y, width, height = cv2.boundingRect(obj)
    #
    # if y_coor - y <= 0:
    #     height_above_bound = 0
    #     height_below_bound = height
    # elif y_coor - y > 0:
    #     height_1 = y_coor - y
    #     if height - height_1 <= 0:
    #         height_above_bound = height
    #         height_below_bound = 0
    #     else:
    #         height_above_bound = y_coor - y
    #         height_below_bound = height - height_above_bound
    #
    # below = []
    # above = []
    # mask_nonzerox, mask_nonzeroy = np.nonzero(mask)
    # obj_points = np.vstack((mask_nonzeroy, mask_nonzerox))
    # obj_points1 = np.transpose(obj_points)
    #
    # for i, c in enumerate(obj_points1):
    #     xy = tuple(c)
    #     pptest = cv2.pointPolygonTest(below_contour[0], xy, measureDist=False)
    #     if pptest == 1:
    #         below.append(xy)
    #         cv2.circle(ori_img, xy, 1, (0, 0, 255))
    #         cv2.circle(wback, xy, 1, (0, 0, 255))
    #     else:
    #         above.append(xy)
    #         cv2.circle(ori_img, xy, 1, (0, 255, 0))
    #         cv2.circle(wback, xy, 1, (0, 255, 0))
    # above_bound_area = len(above)
    # below_bound_area = len(below)
    # percent_bound_area_above = ((float(above_bound_area)) / (float(above_bound_area + below_bound_area))) * 100
    # percent_bound_area_below = ((float(below_bound_area)) / (float(above_bound_area + below_bound_area))) * 100
    #
    # bound_header = [
    #     'HEADER_BOUNDARY' + str(line_position),
    #     'height_above_bound',
    #     'height_below_bound',
    #     'above_bound_area',
    #     'percent_above_bound_area',
    #     'below_bound_area',
    #     'percent_below_bound_area'
    # ]
    #
    # bound_data = [
    #     'BOUNDARY_DATA',
    #     height_above_bound,
    #     height_below_bound,
    #     above_bound_area,
    #     percent_bound_area_above,
    #     below_bound_area,
    #     percent_bound_area_below
    # ]
    #
    # analysis_images = []
    #
    # if above_bound_area or below_bound_area:
    #     point3 = (0, y_coor - 4)
    #     point4 = (x_coor, y_coor - 4)
    #     cv2.line(ori_img, point3, point4, (255, 0, 255), 5)
    #     cv2.line(wback, point3, point4, (255, 0, 255), 5)
    #     m = cv2.moments(mask, binaryImage=True)
    #     cmx, cmy = (m['m10'] / m['m00'], m['m01'] / m['m00'])
    #     if y_coor - y <= 0:
    #         cv2.line(ori_img, (int(cmx), y), (int(cmx), y + height), (0, 255, 0), 3)
    #         cv2.line(wback, (int(cmx), y), (int(cmx), y + height), (0, 255, 0), 3)
    #     elif y_coor - y > 0:
    #         height_1 = y_coor - y
    #         if height - height_1 <= 0:
    #             cv2.line(ori_img, (int(cmx), y), (int(cmx), y + height), (255, 0, 0), 3)
    #             cv2.line(wback, (int(cmx), y), (int(cmx), y + height), (255, 0, 0), 3)
    #         else:
    #             cv2.line(ori_img, (int(cmx), y_coor - 2), (int(cmx), y_coor - height_above_bound), (255, 0, 0), 3)
    #             cv2.line(ori_img, (int(cmx), y_coor - 2), (int(cmx), y_coor + height_below_bound), (0, 255, 0), 3)
    #             cv2.line(wback, (int(cmx), y_coor - 2), (int(cmx), y_coor - height_above_bound), (255, 0, 0), 3)
    #             cv2.line(wback, (int(cmx), y_coor - 2), (int(cmx), y_coor + height_below_bound), (0, 255, 0), 3)
    #     if filename:
    #         # Output images with boundary line, above/below bound area
    #         extention = filename.split('.')[-1]
    #         # out_file = str(filename[0:-4]) + '_boundary' + str(line_position) + '.' + extention
    #         out_file = str(filename[0:-4]) + '_boundary' + str(line_position) + '.jpg'
    #         print_image(ori_img, out_file)
    #         analysis_images = ['IMAGE', 'boundary', out_file]
    #
    # if debug is not None:
    #     point3 = (0, y_coor - 4)
    #     point4 = (x_coor, y_coor - 4)
    #     cv2.line(ori_img, point3, point4, (255, 0, 255), 5)
    #     cv2.line(wback, point3, point4, (255, 0, 255), 5)
    #     m = cv2.moments(mask, binaryImage=True)
    #     cmx, cmy = (m['m10'] / m['m00'], m['m01'] / m['m00'])
    #     if y_coor - y <= 0:
    #         cv2.line(ori_img, (int(cmx), y), (int(cmx), y + height), (0, 255, 0), 3)
    #         cv2.line(wback, (int(cmx), y), (int(cmx), y + height), (0, 255, 0), 3)
    #     elif y_coor - y > 0:
    #         height_1 = y_coor - y
    #         if height - height_1 <= 0:
    #             cv2.line(ori_img, (int(cmx), y), (int(cmx), y + height), (255, 0, 0), 3)
    #             cv2.line(wback, (int(cmx), y), (int(cmx), y + height), (255, 0, 0), 3)
    #         else:
    #             cv2.line(ori_img, (int(cmx), y_coor - 2), (int(cmx), y_coor - height_above_bound), (255, 0, 0), 3)
    #             cv2.line(ori_img, (int(cmx), y_coor - 2), (int(cmx), y_coor + height_below_bound), (0, 255, 0), 3)
    #             cv2.line(wback, (int(cmx), y_coor - 2), (int(cmx), y_coor - height_above_bound), (255, 0, 0), 3)
    #             cv2.line(wback, (int(cmx), y_coor - 2), (int(cmx), y_coor + height_below_bound), (0, 255, 0), 3)
    #     if debug == 'print':
    #         print_image(wback, (str(device) + '_boundary_on_white.jpg'))
    #         print_image(ori_img, (str(device) + '_boundary_on_img.jpg'))
    #     if debug == 'plot':
    #         plot_image(wback)
    #         plot_image(ori_img)
    #
    # return device, bound_header, bound_data, analysis_images
