import os
from shutil import copyfile
from plantcv.learn import naive_bayes, naive_bayes_multiclass


def test_naive_bayes(learn_test_data, tmpdir):
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    imgdir = os.path.join(tmp_dir, "images")
    maskdir = os.path.join(tmp_dir, "masks")
    # Make image and mask directories in the cache directory
    os.makedirs(imgdir, exist_ok=True)
    os.makedirs(maskdir, exist_ok=True)
    # Copy and image and mask to the image/mask directories
    copyfile(learn_test_data.small_rgb_img, os.path.join(imgdir, "image.png"))
    copyfile(learn_test_data.small_bin_img, os.path.join(maskdir, "image.png"))
    # Run the naive Bayes training module
    outfile = os.path.join(str(tmp_dir), "naive_bayes_pdfs.txt")
    naive_bayes(imgdir=imgdir, maskdir=maskdir, outfile=outfile, mkplots=True)
    assert os.path.exists(outfile)


def test_naive_bayes_multiclass(learn_test_data, tmpdir):
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    # Run the naive Bayes multiclass training module
    outfile = os.path.join(tmp_dir, "naive_bayes_multiclass_pdfs.txt")
    naive_bayes_multiclass(samples_file=learn_test_data.rgb_values_table, outfile=outfile, mkplots=True)
    assert os.path.exists(outfile)
