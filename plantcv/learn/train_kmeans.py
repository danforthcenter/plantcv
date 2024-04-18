# training a patch-based kmeans clustering model on a set of images

import os
import numpy as np
import cv2
import random
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction import image
from skimage.filters import gaussian
from joblib import dump


def train_kmeans(img_dir, k, out_path="./kmeansout.fit", prefix="", patch_size=10, sigma=5, sampling=None,
                 seed=1, num_imgs=0, n_init=10):
    """
    Trains a patch-based kmeans clustering model for identifying image features.
    Inputs:
    img_idr = Path to directory where training images are stored
    K = Number of clusters to fit
    out_path = Path to directory where the model output should be stored
    prefix = Keyword for target images. Anything in img_dir without the prefix will be skipped
    patch_size = Size of the NxN neighborhood around each pixel
    sigma = Gaussian blur sigma. Denotes severity of gaussian blur performed before patch identification
    sampling = Fraction of image from which patches are identified
    seed = Seed for determinism of random elements like sampling of patches
    num_imgs = Number of images to use for training. Default is all of them in img_dir with prefix
    n_init = Number of random initiations tried by MiniBatchKMeans. The algorithm is run on the best one
    :param img_dir: str
    :param K: positive non-zero integer
    :param out_path: str
    :param prefix: str
    :param patch_size: positive non-zero integer
    :param sigma: positive real number or sequence of positive real numbers
    :param sampling: float (0,1]
    :param seed: positive integer
    :param num_imgs: positive non-zero integer
    :param n_init: positive non-zero integer
    :return fitted: sklearn.cluster._kmeans.MiniBatchKMeans
    """
    # Establish training set
    file_names = sorted(os.listdir(img_dir))
    if num_imgs == 0:
        training_files = file_names
    else:
        training_files = random.choices(file_names, k=num_imgs)  # choosing a set of random files
    # Read and extract patches
    i = 0
    for img_name in training_files:
        if prefix in img_name:
            img = cv2.imread(os.path.join(img_dir, img_name))
            if i == 0:
                # Getting info from first image
                patches = patch_extract(img, patch_size=patch_size, sigma=sigma, sampling=sampling)
            else:
                # Concatenating each additional image
                patches = np.vstack((patches, patch_extract(img, patch_size=patch_size, sigma=sigma, sampling=sampling)))
            i += 1

    kmeans = MiniBatchKMeans(n_clusters=k, n_init=n_init, random_state=seed)
    fitted = kmeans.fit(patches)
    dump(fitted, out_path)
    return fitted


def patch_extract(img, patch_size=10, sigma=5, sampling=None, seed=1):
    """
    Extracts patches from an image.
    Inputs:
    img = An image from which to extract patches
    patch_size = Size of the NxN neighborhood around each pixel
    sigma = sigma = Gaussian blur sigma. Denotes severity of gaussian blur performed before patch identification
    sampling = Fraction of image from which patches are identified
    seed = Seed for determinism of random elements like sampling of patches
    :param img: numpy.ndarray
    :param patch_size: positive non-zero integer
    :param sigma: positive real number or sequence of positive real numbers
    :param sampling: float (0,1]
    :param seed: positive integer
    :return patches_lin: numpy.ndarray
    """
    # Gaussian blur
    img_blur = np.round(gaussian(img, sigma=sigma, channel_axis=2)*255).astype(np.uint16)
    # Extract patches
    patches = image.extract_patches_2d(img_blur, (patch_size, patch_size),
                                       max_patches=sampling, random_state=seed)
    N = patches.shape[0]
    patches_lin = patches.reshape(N, -1)
    return patches_lin
