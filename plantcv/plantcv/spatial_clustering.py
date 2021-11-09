# Segment objects into spatial based clusters within an image

import os
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.cluster import OPTICS
from sklearn.preprocessing import StandardScaler
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import color_palette


def spatial_clustering(mask, algorithm="DBSCAN", min_cluster_size=5, max_distance=None):
    """
    Counts and segments portions of an image based on distance between two pixels.
    Masks showing all clusters, plus masks of individual clusters, are returned.

    Inputs:
    mask             = Mask/binary image to segment into clusters.
    algorithm        = Algorithm to use for segregating different clusters.
                       Currently supporting OPTICS and DBSCAN. (Default="DBSCAN")
    min_cluster_size = The minimum size a section of a mask must be (in pixels)
                       before it can be considered its own cluster. (Default=5)
    max_distance     = The total distance between two pixels for them to be considered a part
                       of the same cluster.  For the DBSCAN algorithm, value must be between
                       0 and 1.  For OPTICS, the value is in pixels and depends on the size
                       of your picture.  (Default=0)

    Returns:
    clust_img        = Output image with each cluster draw with a unique color.
    clust_masks      = List of binary masks, one per cluster.

    :param mask: numpy.ndarray
    :param algorithm: str
    :param min_cluster_size: int
    :param max_distance: float
    :return clust_img: numpy.ndarray
    :return clust_masks: list
    """

    # Uppercase algorithm name
    al_upper = algorithm.upper()

    # Dictionary of default values per algorithm
    default_max_dist = {"DBSCAN": 0.2, "OPTICS": np.inf}

    # If the algorithm is not in the default_max_dist dictionary raise a NameError
    if al_upper not in default_max_dist:
        raise NameError("Please use only 'OPTICS' or 'DBSCAN' ")

    # If max_distance is not set, apply the default value
    if max_distance is None:
        max_distance = default_max_dist.get(al_upper)

    # Get all x, y coordinates of white pixels in the mask
    x, y = np.where(mask == 255)
    zipped = np.column_stack((x, y))

    if "OPTICS" in al_upper:
        scaled = StandardScaler(with_mean=False, with_std=False).fit_transform(zipped)
        db = OPTICS(max_eps=max_distance, min_samples=min_cluster_size, n_jobs=-1).fit(scaled)
    elif "DBSCAN" in al_upper:
        scaled = StandardScaler().fit_transform(zipped)
        db = DBSCAN(eps=max_distance, min_samples=min_cluster_size, n_jobs=-1).fit(scaled)

    # Number of clusters
    n_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
    # Create a color palette of n_clusters colors
    colors = color_palette(n_clusters + 1)
    # Initialize variables
    dict_of_colors = {}
    clust_masks = []
    h, w = mask.shape
    # Colorized clusters image
    clust_img = np.zeros((h, w, 3), np.uint8)
    # Index the label color for each cluster
    for y in range(0, n_clusters):
        dict_of_colors[str(y)] = colors[y]
        clust_masks.append(np.zeros((h, w), np.uint8))

    # Group -1 are points not assigned to a cluster
    dict_of_colors["-1"] = (255, 255, 255)

    # Loop over labels/clusters
    for z in range(0, len(db.labels_)):
        if not db.labels_[z] == -1:
            # Create a binary mask for each cluster
            clust_masks[db.labels_[z]][zipped[z][0], zipped[z][1]] = 255

        # Add a cluster with a unique label color to the cluster image
        clust_img[zipped[z][0], zipped[z][1]] = (dict_of_colors[str(db.labels_[z])][2],
                                                 dict_of_colors[str(db.labels_[z])][1],
                                                 dict_of_colors[str(db.labels_[z])][0])

    _debug(visual=clust_img,
           filename=os.path.join(params.debug_outdir, f"{params.device}_{al_upper}_clusters.png"))

    return clust_img, clust_masks
