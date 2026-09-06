import pytest
import os
from plantcv.utils import json2csv


def test_json2csv(utils_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    json2csv(json_file=utils_test_data.plantcv_results_file, csv_prefix=os.path.join(str(tmp_dir), "exports"))
    assert os.path.exists(os.path.join(str(tmp_dir), "exports-single-value-traits.csv"))


def test_json2csv_json_prefix(utils_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    # Pass a csv_prefix that still carries the .json extension, as happens when
    # plantcv-run-workflow reuses the JSON results filename as the CSV prefix
    csv_prefix = os.path.join(str(tmp_dir), "exports.json")
    json2csv(json_file=utils_test_data.plantcv_results_file, csv_prefix=csv_prefix)
    # The .json extension should be stripped, not embedded in the CSV filename
    assert os.path.exists(os.path.join(str(tmp_dir), "exports-single-value-traits.csv"))
    assert not os.path.exists(os.path.join(str(tmp_dir), "exports.json-single-value-traits.csv"))


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
