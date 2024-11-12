import os
from plantcv.learn.train_kmeans import train_kmeans


def test_train_kmeans(learn_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    training_dir = learn_test_data.kmeans_train_dir
    training_dir_gray = learn_test_data.kmeans_train_gray_dir
    outfile_subset = os.path.join(str(cache_dir), "kmeansout_subset.fit")
    outfile_full = os.path.join(str(cache_dir), "kmeansout_full.fit")
    outfile_subset_gray = os.path.join(str(cache_dir), "kmeansout_subset_gray.fit")
    outfile_full_gray = os.path.join(str(cache_dir), "kmeansout_full_gray.fit")
    # Train full model and partial model
    train_kmeans(img_dir=training_dir, prefix="kmeans_train",
                 out_path=outfile_subset, k=5, patch_size=4, num_imgs=3)
    train_kmeans(img_dir=training_dir, prefix="kmeans_train",
                 out_path=outfile_full, k=5, patch_size=4)
    train_kmeans(img_dir=training_dir_gray, prefix="kmeans_train",
                 out_path=outfile_subset_gray, k=5, patch_size=4, num_imgs=3)
    train_kmeans(img_dir=training_dir_gray, prefix="kmeans_train",
                 out_path=outfile_full_gray, k=5, patch_size=4)
    assert os.path.exists(outfile_subset)
    assert os.path.exists(outfile_full)
    assert os.path.exists(outfile_subset_gray)
    assert os.path.exists(outfile_full_gray)
