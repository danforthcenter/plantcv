import pytest
import os
import pandas as pd
from plantcv.utils import tabulate_bayes_classes


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
