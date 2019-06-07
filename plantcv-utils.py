#!/usr/bin/env python

import os
import argparse
import json


# Parse command-line arguments
###########################################
def options():
    """Parse command line options.
    """

    # Create an argument parser
    parser = argparse.ArgumentParser(description="A collection of utilities for PlantCV.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # Create subcommand parsers
    subparsers = parser.add_subparsers()

    # Create the Naive Bayes subcommand
    nb_cmd = subparsers.add_parser("json2csv", help="Convert PlantCV output JSON files to CSV.")
    nb_cmd.add_argument("-j", "--json", help="Input PlantCV JSON filename.", required=True)
    nb_cmd.add_argument("-c", "--csv", help="Output CSV filename.", required=True)
    nb_cmd.set_defaults(func=json2csv)

    # Parse command-line options
    args = parser.parse_args()
    # Execute the selected method
    args.func(args)


###########################################


def json2csv(args):
    if os.path.exists(args.json):
        # If the JSON file exists open it for reading
        json_data = open(args.json, "r")
        data = json.load(json_data)
        # If the data is JSON but it does not have the components we expect from PlantCV raise an error
        if "variables" not in data or "entities" not in data:
            raise ValueError("Invalide JSON file: {0}".format(args.json))

        # Open the output CSV file for writing
        csv = open(args.csv, "w")

        

        # Close the CSV file
        csv.close()
    else:
        # If the file does not exist raise an error
        raise IOError("File does not exist: {0}".format(args.json))


# Main
###########################################
def main():
    """Main program.
    """
    # Parse command-line options and run the selected method
    options()


###########################################


if __name__ == '__main__':
    main()
