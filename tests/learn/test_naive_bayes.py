import os
import pytest
import pandas as pd
from plantcv.learn import naive_bayes, naive_bayes_multiclass, tabulate_bayes_classes, check_samples_file


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


def test_tabulate_bayes_classes(learn_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    outfile = os.path.join(str(tmp_dir), "rgb_table.txt")
    tabulate_bayes_classes(input_file=learn_test_data.rgb_values_file, output_file=outfile)
    table = pd.read_csv(outfile, sep="\t")
    assert table.shape == (228, 2)


def test_tabulate_bayes_classes_missing_input(tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    outfile = os.path.join(str(tmp_dir), "rgb_table.txt")
    with pytest.raises(IOError):
        tabulate_bayes_classes(input_file="pixel_inspector_rgb_values.txt", output_file=outfile)


def test_naive_bayes_multiclass_bad_input(learn_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    outfile = os.path.join(tmp_dir, "naive_bayes_multiclass_pdfs.txt")
    # A samples file with formatting problems should abort training instead of failing deep in parsing
    with pytest.raises(RuntimeError):
        naive_bayes_multiclass(samples_file=learn_test_data.rgb_values_table_bad, outfile=outfile)
    assert not os.path.exists(outfile)


def test_check_samples_file_valid(learn_test_data):
    """Test for PlantCV."""
    assert check_samples_file(learn_test_data.rgb_values_table) is True


def test_check_samples_file_bad(learn_test_data):
    """Test for PlantCV."""
    assert check_samples_file(learn_test_data.rgb_values_table_bad) is False


def test_check_samples_file_reports_every_category(learn_test_data, capsys):
    """Test for PlantCV."""
    check_samples_file(learn_test_data.rgb_values_table_bad)
    output = capsys.readouterr().out
    # One header duplicate label, one empty header label, one wrong column count row, three invalid RGB
    # values, and one class with zero valid samples are baked into the fixture file
    assert "Header problems" in output
    assert "class label 'class1' is used in both column 1 and column 2" in output
    assert "class label is empty" in output
    assert "Wrong column count" in output
    assert "Line 7: row has 3 column(s) but the header defines 4 class(es)" in output
    assert "Invalid RGB values" in output
    assert "Classes with no samples" in output
    assert "Class 'class2' has zero valid sampled pixels" in output


def test_check_samples_file_caps_errors_per_category(tmpdir):
    """Test for PlantCV."""
    # A samples file where every row has the same problem (25 out-of-range red values) should not flood the
    # output past max_errors, but the total count should still be accurate
    samples_file = os.path.join(tmpdir, "many_bad_rows.txt")
    with open(samples_file, "w") as f:
        f.write("classA\tclassB\n")
        for i in range(25):
            f.write(f"999,{i},{i}\t1,2,3\n")
    assert check_samples_file(samples_file, max_errors=5) is False


def test_check_samples_file_caps_errors_per_category_output(tmpdir, capsys):
    """Test for PlantCV."""
    samples_file = os.path.join(tmpdir, "many_bad_rows.txt")
    with open(samples_file, "w") as f:
        f.write("classA\tclassB\n")
        for i in range(25):
            f.write(f"999,{i},{i}\t1,2,3\n")
    check_samples_file(samples_file, max_errors=5)
    output = capsys.readouterr().out
    assert "Invalid RGB values (5 of 25 shown)" in output
    assert "...and 20 more." in output


def test_check_samples_file_delimiter_heuristic(tmpdir):
    """Test for PlantCV."""
    # A header with only 1 column is a strong sign the file isn't tab-delimited at all
    samples_file = os.path.join(tmpdir, "wrong_delimiter.txt")
    with open(samples_file, "w") as f:
        f.write("classA,classB\n1,2,3;4,5,6\n")
    assert check_samples_file(samples_file) is False
