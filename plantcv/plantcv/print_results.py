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

    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            hierarchical_data = json.load(f)
            hierarchical_data["observations"] = outputs.observations
    else:
        hierarchical_data = {"metadata": {}, "observations": outputs.observations}

    with open(filename, mode='w') as f:
        json.dump(hierarchical_data, f)
