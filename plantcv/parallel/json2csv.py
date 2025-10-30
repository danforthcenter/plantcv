import os
import json
import itertools
import pandas as pd
import numpy as np


def json2csv(json_file, csv_prefix):
    """Convert a PlantCV JSON file to a CSV files.

    Parameters
    ----------
    json_file : str
        JSON file output by plantcv-run-workflow.
    csv_prefix : str
        CSV output files prefix.

    Raises
    ------
    IOError
        JSON file does not exist.
    ValueError
        JSON file is not in the expected format.
    """
    if not os.path.exists(json_file):
        # If the file does not exist raise an error
        raise IOError(f"File does not exist: {json_file}")
    # Open the JSON file for reading
    with open(json_file, "r") as fp:
        data = json.load(fp)
    # If the data is JSON but it does not have the components we expect from PlantCV raise an error
    if "variables" not in data or "entities" not in data:
        raise ValueError(f"Invalid JSON file: {json_file}")

    # Split up variables
    meta_vars, scalar_vars, multi_vars = _unpack_variables(data)

    # Output files
    scalar_file = csv_prefix + "-single-value-traits.csv"
    multi_file = csv_prefix + "-multi-value-traits.csv"

    # Create a CSV file of vector traits
    with open(multi_file, "w") as csv:
        # Create a header for the long-format table
        csv.write(",".join(map(str, meta_vars + ["sample", "trait", "value", "label"])) + "\n")
        # Iterate over each entity
        for entity in data["entities"]:
            # Add metadata variables
            meta_row = _create_metadata_row(meta_vars=meta_vars, metadata=entity["metadata"])
            # Add trait variables
            for sample, var in itertools.product(entity["observations"].keys(), multi_vars):
                data_rows = _create_data_rows(var=var, obs=entity["observations"][sample])
                for row in data_rows:
                    csv.write(",".join(map(str, meta_row + [sample] + row)) + "\n")

    # Create a CSV file of scalar traits
    # Initialize a dictionary to store the data
    scalar_data = {
        "sample": [],
        "trait": [],
        "value": [],
        "label": []
    }
    # Add metadata terms to the dictionary
    for var in meta_vars:
        scalar_data[var] = []
    # Iterate over each entity
    for entity in data["entities"]:
        # Add metadata variables
        meta_row = _create_metadata_row(meta_vars=meta_vars, metadata=entity["metadata"])
        # Add trait variables
        for sample, var in itertools.product(entity["observations"].keys(), scalar_vars):
            data_rows = _create_data_rows(var=var, obs=entity["observations"][sample])
            for row in data_rows:
                scalar_data["sample"].append(sample)
                scalar_data["trait"].append(row[0])
                scalar_data["value"].append(row[1])
                scalar_data["label"].append(row[2])
                # Add metadata variables
                for i, _ in enumerate(meta_vars):
                    scalar_data[meta_vars[i]].append(meta_row[i])
    # Create a pandas dataframe from the dictionary
    df = pd.DataFrame(scalar_data)
    # Pivot the dataframe to wide format
    # If duplicate indices exist, use the last set of observations are kept
    df = df.pivot_table(index=meta_vars + ["sample"], columns=["trait", "label"], values="value", aggfunc=_last_index)
    # Collapse hierarchical column headers
    df.columns = [f"{c[0]}_{c[1]}" for c in df.columns]
    # Save the dataframe to a CSV file
    df.to_csv(scalar_file)


def _unpack_variables(data):
    """Unpack variables from "variables" key of outputs
    Parameters
    ----------
    data       = dict, json file

    Return
    ------
    meta_vars   = list, variable names that are metadata
    scalar_vars = list, variable names that are single-value traits
    multi_vars  = list, variable names that are multi-value traits

    """
    # Split up variables
    meta_vars = []
    scalar_vars = []
    multi_vars = []
    for key, var in data["variables"].items():
        # Metadata variables
        if var["category"] == "metadata":
            meta_vars.append(key)
        # Data variables
        else:
            # Scalar variables
            if var["datatype"] in ["<class 'bool'>", "<class 'int'>", "<class 'float'>", "<class 'str'>",
                                   "<type 'bool'>", "<type 'int'>", "<type 'float'>", "<type 'str'>"]:
                scalar_vars.append(key)
            # Vector variables
            if var["datatype"] in ["<class 'list'>", "<type 'list'>", "<class 'tuple'>", "<type 'tuple'>"]:
                multi_vars.append(key)
    return meta_vars, scalar_vars, multi_vars


def _last_index(*args):
    """Aggregation function to return the last index of a list."""
    return np.array(args[-1])[-1]


def _create_metadata_row(meta_vars, metadata):
    """Create a row of metadata.

    Parameters
    ----------
    meta_vars : list
        List of metadata terms
    metadata : dict
        Metadata dictionary

    Returns
    -------
    list
        List of metadata values
    """
    meta_row = []
    for var in meta_vars:
        val = "NA"
        if var in metadata:
            vals = metadata[var]["value"]
            vals = ["none" if v is None else v for v in vals]
            # Create a unique list if there are multiple values
            u_list = np.unique(vals).tolist()
            # If there are multiple values, join them with an underscore
            val = "_".join(map(str, u_list))
        meta_row.append(val)
    return meta_row


def _create_data_rows(var, obs):
    """Create rows of data for a variable.

    Parameters
    ----------
    var : str
        Variable name
    obs : dict
        Data dictionary

    Returns
    -------
    list
        List of lists of data rows
    """
    data_rows = []
    if var in obs:
        value = obs[var]["value"]
        label = obs[var]["label"]
        if isinstance(value, bool):
            value = int(value)
        if isinstance(value, (list, tuple)):
            for val, lbl in zip(value, label):
                if not isinstance(val, tuple):
                    data_rows.append([var, val, lbl])
        else:
            data_rows.append([var, value, label])
    else:
        data_rows.append([var, "NA", "NA"])
    return data_rows
