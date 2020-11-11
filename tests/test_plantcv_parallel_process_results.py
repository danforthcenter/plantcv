import pytest
import os
import json
from plantcv.parallel import process_results


def test_plantcv_parallel_process_results(test_data, tmpdir):
    # Create a test tmp directory and results file
    result_file = tmpdir.mkdir("sub").join("appended_results.json")
    process_results(job_dir=test_data["parallel_results_dir"], json_file=str(result_file))
    process_results(job_dir=test_data["parallel_results_dir"], json_file=str(result_file))
    # Assert that the output JSON file matches the expected output JSON file
    results = json.load(result_file)
    with open(test_data["appended_results_file"], "r") as fp:
        expected = json.load(fp)
    assert results == expected


def test_plantcv_parallel_process_results_new_output(test_data, tmpdir):
    # Create a test tmp directory and results file
    result_file = tmpdir.mkdir("sub").join("new_result.json")
    process_results(job_dir=test_data["parallel_results_dir"], json_file=str(result_file))
    # Assert output matches expected values
    results = json.load(result_file)
    with open(test_data["new_results_file"], "r") as fp:
        expected = json.load(fp)
    assert results == expected


def test_plantcv_parallel_process_results_valid_json(test_data):
    # Test when the file is a valid json file but doesn't contain expected keys
    with pytest.raises(RuntimeError):
        process_results(job_dir=test_data["parallel_results_dir"], json_file=test_data["valid_json_file"])


def test_plantcv_parallel_process_results_invalid_json(tmpdir):
    # Create a test tmp directory and results file
    result_file = tmpdir.mkdir("bad_results").join("invalid.txt")
    result_file.write("Invalid")
    # Move the test data to the tmp directory
    with pytest.raises(RuntimeError):
        process_results(job_dir=os.path.split(str(result_file))[0], json_file=str(result_file))
