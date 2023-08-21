import pytest
import os
from plantcv.utils import json2csv


def test_json2csv(utils_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    json2csv(json_file=utils_test_data.plantcv_results_file, csv_prefix=os.path.join(str(tmp_dir), "exports"))
    assert os.path.exists(os.path.join(str(tmp_dir), "exports-single-value-traits.csv"))


def test_json2csv_no_json(utils_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    with pytest.raises(IOError):
        json2csv(json_file=os.path.join(utils_test_data.datadir, "not_a_file.json"),
                 csv_prefix=os.path.join(str(tmp_dir), "exports"))


def test_json2csv_bad_json(utils_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    with pytest.raises(ValueError):
        json2csv(json_file=utils_test_data.invalid_results_file, csv_prefix=os.path.join(str(tmp_dir), "exports"))
