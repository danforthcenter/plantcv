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
    # Load example ouputs and test equality
    f = open(training_dir+"/kmeansout_subset.fit", "rb")
    test_subset = load(f)
    assert fit_subset == test_subset
    f.close()
    
    f = open(training_dir+"/kmeansout_full.fit", "rb")
    test_full = load(f)
    assert fit_full == test_full
    f.close()