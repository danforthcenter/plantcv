import os
import pytest
from plantcv.utils.cli import main


def test_no_arguments():
    """Test for PlantCV."""
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-utils"]
    with pytest.raises(SystemExit):
        main()


def test_run_json2csv(utils_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-utils", "json2csv",
                "--json", utils_test_data.plantcv_results_file,
                "--csv", os.path.join(str(tmp_dir), "exports")]
    assert main() is None


def test_run_tabulate_bayes_classes(utils_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-utils", "tabulate_bayes_classes",
                "--infile", utils_test_data.rgb_values_file,
                "--outfile", os.path.join(str(tmp_dir), "rgb_table.txt")]
    assert main() is None


def test_run_sample_images(utils_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    # Mock ARGV
    import sys
    sys.argv = ["plantcv-utils", "sample_images",
                "--source", utils_test_data.snapshot_imgdir,
                "--outdir", os.path.join(str(tmp_dir), "sample_images"),
                "--number", "3"]
    assert main() is None
