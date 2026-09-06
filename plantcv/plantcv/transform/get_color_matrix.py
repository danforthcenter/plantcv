"""Get RGB color values from a color card matrix"""
import numpy as np
from plantcv.plantcv import fatal_error


def get_color_matrix(rgb_img, mask):
    """Calculate the average value of pixels in each color chip for each color channel.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        an RGB image with color chips visualized
    mask : numpy.ndarray
        a gray-scale img with unique values for each segmented space, representing unique, discrete color chips.

    Returns
    -------
    color_matrix
        a 22x4 matrix containing the average red value, average green value, and average blue value for each color chip.
    headers
        a list of 4 headers corresponding to the 4 columns of color_matrix respectively
    """
    # Check for RGB input
    if len(np.shape(rgb_img)) != 3:
        fatal_error("Input rgb_img is not an RGB image.")
    # Check mask for gray-scale
    if len(np.shape(mask)) != 2:
        fatal_error("Input mask is not an gray-scale image.")

    img_dtype = rgb_img.dtype
    # normalization value as max number if the type is unsigned int
    max_val = 1.0
    if img_dtype.kind == 'u':
        max_val = np.iinfo(img_dtype).max

    # convert to float and normalize to work with values between 0-1
    rgb_img = rgb_img.astype(np.float64)/max_val

    # create empty color_matrix
    color_matrix = np.zeros((len(np.unique(mask))-1, 4))

    # create headers
    headers = ["chip_number", "r_avg", "g_avg", "b_avg"]

    # declare row_counter variable and initialize to 0
    row_counter = 0

    # for each unique color chip calculate each average RGB value
    for i in np.unique(mask):
        if i != 0:
            chip = rgb_img[np.where(mask == i)]
            color_matrix[row_counter][0] = i
            color_matrix[row_counter][1] = np.mean(chip[:, 2])
            color_matrix[row_counter][2] = np.mean(chip[:, 1])
            color_matrix[row_counter][3] = np.mean(chip[:, 0])
            row_counter += 1

    return headers, color_matrix


def get_matrix_m(target_matrix, source_matrix):
    """Calculate Moore-Penrose inverse matrix for transformation matrix calculation.

    Parameters
    ----------
    target_matrix : numpy.ndarray
        A 22x4 matrix containing the average red, green, and blue values
        for each color chip.
    source_matrix : numpy.ndarray
        A 22x4 matrix containing the average red, green, and blue values
        for each color chip.

    Returns
    -------
    matrix_a : numpy.ndarray
        A concatenated 22x9 matrix of source_matrix red, green, and blue
        values to the powers 1, 2, and 3.
    matrix_m : numpy.ndarray
        A 9x22 Moore-Penrose inverse matrix.
    matrix_b : numpy.ndarray
        A 22x9 matrix of linear, square, and cubic RGB values from
        target_matrix.
    """
    # if the number of chips in source_img match the number of chips in target_matrix
    if np.shape(target_matrix) == np.shape(source_matrix):
        t_mats = np.split(target_matrix, 4, 1)
        t_r, t_g, t_b = t_mats[1], t_mats[2], t_mats[3]
        s_mats = np.split(source_matrix, 4, 1)
        s_r, s_g, s_b = s_mats[1], s_mats[2], s_mats[3]
    else:
        combined_matrix = np.zeros((np.ma.size(source_matrix, 0), 7))
        row_count = 0
        for r in range(0, np.ma.size(target_matrix, 0)):
            for i in range(0, np.ma.size(source_matrix, 0)):
                if target_matrix[r][0] == source_matrix[i][0]:
                    combined_matrix[row_count][0] = target_matrix[r][0]
                    combined_matrix[row_count][1] = target_matrix[r][1]
                    combined_matrix[row_count][2] = target_matrix[r][2]
                    combined_matrix[row_count][3] = target_matrix[r][3]
                    combined_matrix[row_count][4] = source_matrix[i][1]
                    combined_matrix[row_count][5] = source_matrix[i][2]
                    combined_matrix[row_count][6] = source_matrix[i][3]
                    row_count += 1
        rgb_mats = np.split(combined_matrix, 7, 1)
        t_r, t_g, t_b, s_r, s_g, s_b = rgb_mats[1], rgb_mats[2], rgb_mats[3], rgb_mats[4], rgb_mats[5], rgb_mats[6]
    t_r2 = np.square(t_r)
    t_r3 = np.power(t_r, 3)
    t_g2 = np.square(t_g)
    t_g3 = np.power(t_g, 3)
    t_b2 = np.square(t_b)
    t_b3 = np.power(t_b, 3)
    s_r2 = np.square(s_r)
    s_r3 = np.power(s_r, 3)
    s_g2 = np.square(s_g)
    s_g3 = np.power(s_g, 3)
    s_b2 = np.square(s_b)
    s_b3 = np.power(s_b, 3)

    # create matrix_a
    matrix_a = np.concatenate((s_r, s_g, s_b, s_r2, s_g2, s_b2, s_r3, s_g3, s_b3), 1)
    # create matrix_m
    matrix_m = np.linalg.solve(np.matmul(matrix_a.T, matrix_a), matrix_a.T)
    # create matrix_b
    matrix_b = np.concatenate((t_r, t_r2, t_r3, t_g, t_g2, t_g3, t_b, t_b2, t_b3), 1)
    return matrix_a, matrix_m, matrix_b
