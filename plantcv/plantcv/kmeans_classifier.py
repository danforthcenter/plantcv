#For classifying an image based on a trained kmeans clustering model output from train_kmeans.py

import os
import numpy as np
import cv2
import plantcv.plantcv as pcv
from skimage.filters import gaussian
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction import image
from joblib import load
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plantcv.learn import patch_extract


def predict_kmeans(img, model_path="./kmeansout.fit", patch_size=10):
    """
    Uses a trained, patch-based kmeans clustering model to predict clusters from an input image.
    Inputs:
    img = An image on which to predict clusters 
    model_path = Path to directory where the trained model output is stored
    patch_size = Size of the NxN neighborhood around each pixel
    :param img: numpy.ndarray
    :param model_path: str
    :param patch_size: positive non-zero integer
    :return labeled: numpy.ndarray
    """
    kmeans = load(model_path)
    train_img, _, _ = pcv.readimage(img)
    
    #Shapes 
    mg = np.floor(patch_size / 2).astype(np.int32)
    h, w,_ = train_img.shape

    #Do the prediction
    train_patches = patch_extract(train_img,patch_size=patch_size)
    train_labels = kmeans.predict(train_patches)
    if patch_size%2 == 0:  #even
        labeled = train_labels.reshape(h - 2*mg + 1, w - 2*mg + 1)
    else:
        labeled = train_labels.reshape(h - 2*mg, w - 2*mg)
    _debug(visual=labeled, filename=os.path.join(params.debug_outdir, "_labeled_img.png"))
    return labeled


def mask_kmeans(labeled_img, K, patch_size, cat_list=[]):
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
    mg = np.floor(patch_size / 2).astype(np.int32)
    h, w = labeled_img.shape
    if len(cat_list) == 0:
        L = [*range(K)]        
        for i in L:
            mask = np.ones(labeled_img.shape)
            mask = np.logical_and(mask,labeled_img != i)
            mask[:, 0:mg] = False
            mask[:, w-mg:w] = False
            mask[0:mg, :] = False
            mask[h-mg:h, :] = False
            pcv.plot_image(mask)
    else: 
        mask = np.ones(labeled_img.shape)
        for label in cat_list:
            mask = np.logical_and(mask,labeled_img != label)
        mask[:, 0:mg] = False
        mask[:, w-mg:w] = False
        mask[0:mg, :] = False
        mask[h-mg:h, :] = False 
        pcv.plot_image(mask)
