import cv2

def get_centroids(bin_img):
    """ Get the coordinates (row,column) of the centroid of each connected
    region in a binary image.

    Inputs:
    bin_img       = Binary image containing the connected regions to consider


    Returns:
    coor  = List of coordinates (row,column) of the centroids of the regions

    :param bin_img: numpy.ndarray
    :return coor: list
    """

    # find contours in the binary image
    _, contours, _ = cv2.findContours(bin_img, cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)
    coor = []
    for c in contours:
        # calculate moments for each contour
        M = cv2.moments(c)
        # calculate row,col coordinates of centroid
        col = int(M["m10"] / M["m00"])
        row = int(M["m01"] / M["m00"])
        coor.append([row,col])

    return coor
