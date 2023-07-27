import pytest
import os
import json
import numpy as np
from shutil import copyfile
from plantcv.plantcv import Outputs


@pytest.mark.parametrize("datatype,value", [[list, []], [int, 2], [float, 2.2], [bool, True], [str, "2"], [dict, {}],
                                            [tuple, ()], [None, None]])
def test_add_observation(datatype, value):
    """Test for PlantCV."""
    # Create output instance
    outputs = Outputs()
    outputs.add_observation(sample='default', variable='test', trait='test variable', method='type', scale='none',
                            datatype=datatype, value=value, label=[])
    assert outputs.observations["default"]["test"]["value"] == value


def test_add_observation_invalid_type():
    """Test for PlantCV."""
    # Create output instance
    outputs = Outputs()
    with pytest.raises(RuntimeError):
        outputs.add_observation(sample='default', variable='test', trait='test variable', method='type', scale='none',
                                datatype=list, value=np.array([2]), label=[])


def test_save_results_json_newfile(tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    outfile = os.path.join(cache_dir, "results.json")
    # Create output instance
    outputs = Outputs()
    outputs.add_observation(sample='default', variable='test', trait='test variable', method='test', scale='none',
                            datatype=str, value="test", label="none")
    outputs.save_results(filename=outfile, outformat="json", append=False)
    with open(outfile, "r") as fp:
        results = json.load(fp)
        assert results["observations"]["default"]["test"]["value"] == "test"

def test_save_results_json_newfile_append(tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    outfile = os.path.join(cache_dir, "results.json")
    # Create output instance
    outputs = Outputs()
    outputs.add_observation(sample='default', variable='test', trait='test variable', method='test', scale='none',
                            datatype=str, value="test", label="none")
    outputs.save_results(filename=outfile, outformat="json", append=True)
    with open(outfile, "r") as fp:
        results = json.load(fp)
        assert results["observations"]["default"]["test"]["value"] == "test"

def test_save_results_json_existing_file(test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    outfile = os.path.join(cache_dir, os.path.basename(test_data.outputs_results_json))
    copyfile(test_data.outputs_results_json, outfile)
    # Create output instance
    outputs = Outputs()
    outputs.add_observation(sample='default', variable='test', trait='test variable', method='test', scale='none',
                            datatype=str, value="test", label="none")
    outputs.save_results(filename=outfile, outformat="json", append=False)
    with open(outfile, "r") as fp:
        results = json.load(fp)
        assert results["observations"]["default"]["test"]["value"] == "test"

def test_save_results_json_existing_file_append(test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    outfile = os.path.join(cache_dir, os.path.basename(test_data.outputs_results_json))
    copyfile(test_data.outputs_results_json, outfile)
    # Create output instance
    outputs = Outputs()
    outputs.add_observation(sample='default', variable='test', trait='test variable', method='test', scale='none',
                            datatype=str, value="test", label="none")
    outputs.save_results(filename=outfile, outformat="json", append=True)

    outputs2 = Outputs()
    outputs2.add_observation(sample='default', variable='test', trait='test variable', method='test', scale='none',
                            datatype=str, value="this data overwrites the original value for this", label="none")
    outputs2.add_observation(sample='newdatas', variable='test', trait='test variable', method='test', scale='none',
                            datatype=str, value="some data here", label="none")
    outputs2.save_results(filename=outfile, outformat="json", append=True)

    with open(outfile, "r") as fp:
        results = json.load(fp)
        assert results["observations"]["default"]["test"]["value"] == "this data overwrites the original value for this"
        assert results["observations"]["newdatas"]["test"]["value"] == "some data here"

def test_save_results_csv(test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    outfile = tmpdir.mkdir("cache").join("results.csv")
    # Create output instance
    outputs = Outputs()
    outputs.add_observation(sample='default', variable='string', trait='string variable', method='string', scale='none',
                            datatype=str, value="string", label="none")
    outputs.add_observation(sample='default', variable='boolean', trait='boolean variable', method='boolean',
                            scale='none', datatype=bool, value=True, label="none")
    outputs.add_observation(sample='default', variable='list', trait='list variable', method='list',
                            scale='none', datatype=list, value=[1, 2, 3], label=[1, 2, 3])
    outputs.save_results(filename=outfile, outformat="csv", append=True)

    outputs2 = Outputs()
    outputs2.add_observation(sample='default', variable='tuple', trait='tuple variable', method='tuple',
                            scale='none', datatype=tuple, value=(1, 2), label=(1, 2))
    outputs2.add_observation(sample='default', variable='tuple_list', trait='list of tuples variable',
                            method='tuple_list', scale='none', datatype=list, value=[(1, 2), (3, 4)], label=[1, 2])
    outputs2.save_results(filename=outfile, outformat="csv", append=True)

    with open(outfile, "r") as fp:
        results = fp.read()
    with open(test_data.outputs_results_csv, "r") as fp:
        test_results = fp.read()
    assert results == test_results


def test_save_results_invalid_outformat():
    """Test for PlantCV."""
    # Create output instance
    outputs = Outputs()
    with pytest.raises(ValueError):
        outputs.save_results(filename="filename does not matter for this test", outformat="INVALIDOUTFORMAT")


def test_clear_outputs():
    """Test for PlantCV."""
    # Create output instance
    outputs = Outputs()
    outputs.add_observation(sample='default', variable='test', trait='test variable', method='test', scale='none',
                            datatype=str, value="test", label="none")
    outputs.clear()
    assert outputs.observations == {}
