# Print Numerical Data

import json
import csv
from plantcv.plantcv import outputs


def print_results(filename):
    """Print result table

    Inputs:
    filename = filename

    :param filename: str
    :return:
    """
    # Open a new text file
    result = open(filename, "a")

    with open(filename, 'a') as outfile:
        json.dump(outputs.observations, outfile)


    # hierarchical_data = {}
    # with open(filename) as feedsjson:
    #     feeds = json.load(feedsjson)
    #
    # hierarchical_data["metadata"] = feeds
    # hierarchical_data["observations"] = outputs.observations
    # with open(filename, mode='w') as f:
    #     json.dump(hierarchical_data, filename)


    # with open(filename) as feedsjson:
    #     feeds = json.load(feedsjson)
    #
    #
    # feeds.update({'observations' : outputs.observations})
    # with open(filename, mode='w') as f:
    #     f.write(json.dumps(feeds, indent=2))

    # READ METADATA TEMP FILE AND ADD MEASURMENTS TO META DATA DICT
    # meta_data = []
    #
    # with open(filename, 'r') as f:
    #     reader = csv.reader(f, dialect='excel', delimiter='\t')
    #     for row in reader:
    #         meta_data.append(row)
    #
    # hierarchical_data = {}
    # hierarchical_data['metadata'] = {}
    # hierarchical_data['observations'] = outputs.observations
    #
    # for i, item in enumerate(meta_data):
    #     if item[0] == "META":
    #         hierarchical_data['metadata'][item[1]] = item[2]
    #
    # with open(filename, mode='w') as f:
    #     json.dump(hierarchical_data, filename)

