"""Color Corrections Functions."""
import os
import math
import cv2
import numpy as np
import altair as alt
import pandas as pd
from plantcv.plantcv import params, outputs, fatal_error
from plantcv.plantcv.roi import circle
from plantcv.plantcv._debug import _debug


def affine_color_correction(rgb_img, source_matrix, target_matrix):
    """Affine color correction of RGB image.

    Correct the color of the input image based on the target color matrix using an affine transformation
    in the RGB space. The vector containing the regression coefficients is calculated as the one that minimizes the
    Euclidean distance between the transformed source color values and the target color values.

    Inputs:
    rgb_img         = an RGB image with color chips visualized
    source_matrix   = array of RGB color values (intensity in the range [0-1]) from
                      the image to be corrected where each row is one
                      color reference and the columns are organized as index,R,G,B
    target_matrix   = array of target RGB color values (intensity in the range [0-1])
                      where each row is one color reference and the columns are
                      organized as index,R,G,B

    Outputs:
    corrected_img   = color corrected image


    :param rgb_img: numpy.ndarray
    :return source_matrix: numpy.ndarray
    :return target_matrix: numpy.ndarray
    :return corrected_img: numpy.ndarray
    """
    # matrices must have the same number of color references
    if source_matrix.shape != target_matrix.shape:
        fatal_error("Missmatch between the color matrices' shapes")

    h, w, c = rgb_img.shape

    # number of references
    n = source_matrix.shape[0]

    # the column zero (index) of the matrices is not used in this model
    # augment matrix of source values with a column of 1s for the constant part of
    # the affine transformation
    S = np.concatenate((source_matrix[:, 1:].copy(), np.ones((n, 1))), axis=1)

    # make vectors of taget values for each color
    T = target_matrix[:, 1:].copy()
    tr = T[:, 0]
    tg = T[:, 1]
    tb = T[:, 2]

    # calculate regression vector for each color as the pseudoinverse of the source
    # values matrix multiplied by each color target vector
    ar = np.matmul(np.linalg.pinv(S), tr)
    ag = np.matmul(np.linalg.pinv(S), tg)
    ab = np.matmul(np.linalg.pinv(S), tb)

    img_rgb = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2RGB)
    # reshape image as a 2D array where the rows are pixels and the colums are color channels
    # and augment the channels with a column of 1s for the affine transformation
    img_pix = np.concatenate((img_rgb.reshape(h*w, c).astype(np.float64)/255, np.ones((h*w, 1))), axis=1)

    # calculate the corrected colors, eliminate values outside the range [0-1] and
    # convert to [0-255] unit8
    img_r_cc = (255*np.clip(np.matmul(img_pix, ar), 0, 1)).astype(np.uint8)
    img_g_cc = (255*np.clip(np.matmul(img_pix, ag), 0, 1)).astype(np.uint8)
    img_b_cc = (255*np.clip(np.matmul(img_pix, ab), 0, 1)).astype(np.uint8)

    # reconstruct the RGB (actually BGR for openCV) image
    corrected_img = np.stack((img_b_cc, img_g_cc, img_r_cc), axis=1).reshape(h, w, c)

    # For debugging, create a horizontal view of the image before and after color correction
    debug_img = np.hstack([rgb_img, corrected_img])
    _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, str(params.device) + '_affine_corrected.png'))

    return corrected_img


def std_color_matrix(pos=0):
    """Create a standard color matrix.

    Standard color values compatible with the x-rite ColorCheker Classic,
    ColorChecker Mini, and ColorChecker Passport targets.
    Source: https://en.wikipedia.org/wiki/ColorChecker

    Inputs:
    pos     = reference value indicating orientation of the color card. The reference
                is based on the position of the white chip:

                pos = 0: bottom-left corner
                pos = 1: bottom-right corner
                pos = 2: top-right corner
                pos = 3: top-left corner

    Outputs:
    color_matrix    = matrix containing the standard red, green, and blue
                        values for each color chip

    :param pos: int
    :return color_matrix: numpy.ndarray
    """
    # list of rgb values as indicated in the color card specs. They need to be
    # aranged depending on the orientation of the color card of reference in the
    # image to be corrected.
    values_list = np.array([[115, 82, 68],  # dark skin
                            [194, 150, 130],  # light skin
                            [98, 122, 157],  # blue sky
                            [87, 108, 67],  # foliage
                            [133, 128, 177],  # blue flower
                            [103, 189, 170],  # bluish green
                            [214, 126, 44],  # orange
                            [80, 91, 166],  # purplish blue
                            [193, 90, 99],  # moderate red
                            [94, 60, 108],  # purple
                            [157, 188, 64],  # yellow green
                            [224, 163, 46],  # orange yellow
                            [56, 61, 150],  # blue
                            [70, 148, 73],  # green
                            [175, 54, 60],  # red
                            [231, 199, 31],  # yellow
                            [187, 86, 149],  # magenta
                            [8, 133, 161],  # cyan
                            [243, 243, 242],  # white (.05*)
                            [200, 200, 200],  # neutral 8 (.23*)
                            [160, 160, 160],  # neutral 6.5 (.44*)
                            [122, 122, 121],  # neutral 5 (.7*)
                            [85, 85, 85],  # neutral 3.5 (1.05*)
                            [52, 52, 52]], dtype=np.float64)  # black (1.50*)

    pos = math.floor(pos)
    if (pos < 0) or (pos > 3):
        fatal_error("white chip position reference 'pos' must be a value among {0, 1, 2, 3}")

    N_chips = values_list.shape[0]

    # array of indices from 1 to N chips in order to match the chip numbering
    # in the color card specs. Later when used for indexing, we substract the 1.
    idx = np.arange(N_chips)+1
    # indices in the shape of the color card
    cc_indices = idx.reshape((4, 6), order='C')
    # rotate the indices depending on the specified orientation
    cc_indices_rot = np.rot90(cc_indices, k=pos, axes=(0, 1))
    # arange color values based on the indices
    color_matrix_wo_chip_nb = values_list[(cc_indices_rot-1).reshape(-1), :]/255.

    # add chip number compatible with other PlantCV functions
    chip_nb = np.arange(10, 10*N_chips+1, 10)
    color_matrix = np.concatenate((chip_nb.reshape(N_chips, 1), color_matrix_wo_chip_nb), axis=1)

    return color_matrix


def get_color_matrix(rgb_img, mask):
    """Calculate the average value of pixels in each color chip for each color channel.

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
    """Calculate Moore-Penrose inverse matrix for use in calculating transformation_matrix.

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
    matrix_a = np.concatenate((s_r, s_g, s_b, s_r2, s_g2, s_b2, s_r3, s_g3, s_b3), 1)
    # create matrix_m
    matrix_m = np.linalg.solve(np.matmul(matrix_a.T, matrix_a), matrix_a.T)
    # create matrix_b
    matrix_b = np.concatenate((t_r, t_r2, t_r3, t_g, t_g2, t_g3, t_b, t_b2, t_b3), 1)
    return matrix_a, matrix_m, matrix_b


def calc_transformation_matrix(matrix_m, matrix_b):
    """Calculate a transformation matrix (transformation_matrix).

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
    """Apply the transformation matrix to the source_image.

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

    # split transformation_matrix
    red, green, blue, red2, green2, blue2, red3, green3, blue3 = np.split(transformation_matrix, 9, 1)

    source_dtype = source_img.dtype
    # normalization value as max number if the type is unsigned int
    max_val = 1.0
    if source_dtype.kind == 'u':
        max_val = np.iinfo(source_dtype).max
    # convert img to float to avoid integer overflow, normalize between 0-1
    source_flt = source_img.astype(np.float64)/max_val
    # find linear, square, and cubic values of source_img color channels
    source_b, source_g, source_r = cv2.split(source_flt)
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

    # return values of the image to the original range
    corrected_img = max_val*np.clip(corrected_img, 0, 1)
    # cast back to original dtype (if uint the value defaults to the closest smaller integer)
    corrected_img = corrected_img.astype(source_dtype)

    # For debugging, create a horizontal view of source_img, corrected_img, and target_img to the plotting device
    # plot horizontal comparison of source_img, corrected_img (with rounded elements) and target_img
    out_img = np.hstack([source_img, corrected_img, target_img])
    # Change range of visualization image to 0-255 and convert to uin8
    out_img = ((255.0/max_val)*out_img).astype(np.uint8)
    _debug(visual=out_img, filename=os.path.join(params.debug_outdir, str(params.device) + '_corrected.png'))

    # return corrected_img
    return corrected_img


def save_matrix(matrix, filename):
    """Serialize a matrix as an numpy.ndarray object and save to a .npz file.

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
    """Deserializes from file an numpy.ndarray object as a matrix.

    Inputs:
    filename    = .npz file to which a numpy.matrix or numpy.ndarray is saved

    Outputs:
    matrix      = a numpy.matrix

    :param filename: string ending in ".npz"
    :return matrix: numpy.matrix
    """
    matrix_file = np.load(filename, encoding="latin1")
    matrix = matrix_file['arr_0']
    np.asmatrix(matrix)

    return matrix


def correct_color(target_img, target_mask, source_img, source_mask, output_directory):
    """Take a target_img with preferred color_space and convert source_img to that color_space.

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
    """Create a labeled mask for color card chips.

    Inputs:
    rgb_img        = Input RGB image data containing a color card.
    radius         = Radius of color masks.
    start_coord    = Two-element tuple of the first chip mask starting x and y coordinate.
    spacing        = Two-element tuple of the horizontal and vertical spacing between chip masks.
    nrows          = Number of chip rows.
    ncols          = Number of chip columns.
    exclude        = Optional list of chips to exclude.

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
    # Store debug mode
    debug = params.debug
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
    # Restore debug parameter
    params.debug = debug
    # Sort excluded chips from largest to smallest
    exclude.sort(reverse=True)
    # Remove any excluded chips
    for chip in exclude:
        del chips[chip]
    # Create mask
    mask = np.zeros(shape=np.shape(rgb_img)[:2], dtype=np.uint8())
    # Mask label index
    i = 1
    # Draw labeled chip boxes on the mask
    for chip in chips:
        mask = cv2.drawContours(mask, chip.contours[0], -1, (i * 10), -1)
        i += 1
    # Create a copy of the input image for plotting
    canvas = np.copy(rgb_img)
    # Draw chip ROIs on the canvas image
    for chip in chips:
        cv2.drawContours(canvas, chip.contours[0], -1, (255, 255, 0), params.line_thickness)
    _debug(visual=canvas, filename=os.path.join(params.debug_outdir, str(params.device) + '_color_card_mask_rois.png'))
    _debug(visual=mask, filename=os.path.join(params.debug_outdir, str(params.device) + '_color_card_mask.png'))
    return mask


def quick_color_check(target_matrix, source_matrix, num_chips):
    """Plot the color values of a target and source color card matrix.

    Quickly plot target matrix values against source matrix values to determine
    over saturated color chips or other issues.

    Inputs:
    source_matrix      = an nrowsXncols matrix containing the avg red, green, and blue values for each color chip
                            of the source image
    target_matrix      = an nrowsXncols matrix containing the avg red, green, and blue values for each color chip
                            of the target image
    num_chips          = number of color card chips included in the matrices (integer)

    Returns:
    p1                 = an altair plot of the target and source color values

    :param source_matrix: numpy.ndarray
    :param target_matrix: numpy.ndarray
    :param num_chips: int
    :return p1: altair.vegalite.v5.api.Chart
    """
    # Scale matrices to 0-255
    target_matrix = 255*target_matrix
    source_matrix = 255*source_matrix

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
    p1 = alt.Chart(dataset).mark_point(point=True).encode(
        x="target",
        y="source",
        color=alt.Color("color").scale(range=["blue", "green", "red"]),
        column="color"
        ).interactive()

    _debug(visual=p1, filename=os.path.join(params.debug_outdir, 'color_quick_check.png'))

    return p1


def find_color_card(rgb_img, threshold_type='adaptgauss', threshvalue=125, blurry=False, background='dark',
                    record_chip_size="median", label=None):
    """Automatically detect a color card and output info to use in create_color_card_mask function.

    Algorithm written by Brandon Hurr. Updated and implemented into PlantCV by Haley Schuhl.

        Inputs:
    rgb_img          = Input RGB image data containing a color card.
    threshold_type   = Threshold method, either 'normal', 'otsu', or 'adaptgauss', optional (default 'adaptgauss')
    threshvalue      = Thresholding value, optional (default 125)
    blurry           = Bool (default False) if True then image sharpening applied
    background       = Type of image background either 'dark' or 'light' (default 'dark'); if 'light' then histogram
                       expansion applied to better detect edges, but histogram expansion will be hindered if there
                       is a dark background
    record_chip_size = Optional str for choosing chip size measurement to be recorded, either "median",
                       "mean", or None
    label            = Optional label parameter, modifies the variable name of
                       observations recorded (default = pcv.params.sample_label).

    Returns:
    df             = Dataframe containing information about the filtered contours
    start_coord    = Two element tuple of starting coordinates, location of the top left pixel detected
    spacing        = Two element tuple of spacing between centers of chips

    :param rgb_img: numpy.ndarray
    :param threshold_type: str
    :param threshvalue: int
    :param blurry: bool
    :param background: str
    :param record_chip_size: str
    :param label: str
    :return df: pandas.core.frame.DataFrame
    :return start_coord: tuple
    :return spacing: tuple
    """
    # Imports
    import skimage
    import pandas as pd
    from scipy.spatial.distance import squareform, pdist

    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    # Get image attributes
    height, width, channels = rgb_img.shape
    total_pix = float(height * width)

    # Minimum and maximum square size based upon 12 MP image
    min_area = 1000. / 12000000. * total_pix
    max_area = 8000000. / 12000000. * total_pix

    # Create gray image for further processing
    gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)

    # Laplacian Fourier Transform detection of blurriness
    blurfactor = cv2.Laplacian(gray_img, cv2.CV_64F).var()

    # If image is blurry then try to deblur using kernel
    if blurry:
        # from https://www.packtpub.com/mapt/book/Application+Development/9781785283932/2/ch02lvl1sec22/Sharpening
        kernel = np.array([[-1, -1, -1, -1, -1],
                           [-1, 2, 2, 2, -1],
                           [-1, 2, 8, 2, -1],
                           [-1, 2, 2, 2, -1],
                           [-1, -1, -1, -1, -1]]) / 8.0
        # Store result back out for further processing
        gray_img = cv2.filter2D(gray_img, -1, kernel)

    # In darker samples, the expansion of the histogram hinders finding the squares due to problems with the otsu
    # thresholding. If your image has a bright background then apply
    if background == 'light':
        clahe = cv2.createCLAHE(clipLimit=3.25, tileGridSize=(4, 4))
        # apply CLAHE histogram expansion to find squares better with canny edge detection
        gray_img = clahe.apply(gray_img)
    elif background != 'dark':
        fatal_error('Background parameter ' + str(background) + ' is not "light" or "dark"!')

    # Thresholding
    if threshold_type.upper() == "OTSU":
        # Blur slightly so defects on card squares and background patterns are less likely to be picked up
        gaussian = cv2.GaussianBlur(gray_img, (5, 5), 0)
        ret, threshold = cv2.threshold(gaussian, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif threshold_type.upper() == "NORMAL":
        # Blur slightly so defects on card squares and background patterns are less likely to be picked up
        gaussian = cv2.GaussianBlur(gray_img, (5, 5), 0)
        ret, threshold = cv2.threshold(gaussian, threshvalue, 255, cv2.THRESH_BINARY)
    elif threshold_type.upper() == "ADAPTGAUSS":
        # Blur slightly so defects on card squares and background patterns are less likely to be picked up
        gaussian = cv2.GaussianBlur(gray_img, (11, 11), 0)
        threshold = cv2.adaptiveThreshold(gaussian, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV, 51, 2)
    else:
        fatal_error('Input threshold_type=' + str(threshold_type) + ' but should be "otsu", "normal", or "adaptgauss"!')

    # Apply automatic Canny edge detection using the computed median
    canny_edges = skimage.feature.canny(threshold)
    canny_edges.dtype = 'uint8'

    # Compute contours to find the squares of the card
    contours, hierarchy = cv2.findContours(canny_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    # Variable of which contour is which
    mindex = []
    # Variable to store moments
    mu = []
    # Variable to x,y coordinates in tuples
    mc = []
    # Variable to x coordinate as integer
    mx = []
    # Variable to y coordinate as integer
    my = []
    # Variable to store area
    marea = []
    # Variable to store whether something is a square (1) or not (0)
    msquare = []
    # Variable to store square approximation coordinates
    msquarecoords = []
    # Variable to store child hierarchy element
    mchild = []
    # Fitted rectangle height
    mheight = []
    # Fitted rectangle width
    mwidth = []
    # Ratio of height/width
    mwhratio = []

    # Extract moments from contour image
    for x in range(0, len(contours)):
        mu.append(cv2.moments(contours[x]))
        marea.append(cv2.contourArea(contours[x]))
        mchild.append(int(hierarchy[0][x][2]))
        mindex.append(x)

    # Cycle through moment data and compute location for each moment
    for m in mu:
        if m['m00'] != 0:  # This is the area term for a moment
            mc.append((int(m['m10'] / m['m00']), int(m['m01']) / m['m00']))
            mx.append(int(m['m10'] / m['m00']))
            my.append(int(m['m01'] / m['m00']))
        else:
            mc.append((0, 0))
            mx.append((0))
            my.append((0))

    # Loop over our contours and extract data about them
    for index, c in enumerate(contours):
        # Area isn't 0, but greater than min-area and less than max-area
        if marea[index] != 0 and min_area < marea[index] < max_area:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.1 * peri, True)
            center, wh, angle = cv2.minAreaRect(c)  # Rotated rectangle
            mwidth.append(wh[0])
            mheight.append(wh[1])
            # In different versions of OpenCV, width and height can be listed in a different order
            # To normalize the ratio we sort them and take the ratio of the longest / shortest
            wh_sorted = list(wh)
            wh_sorted.sort()
            mwhratio.append(wh_sorted[1] / wh_sorted[0])
            msquare.append(len(approx))
            # If the approx contour has 4 points then we can assume we have 4-sided objects
            if len(approx) in (4, 5):
                msquarecoords.append(approx)
            else:  # It's not square
                msquarecoords.append(0)
        else:  # Contour has area of 0, not interesting
            msquare.append(0)
            msquarecoords.append(0)
            mwidth.append(0)
            mheight.append(0)
            mwhratio.append(0)

    # Make a pandas df from data for filtering out junk
    all_contours = {'index': mindex, 'x': mx, 'y': my, 'width': mwidth, 'height': mheight, 'res_ratio': mwhratio,
                    'area': marea, 'square': msquare, 'child': mchild}
    df = pd.DataFrame(all_contours)

    # Add calculated blur factor to output
    df['blurriness'] = blurfactor

    # Filter df for attributes that would isolate squares of reasonable size
    df = df[(df['area'] > min_area) & (df['area'] < max_area) & (df['child'] != -1) &
            (df['square'].isin([4, 5])) & (df['res_ratio'] < 1.2) & (df['res_ratio'] > 0.85)]

    # Filter nested squares from dataframe, was having issues with median being towards smaller nested squares
    df = df[~(df['index'].isin(df['index'] + 1))]

    # Count up squares that are within a given radius, more squares = more likelihood of them being the card
    # Median width of square time 2.5 gives proximity radius for searching for similar squares
    median_sq_width_px = df["width"].median()

    # Squares that are within 6 widths of the current square
    pixeldist = median_sq_width_px * 6
    # Computes euclidean distance matrix for the x and y contour centroids
    distmatrix = pd.DataFrame(squareform(pdist(df[['x', 'y']])))
    # Add up distances that are less than  ones have distance less than pixeldist pixels
    distmatrixflat = distmatrix.apply(lambda dist: dist[dist <= pixeldist].count() - 1, axis=1)

    # Append distprox summary to dataframe
    df = df.assign(distprox=distmatrixflat.values)

    # Compute how similar in area the squares are. lots of similar values indicates card isolate area measurements
    filtered_area = df['area']
    # Create empty matrix for storing comparisons
    sizecomp = np.zeros((len(filtered_area), len(filtered_area)))
    # Double loop through all areas to compare to each other
    for p in range(0, len(filtered_area)):
        for o in range(0, len(filtered_area)):
            big = max(filtered_area.iloc[p], filtered_area.iloc[o])
            small = min(filtered_area.iloc[p], filtered_area.iloc[o])
            pct = 100. * (small / big)
            sizecomp[p][o] = pct

    # How many comparisons given 90% square similarity
    sizematrix = pd.DataFrame(sizecomp).apply(lambda sim: sim[sim >= 90].count() - 1, axis=1)

    # Append sizeprox summary to dataframe
    df = df.assign(sizeprox=sizematrix.values)

    # Reorder dataframe for better printing
    df = df[['index', 'x', 'y', 'width', 'height', 'res_ratio', 'area', 'square', 'child',
             'blurriness', 'distprox', 'sizeprox']]

    # Loosely filter for size and distance (relative size to median)
    minsqwidth = median_sq_width_px * 0.80
    maxsqwidth = median_sq_width_px * 1.2
    df = df[(df['distprox'] >= 5) & (df['sizeprox'] >= 5) & (df['width'] > minsqwidth) &
            (df['width'] < maxsqwidth)]

    # Filter for proximity again to root out stragglers. Find and count up squares that are within given radius,
    # more squares = more likelihood of them being the card. Median width of square time 2.5 gives proximity radius
    # for searching for similar squares
    median_sq_width_px = df["width"].median()

    # Squares that are within 6 widths of the current square
    pixeldist = median_sq_width_px * 5
    # Computes euclidean distance matrix for the x and y contour centroids
    distmatrix = pd.DataFrame(squareform(pdist(df[['x', 'y']])))
    # Add up distances that are less than  ones have distance less than pixeldist pixels
    distmatrixflat = distmatrix.apply(lambda dist: dist[dist <= pixeldist].count() - 1, axis=1)

    # Append distprox summary to dataframe
    df = df.assign(distprox=distmatrixflat.values)

    # Filter results for distance proximity to other squares
    df = df[(df['distprox'] >= 4)]
    # Remove all not numeric values use to_numeric with parameter, errors='coerce' - it replace non numeric to NaNs:
    df['x'] = pd.to_numeric(df['x'], errors='coerce')
    df['y'] = pd.to_numeric(df['y'], errors='coerce')

    # Remove NaN
    df = df.dropna()

    if df['x'].min() is np.nan or df['y'].min() is np.nan:
        fatal_error('No color card found under current parameters')
    else:
        # Extract the starting coordinate
        start_coord = (df['x'].min(), df['y'].min())

        # start_coord = (int(df['X'].min()), int(df['Y'].min()))
        # Calculate the range
        spacingx_short = (df['x'].max() - df['x'].min()) / 3
        spacingy_short = (df['y'].max() - df['y'].min()) / 3
        spacingx_long = (df['x'].max() - df['x'].min()) / 5
        spacingy_long = (df['y'].max() - df['y'].min()) / 5
        # Chip spacing since 4x6 card assumed
        spacing_short = min(spacingx_short, spacingy_short)
        spacing_long = max(spacingx_long, spacingy_long)
        # Smaller spacing measurement might have a chip missing
        spacing = int(max(spacing_short, spacing_long))
        spacing = (spacing, spacing)

    if record_chip_size is not None:
        if record_chip_size.upper() == "MEDIAN":
            chip_size = df.loc[:, "area"].median()
            chip_height = df.loc[:, "height"].median()
            chip_width = df.loc[:, "width"].median()
        elif record_chip_size.upper() == "MEAN":
            chip_size = df.loc[:, "area"].mean()
            chip_height = df.loc[:, "height"].mean()
            chip_width = df.loc[:, "width"].mean()
        else:
            print(str(record_chip_size) + " Is not a valid entry for record_chip_size." +
                  " Must be either 'mean', 'median', or None.")
            chip_size = None
            chip_height = None
            chip_width = None
        # Store into global measurements
        outputs.add_observation(sample=label, variable='color_chip_size', trait='size of color card chips identified',
                                method='plantcv.plantcv.transform.find_color_card', scale='none',
                                datatype=float, value=chip_size, label=str(record_chip_size))
        method = record_chip_size.lower()
        outputs.add_observation(sample=label, variable=f'{method}_color_chip_height',
                                trait=f'{method} height of color card chips identified',
                                method='plantcv.plantcv.transform.find_color_card', scale='none',
                                datatype=float, value=chip_height, label=str(record_chip_size))
        outputs.add_observation(sample=label, variable=f'{method}_color_chip_width',
                                trait=f'{method} size of color card chips identified',
                                method='plantcv.plantcv.transform.find_color_card', scale='none',
                                datatype=float, value=chip_width, label=str(record_chip_size))

    return df, start_coord, spacing
