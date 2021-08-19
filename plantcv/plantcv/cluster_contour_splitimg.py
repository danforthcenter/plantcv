import sys
import os
import cv2
import numpy as np
from datetime import datetime
from plantcv.plantcv import print_image
from plantcv.plantcv import apply_mask
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def cluster_contour_splitimg(img, grouped_contour_indexes, contours, hierarchy, outdir=None, file=None,
                             filenames=None):

    """
    This function takes clustered contours and splits them into multiple images, also does a check to make sure that
    the number of inputted filenames matches the number of clustered contours.

    Inputs:
    img                     = image data
    grouped_contour_indexes = output of cluster_contours, indexes of clusters of contours
    contours                = contours to cluster, output of cluster_contours
    hierarchy               = hierarchy of contours, output of find_objects
    outdir                  = out directory for output images
    file                    = the name of the input image to use as a plantcv name,
                              output of filename from read_image function
    filenames               = input txt file with list of filenames in order from top to bottom left to right
                              (likely list of genotypes)

    Returns:
    output_path             = array of paths to output images

    :param img: numpy.ndarray
    :param grouped_contour_indexes: list
    :param contours: list
    :param hierarchy: numpy.ndarray
    :param outdir: str
    :param file: str
    :param filenames: str
    :return output_path: str
    """

    params.device += 1

    sys.stderr.write(
        'This function has been updated to include object hierarchy so object holes can be included\n')

    i = datetime.now()
    timenow = i.strftime('%m-%d-%Y_%H:%M:%S')

    if file is None:
        filebase = timenow
    else:
        filebase = os.path.splitext(file)[0]

    if filenames is None:
        namelist = []
        for x in range(0, len(grouped_contour_indexes)):
            namelist.append(x)
    else:
        with open(filenames, 'r') as n:
            namelist = n.read().splitlines()
        n.close()

    # make sure the number of objects matches the namelist, and if not, remove the smallest grouped countor
    # removing contours is not ideal but the lists don't match there is a warning to check output
    if len(namelist) == len(grouped_contour_indexes):
        corrected_contour_indexes = grouped_contour_indexes
    elif len(namelist) < len(grouped_contour_indexes):
        print("Warning number of names is less than number of grouped contours, attempting to fix, to double check "
              "output")
        diff = len(grouped_contour_indexes) - len(namelist)
        size = []
        for i, x in enumerate(grouped_contour_indexes):
            totallen = []
            for a in x:
                g = i
                la = len(contours[a])
                totallen.append(la)
            sumlen = np.sum(totallen)
            size.append((sumlen, g, i))

        dtype = [('len', int), ('group', list), ('index', int)]
        lencontour = np.array(size, dtype=dtype)
        lencontour = np.sort(lencontour, order='len')

        rm_contour = lencontour[diff:]
        rm_contour = np.sort(rm_contour, order='group')
        corrected_contour_indexes = []

        for x in rm_contour:
            index = x[2]
            corrected_contour_indexes.append(grouped_contour_indexes[index])

    elif len(namelist) > len(grouped_contour_indexes):
        print("Warning number of names is more than number of  grouped contours, double check output")
        diff = len(namelist) - len(grouped_contour_indexes)
        namelist = namelist[0:-diff]
        corrected_contour_indexes = grouped_contour_indexes

    # create filenames
    group_names = []
    group_names1 = []
    for i, x in enumerate(namelist):
        plantname = str(filebase) + '_' + str(x) + '_p' + str(i) + '.png'
        maskname = str(filebase) + '_' + str(x) + '_p' + str(i) + '_mask.png'
        group_names.append(plantname)
        group_names1.append(maskname)

    # split image
    output_path = []
    output_imgs = []
    output_masks = []

    for y, x in enumerate(corrected_contour_indexes):
        if outdir is not None:
            savename = os.path.join(str(outdir), group_names[y])
            savename1 = os.path.join(str(outdir), group_names1[y])
        else:
            savename = os.path.join(".", group_names[y])
            savename1 = os.path.join(".", group_names1[y])
        iy, ix = np.shape(img)[:2]
        mask = np.zeros((iy, ix, 3), dtype=np.uint8)
        masked_img = np.copy(img)
        for a in x:
            if hierarchy[0][a][3] > -1:
                cv2.drawContours(mask, contours, a, (0, 0, 0), -1, lineType=8, hierarchy=hierarchy)
            else:
                cv2.drawContours(mask, contours, a, (255, 255, 255), -1, lineType=8, hierarchy=hierarchy)

        mask_binary = mask[:, :, 0]

        if np.sum(mask_binary) == 0:
            pass
        else:
            retval, mask_binary = cv2.threshold(mask_binary, 254, 255, cv2.THRESH_BINARY)
            masked1 = apply_mask(masked_img, mask_binary, 'white')
            output_imgs.append(masked1)
            output_masks.append(mask_binary)
            if outdir is not None:
                print_image(masked1, savename)
                print_image(mask_binary, savename1)
            output_path.append(savename)

            _debug(visual=masked1, filename=os.path.join(params.debug_outdir, str(params.device) + '_clusters.png'))
            _debug(visual=mask_binary, filename=os.path.join(params.debug_outdir, str(params.device) + '_clusters_mask.png'))

    return output_path, output_imgs, output_masks
