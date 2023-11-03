"""Find color card module."""
import cv2
import numpy as np
from plantcv.plantcv import params, outputs, deprecation_warning, fatal_error


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
    deprecation_warning(
        "This function is deprecated and will be removed in PlantCV v5.0. "
        "Please use plantcv.transform.detect_color_card instead."
        )
    # Imports
    import skimage
    import pandas as pd
    from scipy.spatial.distance import squareform, pdist

    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    # Get image attributes
    height, width, _ = rgb_img.shape
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
        _, threshold = cv2.threshold(gaussian, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif threshold_type.upper() == "NORMAL":
        # Blur slightly so defects on card squares and background patterns are less likely to be picked up
        gaussian = cv2.GaussianBlur(gray_img, (5, 5), 0)
        _, threshold = cv2.threshold(gaussian, threshvalue, 255, cv2.THRESH_BINARY)
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
            _, wh, _ = cv2.minAreaRect(c)  # Rotated rectangle
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
