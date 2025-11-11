import pytest
import os
from plantcv.plantcv.process_results import process_results


def test_process_results(test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory and results file
    tmp_dir = tmpdir.mkdir("sub")
    result_file = tmp_dir.join("appended_results.json")
    config = type("smallconfig", (),
                  {"tmp_dir": test_data.parallel_results_dir,
                   "checkpoint": False,
                   "results": result_file})
    # Run twice to create appended results
    process_results(config, outformat="json")
    process_results(config, outformat="json")
    # Assert that the output JSON file matches the expected output JSON file
    results = test_data.load_json(json_file=result_file)
    expected = test_data.appended_results()
    assert results == expected


def test_process_results_new_output(test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory and results file
    result_file = tmpdir.mkdir("sub").join("new_result.json")
    config = type("smallconfig", (),
                  {"tmp_dir": test_data.parallel_results_dir,
                   "checkpoint": False,
                   "results": result_file})
    process_results(config, outformat="json")

    # Assert output matches expected values
    results = test_data.load_json(json_file=result_file)
    expected = test_data.new_results()
    assert results == expected


def test_process_results_valid_json(test_data):
    """Test for PlantCV."""
    config = type("smallconfig", (),
                  {"tmp_dir": test_data.parallel_results_dir,
                   "checkpoint": "false",
                   "results": test_data.valid_json_file})
    # Test when the file is a valid json file but doesn't contain expected keys
    with pytest.raises(RuntimeError):
        process_results(config, outformat="json")


def test_process_results_invalid_json(tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory and invalid results file
    result_file = tmpdir.mkdir("bad_results").join("invalid.txt")
    result_file.write("Invalid")
    config = type("smallconfig", (),
                  {"tmp_dir": os.path.split(str(result_file))[0],
                   "checkpoint": "false",
                   "results": result_file})
    with pytest.raises(RuntimeError):
        process_results(config, outformat="json")
