import os
import json
import itertools


def json2csv(json_file, csv_file):
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
    meta_vars = []
    trait_vars = []
    for key, var in data["variables"].items():
        if var["category"] == "metadata":
            meta_vars.append(key)
        else:
            trait_vars.append(key)

    # Create a CSV file of traits
    with open(csv_file, "w") as csv:
        # Create a header for the long-format table
        csv.write(",".join(map(str, meta_vars + ["sample", "trait", "value", "label"])) + "\n")
        # Iterate over each entity
        for entity in data["entities"]:
            # Add metadata variables
            meta_row = _create_metadata_row(meta_vars=meta_vars, metadata=entity["metadata"])
            # Add trait variables
            for sample, var in itertools.product(entity["observations"].keys(), trait_vars):
                data_rows = _create_data_rows(var=var, obs=entity["observations"][sample])
                for row in data_rows:
                    csv.write(",".join(map(str, meta_row + [sample] + row)) + "\n")


def _create_metadata_row(meta_vars, metadata):
    meta_row = []
    for var in meta_vars:
        val = "NA"
        if var in metadata:
            val = "_".join(map(str, metadata[var]["value"]))
        meta_row.append(val)
    return meta_row


def _create_data_rows(var, obs):
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


def tabulate_bayes_classes(input_file, output_file):
    """Tabulate pixel RGB values into a table for naive Bayes training.
    Inputs:
    input_file   = Input text file of class names and RGB values
    output_file  = Output file for storing the tab-delimited naive Bayes training data

    The input file should have class names preceded by the "#" character. RGB values can be pasted
    directly from ImageJ without reformatting. E.g.:

    #plant
    96,154,72	95,153,72	91,155,71	91,160,70	90,155,67	92,152,66	92,157,70
    54,104,39	56,104,38	59,106,41	57,105,43	54,104,40	54,103,35	56,101,39	58,99,41	59,99,41
    #background
    114,127,121	117,135,125	120,137,131	132,145,138	142,154,148	151,166,158	160,182,172
    115,125,121	118,131,123	122,132,135	133,142,144	141,151,152	150,166,158	159,179,172

    :param input_file: str
    :param output_file: str
    """
    # If the input file does not exist raise an error
    if not os.path.exists(input_file):
        raise IOError("File does not exist: {0}".format(input_file))

    # Read the file into a string
    with open(input_file, "r") as fd:
        pixel_data = fd.read()

    # Split the file string by the classname/header character
    classes = pixel_data.split("#")

    # Parse the class data
    class_dict = {}
    # Ignore the first item, it's the empty string or whitespace to the "left" of the first class/header
    for i in range(1, len(classes)):
        # Replace tabs with newlines
        classes[i] = classes[i].replace("\t", "\n")
        # Split the class data on newlines
        class_data = classes[i].split("\n")
        # The class name is the first item
        class_name = class_data[0]
        rgb_values = []
        # Loop over the RGB values, starting with the second element
        for j in range(1, len(class_data)):
            # Skip blank lines but keep the lines with RGB values
            if len(class_data[j]) > 0:
                rgb_values.append(class_data[j])
        class_dict[class_name] = rgb_values

    # Each class could have a different number of RGB values, find the largest
    total_rgb = 0
    for class_name in class_dict:
        if len(class_dict[class_name]) > total_rgb:
            total_rgb = len(class_dict[class_name])

    # Pad the classes with empty strings if they have less than the total RGB values
    for class_name in class_dict:
        missing = total_rgb - len(class_dict[class_name])
        if missing > 0:
            for i in range(missing):
                class_dict[class_name].append("")

    # Open the output file
    out = open(output_file, "w")
    # Create the output table
    class_names = class_dict.keys()
    out.write("\t".join(map(str, class_names)) + "\n")
    for i in range(0, total_rgb):
        row = []
        for class_name in class_names:
            row.append(class_dict[class_name][i])
        out.write("\t".join(map(str, row)) + "\n")
    out.close()
