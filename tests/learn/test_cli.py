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


def test_run_naive_bayes_bad_maskdir(nb_train_dirs):
    """Test for PlantCV."""
    # Define input and output files
    imgdir, _ = nb_train_dirs
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-train", "naive_bayes",
                "--imgdir", imgdir,
                "--maskdir", "does-not-exist",
                "--outfile", "does-not-exist",
                "--plots"]
    with pytest.raises(IOError):
        main()


def test_run_naive_bayes(tmpdir, nb_train_dirs):
    """Test for PlantCV."""
    # Temp directory
    tmp_dir = tmpdir.mkdir("sub")
    # Define input and output files
    imgdir, maskdir = nb_train_dirs
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


def test_run_tabulate_bayes_classes(learn_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-train", "tabulate_bayes_classes",
                "--file", learn_test_data.rgb_values_file,
                "--outfile", os.path.join(str(tmp_dir), "rgb_table.txt")]
    assert main() is None


def test_run_tabulate_bayes_classes_bad_file(tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-train", "tabulate_bayes_classes",
                "--file", "thisfiledoesnotexist.txt",
                "--outfile", os.path.join(str(tmp_dir), "rgb_table.txt")]
    with pytest.raises(IOError):
        main()


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


def test_run_kmeans_bad_imgdir():
    """Test for PlantCV."""
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-train", "kmeans",
                "--imgdir", "does-not-exist",
                "--categories", "3",
                "--out", "does-not-exist"]
    with pytest.raises(IOError):
        main()


def test_run_kmeans(tmpdir, kmeans_train_dir):
    """Test for PlantCV."""
    # Temp directory
    tmp_dir = tmpdir.mkdir("sub")
    # Define input and output files
    imgdir, _ = kmeans_train_dir
    outfile = os.path.join(str(tmp_dir), "kmeans.fit")
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-train", "kmeans",
                "--imgdir", imgdir,
                "--categories", "3",
                "--out", outfile]
    assert main() is None
