# Color Corrections Functions

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import plot_image
from plantcv.plantcv.roi import circle
from plantcv.plantcv import print_image
from plantcv.plantcv import fatal_error


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
    # Check for RGB input
    if len(np.shape(rgb_img)) != 3:
        fatal_error("Input rgb_img is not an RGB image.")
    # Check mask for gray-scale
    if len(np.shape(mask)) != 2:
        fatal_error("Input mask is not an gray-scale image.")

    # convert to float and normalize to work with values between 0-1
    rgb_img = rgb_img.astype(np.float64)/255

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

    # convert img to float to avoid integer overflow, normalize between 0-1
    source_img = source_img.astype(np.float64)/255
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

    # return values of the image to the 0-255 range
    corrected_img = 255*np.clip(corrected_img, 0, 1)
    corrected_img = np.floor(corrected_img)
    # cast back to unsigned int
    corrected_img = corrected_img.astype(np.uint8)

    if params.debug == "print":
        # If debug is print, save the image to a file
        print_image(corrected_img, os.path.join(params.debug_outdir, str(params.device) + "_corrected.png"))
    elif params.debug == "plot":
        # If debug is plot, print a horizontal view of source_img, corrected_img, and target_img to the plotting device
        # plot horizontal comparison of source_img, corrected_img (with rounded elements) and target_img
        # cast source_img back to unsigned int between 0-255 for visualization
        source_img = (255*source_img).astype(np.uint8)
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

    # Autoincrement the device counter
    params.device += 1
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
        mask = cv2.drawContours(mask, chip[0], -1, (i * 10), -1)
        i += 1
    if params.debug is not None:
        # Create a copy of the input image for plotting
        canvas = np.copy(rgb_img)
        # Draw chip ROIs on the canvas image
        for chip in chips:
            cv2.drawContours(canvas, chip[0], -1, (255, 255, 0), params.line_thickness)
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
    source_matrix      = an nrowsXncols matrix containing the avg red, green, and blue values for each color chip
                            of the source image
    target_matrix      = an nrowsXncols matrix containing the avg red, green, and blue values for each color chip
                            of the target image
    num_chips          = number of color card chips included in the matrices (integer)

    :param source_matrix: numpy.ndarray
    :param target_matrix: numpy.ndarray
    :param num_chips: int
    """
    # Imports
    from plotnine import ggplot, geom_point, geom_smooth, theme_seaborn, facet_grid, geom_label, scale_x_continuous, \
        scale_y_continuous, scale_color_manual, aes
    import pandas as pd

    # Scale matrices back to 0-255
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
    p1 = ggplot(dataset, aes(x='target', y='source', color='color', label='chip')) + \
        geom_point(show_legend=False, size=2) + \
        geom_smooth(method='lm', size=.5, show_legend=False) + \
        theme_seaborn() + facet_grid('.~color') + \
        geom_label(angle=15, size=7, nudge_y=-.25, nudge_x=.5, show_legend=False) + \
        scale_x_continuous(limits=(-5, 270)) + scale_y_continuous(limits=(-5, 275)) + \
        scale_color_manual(values=['blue', 'green', 'red'])

    # Autoincrement the device counter
    params.device += 1

    # Reset debug
    if params.debug is not None:
        if params.debug == 'print':
            p1.save(os.path.join(params.debug_outdir, 'color_quick_check.png'), verbose=False)
        elif params.debug == 'plot':
            print(p1)


def find_color_card(rgb_img, threshold_type='adaptgauss', threshvalue=125, blurry=False, background='dark',
                    record_chip_size="median", label="default"):
    """Automatically detects a color card and output info to use in create_color_card_mask function

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
    label            = optional label parameter, modifies the variable name of observations recorded (default 'default')

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
            if len(approx) == 4 or len(approx) == 5:
                msquarecoords.append(approx)
            else:  # It's not square
                # msquare.append(0)
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
