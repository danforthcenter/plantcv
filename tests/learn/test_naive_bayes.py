import os
import pytest
import pandas as pd
from plantcv.learn import naive_bayes, naive_bayes_multiclass, tabulate_bayes_classes


def test_naive_bayes(learn_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    imgdir = os.path.join(learn_test_data.train_data, "images")
    maskdir = os.path.join(learn_test_data.train_data, "masks")
    # Run the naive Bayes training module
    outfile = os.path.join(str(tmp_dir), "naive_bayes_pdfs.txt")
    naive_bayes(imgdir=imgdir, maskdir=maskdir, outfile=outfile, mkplots=True)
    assert os.path.exists(outfile)


def test_naive_bayes_multiclass(learn_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    # Run the naive Bayes multiclass training module
    outfile = os.path.join(tmp_dir, "naive_bayes_multiclass_pdfs.txt")
    naive_bayes_multiclass(samples_file=learn_test_data.rgb_values_table, outfile=outfile, mkplots=True)
    assert os.path.exists(outfile)


def test_tabulate_bayes_classes(utils_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    outfile = os.path.join(str(tmp_dir), "rgb_table.txt")
    tabulate_bayes_classes(input_file=utils_test_data.rgb_values_file, output_file=outfile)
    table = pd.read_csv(outfile, sep="\t")
    assert table.shape == (228, 2)


def test_tabulate_bayes_classes_missing_input(tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    outfile = os.path.join(str(tmp_dir), "rgb_table.txt")
    with pytest.raises(IOError):
        tabulate_bayes_classes(input_file="pixel_inspector_rgb_values.txt", output_file=outfile)
