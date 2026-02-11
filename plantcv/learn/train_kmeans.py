# training a patch-based kmeans clustering model on a set of images

import os
import numpy as np
import cv2
import random
from plantcv.plantcv._globals import params
from plantcv.plantcv.readimage import readimage
from plantcv.learn.patch_extract import _patch_extract
from sklearn.cluster import MiniBatchKMeans
from joblib import dump


def train_kmeans(img_dir, k, out_path="./kmeansout.fit", prefix="", patch_size=10, mode=None,
                 sigma=5, sampling=None, seed=1, num_imgs=0, n_init=10):
    """Trains a patch-based kmeans clustering model for identifying image features.
    Parameters
    ----------
    img_idr = str, Path to directory where training images are stored
    K = int, Number of clusters to fit (>0)
    out_path = str, Path to directory where the model output should be stored
    prefix = str, Keyword for target images. Anything in img_dir without the prefix will be skipped
    patch_size = int, Size of the NxN neighborhood around each pixel (>0)
    mode = str, Either None (default) denoting an RGB or grayscale image, or "spectral" for multispectral images
    sigma = numeric, Gaussian blur sigma. Denotes severity of gaussian blur performed before patch identification
    sampling = float (0,1], Fraction of image from which patches are identified
    seed = int, Seed for determinism of random elements like sampling of patches
    num_imgs = int, Number of images to use for training. Default is all of them in img_dir with prefix
    n_init = int, Number of random initiations tried by MiniBatchKMeans. The algorithm is run on the best one

    Returns
    -------
    fitted = sklearn.cluster._kmeans.MiniBatchKMeans object
    """
    # Establish training set
    exts = ["jpg", "png", "jpeg", "JPG", "PNG"]
    file_names = []
    for i in sorted(os.listdir(img_dir)):
        if not mode:
            if i.split(".")[-1] in exts:
                file_names.append(i)
        elif mode.upper() == "SPECTRAL":
            if i.endswith(".raw"):
                file_names.append(i)
    if num_imgs == 0:
        training_files = file_names
    else:
        training_files = random.choices(file_names, k=num_imgs)  # choosing a set of random files
    # Read and extract patches
    for idx, img_name in enumerate(training_files):
        if prefix in img_name:
            img = _read_by_mode(os.path.join(img_dir, img_name), mode)
            if idx == 0:
                # Getting info from first image
                patches = _patch_extract(img, patch_size=patch_size, sigma=sigma, sampling=sampling)
            else:
                # Concatenating each additional image
                patches = np.vstack((patches, _patch_extract(img, patch_size=patch_size, sigma=sigma, sampling=sampling)))

    kmeans = MiniBatchKMeans(n_clusters=k, n_init=n_init, random_state=seed)
    fitted = kmeans.fit(patches)
    dump(fitted, out_path)
    return fitted


def _read_by_mode(path, mode):
    """Helper function to reduce complexity in training K-means

    Parameters
    ----------
    path: str,
        path to image file
    mode: str,
        K-means mode, either None or "spectral"

    Returns
    -------
    img: numpy.ndarray
        Image to use in training
    """
    if not mode:
        img = cv2.imread(path, -1)
    elif mode.upper() == "SPECTRAL":
        debug = params.debug
        params.debug = None
        spec_obj = readimage(filename=path, mode='envi')
        img = spec_obj.array_data
        params.debug = debug
    return img
