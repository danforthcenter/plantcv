import pytest
import os
from plantcv.parallel import process_results


def test_process_results(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory and results file
    result_file = tmpdir.mkdir("sub").join("appended_results.json")
    # Run twice to create appended results
    process_results(job_dir=parallel_test_data.parallel_results_dir, json_file=result_file)
    process_results(job_dir=parallel_test_data.parallel_results_dir, json_file=result_file)
    # Assert that the output JSON file matches the expected output JSON file
    results = parallel_test_data.load_json(json_file=result_file)
    expected = parallel_test_data.appended_results()
    assert results == expected


def test_process_results_new_output(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory and results file
    result_file = tmpdir.mkdir("sub").join("new_result.json")
    process_results(job_dir=parallel_test_data.parallel_results_dir, json_file=result_file)
    # Assert output matches expected values
    results = parallel_test_data.new_results()
    expected = parallel_test_data.load_json(json_file=result_file)
    assert results == expected


def test_process_results_valid_json(parallel_test_data):
    """Test for PlantCV."""
    # Test when the file is a valid json file but doesn't contain expected keys
    with pytest.raises(RuntimeError):
        process_results(job_dir=parallel_test_data.parallel_results_dir, json_file=parallel_test_data.valid_json_file)


def test_process_results_invalid_json(tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory and invalid results file
    result_file = tmpdir.mkdir("bad_results").join("invalid.txt")
    result_file.write("Invalid")
    with pytest.raises(RuntimeError):
        process_results(job_dir=os.path.split(str(result_file))[0], json_file=result_file)
