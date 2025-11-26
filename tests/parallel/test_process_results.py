import pytest
import os
from plantcv.parallel import process_results


def test_process_results(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory and results file
    tmp_dir = tmpdir.mkdir("sub")
    result_file = tmp_dir.join("appended_results.json")
    config = type("smallconfig", (),
                  {"tmp_dir": parallel_test_data.parallel_results_dir,
                   "checkpoint": False,
                   "json": result_file})
    # Run twice to create appended results
    process_results(config)
    process_results(config)
    # Assert that the output JSON file matches the expected output JSON file
    results = parallel_test_data.load_json(json_file=result_file)
    expected = parallel_test_data.appended_results()
    assert results == expected


def test_process_results_new_output(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory and results file
    result_file = tmpdir.mkdir("sub").join("new_result.json")
    config = type("smallconfig", (),
                  {"tmp_dir": parallel_test_data.parallel_results_dir,
                   "checkpoint": False,
                   "json": result_file})
    process_results(config)

    # Assert output matches expected values
    results = parallel_test_data.load_json(json_file=result_file)
    expected = parallel_test_data.new_results()
    assert results == expected


def test_process_results_valid_json(parallel_test_data):
    """Test for PlantCV."""
    config = type("smallconfig", (),
                  {"tmp_dir": parallel_test_data.parallel_results_dir,
                   "checkpoint": "false",
                   "json": parallel_test_data.valid_json_file})
    # Test when the file is a valid json file but doesn't contain expected keys
    with pytest.raises(RuntimeError):
        process_results(config)


def test_process_results_invalid_json(tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory and invalid results file
    result_file = tmpdir.mkdir("bad_results").join("invalid.txt")
    result_file.write("Invalid")
    config = type("smallconfig", (),
                  {"tmp_dir": os.path.split(str(result_file))[0],
                   "checkpoint": "false",
                   "json": result_file})
    with pytest.raises(RuntimeError):
        process_results(config)
