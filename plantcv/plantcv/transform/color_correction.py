# Color Corrections Functions

import os
import errno
import cv2
import numpy as np
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from plantcv.plantcv.roi import rectangle


def get_color_matrix(rgb_img, mask):
    """ Calculate the average value of pixels in each color chip for each color channel.

    Inputs:
    rgb_img         = RGB image with color chips visualized
    mask        = a gray-scale img with unique values for each segmented space, representing unique, discrete
                    color chips.

    Outputs:
    color_matrix        = a 22x4 matrix containing the average red value, average green value, and average blue value
                            for each color chip.
    headers             = a list of 4 headers corresponding to the 4 columns of color_matrix respectively

    :param rgb_img: numpy.ndarray
    :param mask: numpy.ndarray
    :return headers: string array
    :return color_matrix: numpy.ndarray
    """
    # Autoincrement the device counter
    params.device += 1

    # Check for RGB input
    if len(np.shape(rgb_img)) != 3:
        fatal_error("Input rgb_img is not an RGB image.")
    # Check mask for gray-scale
    if len(np.shape(mask)) != 2:
        fatal_error("Input mask is not an gray-scale image.")

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
    """ Calculate Moore-Penrose inverse matrix for use in calculating transformation_matrix

    Inputs:
    target_matrix       = a 22x4 matrix containing the average red value, average green value, and average blue value
                            for each color chip.
    source_matrix       = a 22x4 matrix containing the average red value, average green value, and average blue value
                            for each color chip.

    Outputs:
    matrix_a    = a concatenated 22x9 matrix of source_matrix red, green, and blue values to the powers 1, 2, 3
    matrix_m    = a 9x22 Moore-Penrose inverse matrix
    matrix_b    = a 22x9 matrix of linear, square, and cubic rgb values from target_img


    :param target_matrix: numpy.ndarray
    :param source_matrix: numpy.ndarray
    :return matrix_a: numpy.ndarray
    :return matrix_m: numpy.ndarray
    :return matrix_b: numpy.ndarray

    """

    # Autoincrement the device counter
    params.device += 1

    # if the number of chips in source_img match the number of chips in target_matrix
    if np.shape(target_matrix) == np.shape(source_matrix):
        t_cc, t_r, t_g, t_b = np.split(target_matrix, 4, 1)
        s_cc, s_r, s_g, s_b = np.split(source_matrix, 4, 1)
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
        t_cc, t_r, t_g, t_b, s_r, s_g, s_b = np.split(combined_matrix, 7, 1)
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
    matrix_a = np.concatenate((s_r, s_g, s_b, s_b2, s_g2, s_r2, s_b3, s_g3, s_r3), 1)
    # create matrix_m
    matrix_m = np.linalg.solve(np.matmul(matrix_a.T, matrix_a), matrix_a.T)
    # create matrix_b
    matrix_b = np.concatenate((t_r, t_r2, t_r3, t_g, t_g2, t_g3, t_b, t_b2, t_b3), 1)
    return matrix_a, matrix_m, matrix_b


def calc_transformation_matrix(matrix_m, matrix_b):
    """ Calculates transformation matrix (transformation_matrix).

    Inputs:
    matrix_m    = a 9x22 Moore-Penrose inverse matrix
    matrix_b    = a 22x9 matrix of linear, square, and cubic rgb values from target_img

    Outputs:
    1-t_det     = "deviance" the measure of how greatly the source image deviates from the target image's color space.
                    Two images of the same color space should have a deviance of ~0.
    transformation_matrix    = a 9x9 matrix of linear, square, and cubic transformation coefficients


    :param matrix_m: numpy.ndarray
    :param matrix_b: numpy.ndarray
    :return red: numpy.ndarray
    :return blue: numpy.ndarray
    :return green: numpy.ndarray
    :return 1-t_det: float
    :return transformation_matrix: numpy.ndarray
    """
    # check matrix_m and matrix_b are matrices
    if len(np.shape(matrix_b)) != 2 or len(np.shape(matrix_m)) != 2:
        fatal_error("matrix_m and matrix_b must be n x m matrices such that m,n != 1.")
    # check matrix_b has 9 columns
    if np.shape(matrix_b)[1] != 9:
        fatal_error("matrix_b must have 9 columns.")
    # check matrix_m and matrix_b for multiplication
    if np.shape(matrix_m)[0] != np.shape(matrix_b)[1] or np.shape(matrix_m)[1] != np.shape(matrix_b)[0]:
        fatal_error("Cannot multiply matrices.")

    # Autoincrement the device counter
    params.device += 1

    t_r, t_r2, t_r3, t_g, t_g2, t_g3, t_b, t_b2, t_b3 = np.split(matrix_b, 9, 1)

    # multiply each 22x1 matrix from target color space by matrix_m
    red = np.matmul(matrix_m, t_r)
    green = np.matmul(matrix_m, t_g)
    blue = np.matmul(matrix_m, t_b)

    red2 = np.matmul(matrix_m, t_r2)
    green2 = np.matmul(matrix_m, t_g2)
    blue2 = np.matmul(matrix_m, t_b2)

    red3 = np.matmul(matrix_m, t_r3)
    green3 = np.matmul(matrix_m, t_g3)
    blue3 = np.matmul(matrix_m, t_b3)

    # concatenate each product column into 9X9 transformation matrix
    transformation_matrix = np.concatenate((red, green, blue, red2, green2, blue2, red3, green3, blue3), 1)

    # find determinant of transformation matrix
    t_det = np.linalg.det(transformation_matrix)

    return 1-t_det, transformation_matrix


def apply_transformation_matrix(source_img, target_img, transformation_matrix):
    """ Apply the transformation matrix to the source_image.

    Inputs:
    source_img      = an RGB image to be corrected to the target color space
    target_img      = an RGB image with the target color space
    transformation_matrix        = a 9x9 matrix of tranformation coefficients

    Outputs:
    corrected_img    = an RGB image in correct color space

    :param source_img: numpy.ndarray
    :param target_img: numpy.ndarray
    :param transformation_matrix: numpy.ndarray
    :return corrected_img: numpy.ndarray
    """
    # check transformation_matrix for 9x9
    if np.shape(transformation_matrix) != (9, 9):
        fatal_error("transformation_matrix must be a 9x9 matrix of transformation coefficients.")
    # Check for RGB input
    if len(np.shape(source_img)) != 3:
        fatal_error("Source_img is not an RGB image.")

    # Autoincrement the device counter
    params.device += 1

    # split transformation_matrix
    red, green, blue, red2, green2, blue2, red3, green3, blue3 = np.split(transformation_matrix, 9, 1)

    # find linear, square, and cubic values of source_img color channels
    source_b, source_g, source_r = cv2.split(source_img)
    source_b2 = np.square(source_b)
    source_b3 = np.power(source_b, 3)
    source_g2 = np.square(source_g)
    source_g3 = np.power(source_g, 3)
    source_r2 = np.square(source_r)
    source_r3 = np.power(source_r, 3)

    # apply linear model to source color channels
    b = 0 + source_r * blue[0] + source_g * blue[1] + source_b * blue[2] + source_r2 * blue[3] + source_g2 * blue[
        4] + source_b2 * blue[5] + source_r3 * blue[6] + source_g3 * blue[7] + source_b3 * blue[8]
    g = 0 + source_r * green[0] + source_g * green[1] + source_b * green[2] + source_r2 * green[3] + source_g2 * green[
        4] + source_b2 * green[5] + source_r3 * green[6] + source_g3 * green[7] + source_b3 * green[8]
    r = 0 + source_r * red[0] + source_g * red[1] + source_b * red[2] + source_r2 * red[3] + source_g2 * red[
        4] + source_b2 * red[5] + source_r3 * red[6] + source_g3 * red[7] + source_b3 * red[8]

    # merge corrected color channels onto source_image
    bgr = [b, g, r]
    corrected_img = cv2.merge(bgr)

    # round corrected_img elements to be within range and of the correct data type
    corrected_img = np.rint(corrected_img)
    corrected_img[np.where(corrected_img > 255)] = 255
    corrected_img = corrected_img.astype(np.uint8)

    if params.debug == "print":
        # If debug is print, save the image to a file
        print_image(corrected_img, os.path.join(params.debug_outdir, str(params.device) + "_corrected.png"))
    elif params.debug == "plot":
        # If debug is plot, print a horizontal view of source_img, corrected_img, and target_img to the plotting device
        # plot horizontal comparison of source_img, corrected_img (with rounded elements) and target_img
        plot_image(np.hstack([source_img, corrected_img, target_img]))

    # return corrected_img
    return corrected_img


def save_matrix(matrix, filename):
    """ Serializes a matrix as an numpy.ndarray object and save to a .npz file.
    Inputs:
    matrix      = a numpy.matrix
    filename    = name of file to which matrix will be saved. Must end in .npz

    :param matrix: numpy.ndarray
    :param filename: string ending in ".npz"
    """
    if ".npz" not in filename:
        fatal_error("File must be an .npz file.")

    # Autoincrement the device counter
    params.device += 1

    np.savez(filename, matrix)


def load_matrix(filename):
    """ Deserializes from file an numpy.ndarray object as a matrix
    Inputs:
    filename    = .npz file to which a numpy.matrix or numpy.ndarray is saved

    Outputs:
    matrix      = a numpy.matrix

    :param filename: string ending in ".npz"
    :return matrix: numpy.matrix
    """

    # Autoincrement the device counter
    params.device += 1

    matrix_file = np.load(filename, encoding="latin1")
    matrix = matrix_file['arr_0']
    np.asmatrix(matrix)

    return matrix


def correct_color(target_img, target_mask, source_img, source_mask, output_directory):
    """Takes a target_img with preferred color_space and converts source_img to that color_space.
    Inputs:
    target_img          = an RGB image with color chips visualized
    source_img          = an RGB image with color chips visualized
    target_mask         = a gray-scale image with color chips and background each represented with unique values
    target_mask         = a gray-scale image with color chips and background each represented as unique values
    output_directory    = a file path to which outputs will be saved
    Outputs:
    target_matrix   = saved in .npz file, a 22x4 matrix containing the average red value, average green value, and
                            average blue value for each color chip.
    source_matrix   = saved in .npz file, a 22x4 matrix containing the average red value, average green value, and
                            average blue value for each color chip.
    transformation_matrix        = saved in .npz file, a 9x9 transformation matrix

    corrected_img   = the source_img converted to the correct color space.


    :param target_img: numpy.ndarray
    :param source_img: numpy.ndarray
    :param target_mask: numpy.ndarray
    :param source_mask: numpy.ndarray
    :param output_directory: string
    :return target_matrix: numpy.matrix
    :return source_matrix: numpy.matrix
    :return transformation_matrix: numpy.matrix
    :return corrected_img: numpy.ndarray
    """
    # check output_directory, if it does not exist, create
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    # get color matrices for target and source images
    target_headers, target_matrix = get_color_matrix(target_img, target_mask)
    source_headers, source_matrix = get_color_matrix(source_img, source_mask)

    # save target and source matrices
    save_matrix(target_matrix, os.path.join(output_directory, "target_matrix.npz"))
    save_matrix(source_matrix, os.path.join(output_directory, "source_matrix.npz"))

    # get matrix_m
    matrix_a, matrix_m, matrix_b = get_matrix_m(target_matrix=target_matrix, source_matrix=source_matrix)
    # calculate transformation_matrix and save
    deviance, transformation_matrix = calc_transformation_matrix(matrix_m, matrix_b)
    save_matrix(transformation_matrix, os.path.join(output_directory, "transformation_matrix.npz"))

    # apply transformation
    corrected_img = apply_transformation_matrix(source_img, target_img, transformation_matrix)

    return target_matrix, source_matrix, transformation_matrix, corrected_img


def create_color_card_mask(rgb_img, radius, start_coord, spacing, nrows, ncols, exclude=[]):
    """Create a labeled mask for color card chips
    Inputs:
    rgb_img        = Input RGB image data containing a color card.
    radius         = Radius of color masks.
    start_coord    = Two-element tuple of the first chip mask starting x and y coordinate.
    spacing        = Two-element tuple of the horizontal and vertical spacing between chip masks.
    nrows          = Number of chip rows.
    ncols          = Number of chip columns.
    exclude        = Optional list of chips to exclude. List in largest to smallest index (e.g. [20, 0])

    Returns:
    mask           = Labeled mask of chips

    :param rgb_img: numpy.ndarray
    :param radius: int
    :param start_coord: tuple
    :param spacing: tuple
    :param nrows: int
    :param ncols: int
    :param exclude: list
    :return mask: numpy.ndarray
    """
    # Initialize chip list
    chips = []
    # Store user debug
    debug = params.debug
    # Temporarily disable debug
    params.debug = None
    # Loop over each color card row
    for i in range(0, nrows):
        # The upper left corner is the y starting coordinate + the chip offset * the vertical spacing between chips
        y = start_coord[1] + i * spacing[1]
        # Loop over each column
        for j in range(0, ncols):
            # The upper left corner is the x starting coordinate + the chip offset * the
            # horizontal spacing between chips
            x = start_coord[0] + j * spacing[0]
            # Create a chip ROI
            chips.append(circle(img=rgb_img, x=x, y=y, r=radius))
    # Remove any excluded chips
    for chip in exclude:
        del chips[chip]
    # Create mask
    mask = np.zeros(shape=np.shape(rgb_img)[:2], dtype=np.uint8())
    # Mask label index
    i = 1
    # Draw labeled chip boxes on the mask
    for chip in chips:
        mask = cv2.drawContours(mask, chip[0], -1, (i * 10), -1)
        i += 1
    # Reset debug
    params.debug = debug
    if params.debug is not None:
        # Create a copy of the input image for plotting
        canvas = np.copy(rgb_img)
        # Draw chip ROIs on the canvas image
        for chip in chips:
            cv2.drawContours(canvas, chip[0], -1, (255, 255, 0), 5)
        if params.debug == "print":
            print_image(img=canvas, filename=os.path.join(params.debug_outdir,
                                                          str(params.device) + "_color_card_mask_rois.png"))
            print_image(img=mask, filename=os.path.join(params.debug_outdir,
                                                        str(params.device) + "_color_card_mask.png"))
        elif params.debug == "plot":
            plot_image(canvas)
    return mask


def quick_color_check(target_matrix, source_matrix, num_chips):
    """ Quickly plot target matrix values against source matrix values to determine
    over saturated color chips or other issues.

    Inputs:
    source_matrix      = a 22x4 matrix containing the average red value, average green value, and
                             average blue value for each color chip of the source image
    target_matrix      = a 22x4 matrix containing the average red value, average green value, and
                             average blue value for each color chip of the target image
    num_chips          = number of color card chips included in the matrices (integer)

    :param source_matrix: numpy.ndarray
    :param target_matrix: numpy.ndarray
    :param num_chips: int
    """
    # Imports
    from plotnine import ggplot, geom_point, geom_smooth, theme_seaborn, facet_grid, geom_label, scale_x_continuous, \
        scale_y_continuous, scale_color_manual, aes
    import pandas as pd

    # Extract and organize matrix info
    tr = target_matrix[:num_chips, 1:2]
    tg = target_matrix[:num_chips, 2:3]
    tb = target_matrix[:num_chips, 3:4]
    sr = source_matrix[:num_chips, 1:2]
    sg = source_matrix[:num_chips, 2:3]
    sb = source_matrix[:num_chips, 3:4]

    # Create columns of color labels
    red = []
    blue = []
    green = []
    for i in range(num_chips):
        red.append('red')
        blue.append('blue')
        green.append('green')

    # Make a column of chip numbers
    chip = np.arange(0, num_chips).reshape((num_chips, 1))
    chips = np.row_stack((chip, chip, chip))

    # Combine info
    color_data_r = np.column_stack((sr, tr, red))
    color_data_g = np.column_stack((sg, tg, green))
    color_data_b = np.column_stack((sb, tb, blue))
    all_color_data = np.row_stack((color_data_b, color_data_g, color_data_r))

    # Create a dataframe with headers
    dataset = pd.DataFrame({'source': all_color_data[:, 0], 'target': all_color_data[:, 1],
                            'color': all_color_data[:, 2]})

    # Add chip numbers to the dataframe
    dataset['chip'] = chips
    dataset = dataset.astype({'color': str, 'chip': str, 'target': float, 'source': float})

    # Make the plot
    p1 = ggplot(dataset, aes(x='target', y='source', color='color', label='chip')) + \
        geom_point(show_legend=False, size=2) + \
        geom_smooth(method='lm', size=.5, show_legend=False) + \
        theme_seaborn() + facet_grid('.~color') + \
        geom_label(angle=15, size=7, nudge_y=-.25, nudge_x=.5, show_legend=False) + \
        scale_x_continuous(limits=(-5, 270)) + scale_y_continuous(limits=(-5, 275)) + \
        scale_color_manual(values=['blue', 'green', 'red'])

    # Reset debug
    if params.debug is not None:
        if params.debug == 'print':
            p1.save(os.path.join(params.debug_outdir, 'color_quick_check.png'))
        elif params.debug == 'plot':
            print(p1)
