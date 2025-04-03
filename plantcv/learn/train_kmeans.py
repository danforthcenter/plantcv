# training a patch-based kmeans clustering model on a set of images

import os
import numpy as np
import cv2
import random
from plantcv.plantcv import readimage, params
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction import image
from skimage.filters import gaussian
from joblib import dump


def train_kmeans(img_dir, k, out_path="./kmeansout.fit", prefix="", patch_size=10, mode=None,
                 sigma=5, sampling=None, seed=1, num_imgs=0, n_init=10):
    """
    Trains a patch-based kmeans clustering model for identifying image features.
    Inputs:
    img_idr = Path to directory where training images are stored
    K = Number of clusters to fit
    out_path = Path to directory where the model output should be stored
    prefix = Keyword for target images. Anything in img_dir without the prefix will be skipped
    patch_size = Size of the NxN neighborhood around each pixel
    mode = Either None (default) denoting an RGB or grayscale image, or "spectral" for multispectral images
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
    :param mode: str
    :param sigma: positive real number or sequence of positive real numbers
    :param sampling: float (0,1]
    :param seed: positive integer
    :param num_imgs: positive non-zero integer
    :param n_init: positive non-zero integer
    :return fitted: sklearn.cluster._kmeans.MiniBatchKMeans
    """
    # Establish training set
    exts = ["jpg", "png", "jpeg", "JPG", "PNG"]
    file_names = []
    for i in sorted(os.listdir(img_dir)):
        if not mode:
            if i.split(".")[-1] in exts:
                file_names.append(i)
        elif mode == "spectral":
            if i.endswith(".raw"):
                file_names.append(i)
    if num_imgs == 0:
        training_files = file_names
    else:
        training_files = random.choices(file_names, k=num_imgs)  # choosing a set of random files
    # Read and extract patches
    for idx, img_name in enumerate(training_files):
        if prefix in img_name:
            if not mode:
                img = cv2.imread(os.path.join(img_dir, img_name), -1)
            elif mode == "spectral":
                debug = params.debug
                params.debug = None
                spec_obj = readimage(filename=os.path.join(img_dir, img_name), mode='envi')
                img = spec_obj.array_data
                params.debug = debug
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


def _patch_extract(img, patch_size=10, sigma=5, sampling=None, seed=1):
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
    if len(img.shape) == 2:
        img_blur = np.round(gaussian(img, sigma=sigma)*255).astype(np.uint16)
    elif len(img.shape) == 3 and img.shape[2] >= 3:
        img_blur = np.round(gaussian(img, sigma=sigma, channel_axis=2)*255).astype(np.uint16)

    # Extract patches
    patches = image.extract_patches_2d(img_blur, (patch_size, patch_size),
                                       max_patches=sampling, random_state=seed)
    N = patches.shape[0]
    patches_lin = patches.reshape(N, -1)
    return patches_lin
