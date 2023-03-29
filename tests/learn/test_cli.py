import os
import pytest
from plantcv.learn.cli import main


def test_no_arguments():
    """Test for PlantCV."""
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-train"]
    with pytest.raises(SystemExit):
        main()


def test_run_naive_bayes_bad_imgdir():
    """Test for PlantCV."""
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-train", "naive_bayes",
                "--imgdir", "does-not-exist",
                "--maskdir", "does-not-exist",
                "--outfile", "does-not-exist",
                "--plots"]
    with pytest.raises(IOError):
        main()


def test_run_naive_bayes_bad_maskdir(learn_test_data):
    """Test for PlantCV."""
    # Define input and output files
    imgdir = os.path.join(learn_test_data.train_data, "images")
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-train", "naive_bayes",
                "--imgdir", imgdir,
                "--maskdir", "does-not-exist",
                "--outfile", "does-not-exist",
                "--plots"]
    with pytest.raises(IOError):
        main()


def test_run_naive_bayes(tmpdir, learn_test_data):
    """Test for PlantCV."""
    # Temp directory
    tmp_dir = tmpdir.mkdir("sub")
    # Define input and output files
    imgdir = os.path.join(learn_test_data.train_data, "images")
    maskdir = os.path.join(learn_test_data.train_data, "masks")
    outfile = os.path.join(str(tmp_dir), "naive_bayes_pdfs.txt")
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-train", "naive_bayes",
                "--imgdir", imgdir,
                "--maskdir", maskdir,
                "--outfile", outfile,
                "--plots"]
    assert main() is None


def test_run_naive_bayes_multiclass(tmpdir, learn_test_data):
    """Test for PlantCV."""
    # Temp directory
    tmp_dir = tmpdir.mkdir("sub")
    # Define input and output files
    outfile = os.path.join(str(tmp_dir), "naive_bayes_multiclass_pdfs.txt")
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-train", "naive_bayes_multiclass",
                "--file", learn_test_data.rgb_values_table,
                "--outfile", outfile,
                "--plots"]
    assert main() is None


def test_run_naive_bayes_multiclass_bad_file():
    """Test for PlantCV."""
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-train", "naive_bayes_multiclass",
                "--file", "does-not-exist",
                "--outfile", "does-not-exist",
                "--plots"]
    with pytest.raises(IOError):
        main()
