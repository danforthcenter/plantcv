# Print Numerical Data

import json
import csv
import os
from plantcv.plantcv import outputs


def print_results(filename):
    """Print result table

    Inputs:
    filename = filename

    :param filename: str
    :return:
    """

    # READ METADATA TEMP FILE AND ADD MEASUREMENTS TO META DATA DICTIONARY
    meta_data = []

    hierarchical_data = {}
    hierarchical_data['metadata'] = {}
    hierarchical_data['observations'] = outputs.observations

    exists = os.path.isfile(filename)
    if exists:
        with open(filename, 'r') as f:
            reader = csv.reader(f, dialect='excel', delimiter='\t')
            for row in reader:
                meta_data.append(row)
        for i, item in enumerate(meta_data):
            if item[0] == "META":
                hierarchical_data['metadata'][item[1]] = item[2]

    with open(filename, mode='w') as f:
        json.dump(hierarchical_data, f)
