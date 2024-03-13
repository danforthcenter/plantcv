import numpy as np
import cv2
import os
from joblib import load
from plantcv.learn.train_kmeans import train_kmeans, patch_extract


def test_train_kmeans(learn_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    training_dir = learn_test_data.kmeans_train_dir
    # Train full model and partial model 
    fit_subset = train_kmeans(img_dir=training_dir, prefix="image", 
                              out_path=cache_dir+"/kmeansout_subset.fit", K=5, num_imgs=5)
    fit_full = train_kmeans(img_dir=training_dir, prefix="image", 
                            out_path=cache_dir+"/kmeansout_full.fit", K=5)
    # Load example ouputs
    test_subset = load(training_dir+"kmeansout_subset.fit")
    test_full = load(training_dir+"kmeansout_full.fit")
    # Test equality
    assert fit_subset == test_subset
    assert fit_full == test_full