# For classifying an image based on a trained kmeans clustering model output from train_kmeans.py

import os
import numpy as np
from joblib import load
from plantcv.learn.train_kmeans import _patch_extract
from plantcv.plantcv import readimage, params, logical_or
from plantcv.plantcv._debug import _debug


def predict_kmeans(img, model_path="./kmeansout.fit", patch_size=10, mode=None):
    """
    Uses a trained, patch-based kmeans clustering model to predict clusters from an input image.
    Inputs:
    img = An image on which to predict clusters
    model_path = Path to directory where the trained model output is stored
    patch_size = Size of the NxN neighborhood around each pixel
    mode = either None (default) for RGB or grayscale images, or "spectral" for multispectral images
    :param img: numpy.ndarray
    :param model_path: str
    :param patch_size: positive non-zero integer
    :param mode: str
    :return labeled: numpy.ndarray
    """
    kmeans = load(model_path)
    if not mode:
        train_img, _, _ = readimage(img)
    elif mode == "spectral":
        spec_obj = readimage(img, mode='envi')
        train_img = spec_obj.array_data

    before = after = int((patch_size - 1)/2)   # odd
    if patch_size % 2 == 0:   # even
        before = int((patch_size-2)/2)
        after = int(patch_size/2)

    # Padding
    if len(train_img.shape) == 2:  # gray
        train_img = np.pad(train_img, pad_width=((before, after), (before, after)), mode="edge")
    elif len(train_img.shape) == 3 and train_img.shape[2] >= 3:  # rgb
        train_img = np.pad(train_img, pad_width=((before, after), (before, after), (0, 0)), mode="edge")

    # Shapes
    mg = np.floor(patch_size / 2).astype(np.int32)
    if len(train_img.shape) == 2:
        h, w = train_img.shape
    elif len(train_img.shape) == 3 and train_img.shape[2] >= 3:
        h, w, _ = train_img.shape

    # Do the prediction
    train_patches = _patch_extract(train_img, patch_size=patch_size)
    train_labels = kmeans.predict(train_patches)
    reshape_params = [[h - 2*mg + 1, w - 2*mg + 1], [h - 2*mg, w - 2*mg]]
    # Takes care of even vs odd numbered patch size reshaping
    labeled = train_labels.reshape(reshape_params[patch_size % 2][0], reshape_params[patch_size % 2][1])
    labeled = labeled.astype("uint8")
    _debug(visual=labeled, filename=os.path.join(params.debug_outdir, "_labeled_img.png"))
    return labeled


def mask_kmeans(labeled_img, k, cat_list=None):
    """
    Uses the predicted clusters from a target image to generate a binary mask.
    Inputs:
    labeled_img = An image with predicted clusters
    K = Number of clusters to fit
    patch_size = Size of the NxN neighborhood around each pixel
    cat_list = A list of the numeric classes for composing a combined mask.
               If empty, function prints all classes as separate masks.
    :param labeled_img: numpy.ndarray
    :param K: positive non-zero integer
    :param patch_size: positive non-zero integer
    :param cat_list: list of positive non-zero integers
    """
    if cat_list is None:
        mask_dict = {}
        L = [*range(k)]
        for i in L:
            mask_light = np.where(labeled_img == i, 255, 0).astype("uint8")
            _debug(visual=mask_light, filename=os.path.join(params.debug_outdir, "_kmeans_mask_"+str(i)+".png"))
            mask_dict[str(i)] = mask_light
        return mask_dict
    # Store debug
    debug = params.debug
    # Change to None so that logical_or does not plot each stepwise addition
    params.debug = None
    for idx, i in enumerate(cat_list):
        if idx == 0:
            mask_light = np.where(labeled_img == i, 255, 0).astype("uint8")
        else:
            mask_light = logical_or(mask_light, np.where(labeled_img == i, 255, 0).astype("uint8"))
    params.debug = debug
    _debug(visual=mask_light, filename=os.path.join(params.debug_outdir, "_kmeans_combined_mask.png"))
    return mask_light
