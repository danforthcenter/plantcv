import os
import json


def json2csv(json_file, csv_file):
    if os.path.exists(json_file):
        # If the JSON file exists open it for reading
        json_data = open(json_file, "r")
        data = json.load(json_data)
        # If the data is JSON but it does not have the components we expect from PlantCV raise an error
        if "variables" not in data or "entities" not in data:
            raise ValueError("Invalid JSON file: {0}".format(json_file))

        # Split up variables
        meta_vars = []
        scalar_vars = []
        multi_vars = []
        for key, var in data["variables"].items():
            if var["category"] == "metadata":
                meta_vars.append(key)
            elif var["datatype"] in ["<class 'bool'>", "<class 'int'>", "<class 'float'>", "<class 'str'>"]:
                scalar_vars.append(key)
            elif var["datatype"] in ["<class 'list'>"]:
                multi_vars.append(key)

        # Create a CSV file of single-value traits
        csv = open(csv_file + "-single-value-traits.csv", "w")

        # Build the single-value variables output table
        csv.write(",".join(map(str, meta_vars + scalar_vars)) + "\n")
        for entity in data["entities"]:
            row = []
            # Add metadata variables
            for var in meta_vars:
                obs = entity[data["variables"][var]["category"]]
                if var in obs:
                    row.append(obs[var]["value"])
                else:
                    row.append("NA")
            # Add scalar variables
            for var in scalar_vars:
                obs = entity[data["variables"][var]["category"]]
                if var in obs:
                    row.append(obs[var]["value"])
                else:
                    row.append("NA")
            csv.write(",".join(map(str, row)) + "\n")
        # Close the CSV file
        csv.close()

        # Create a CSV file of multi-value variables
        csv = open(csv_file + "-multi-value-traits.csv", "w")
        csv.write(",".join(map(str, meta_vars + ["trait", "value", "label"])) + "\n")
        for entity in data["entities"]:
            meta_row = []
            # Add metadata variables
            for var in meta_vars:
                obs = entity[data["variables"][var]["category"]]
                if var in obs:
                    meta_row.append(obs[var]["value"])
                else:
                    meta_row.append("NA")
            # Add multi-value variables
            for var in multi_vars:
                obs = entity[data["variables"][var]["category"]]
                if var in obs:
                    if obs[var]["label"] != "none":
                        for i in range(0, len(obs[var]["value"])):
                            row = [var]
                            row.append(obs[var]["value"][i])
                            row.append(obs[var]["label"][i])
                            csv.write(",".join(map(str, meta_row + row)) + "\n")
                else:
                    csv.write(",".join(map(str, meta_row + [var, "NA", "NA"])) + "\n")
        csv.close()
    else:
        # If the file does not exist raise an error
        raise IOError("File does not exist: {0}".format(json_file))
