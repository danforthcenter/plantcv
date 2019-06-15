#!/usr/bin/env python

import sys
import argparse
import plantcv.utils


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
    json2csv_cmd = subparsers.add_parser("json2csv", help="Convert PlantCV output JSON files to CSV.")
    json2csv_cmd.add_argument("-j", "--json", help="Input PlantCV JSON filename.", required=True)
    json2csv_cmd.add_argument("-c", "--csv", help="Output CSV filename prefix.", required=True)
    json2csv_cmd.set_defaults(func=run_json2csv)

    # If no arguments are given, print the help menu
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Parse command-line options
    args = parser.parse_args()
    # Execute the selected method
    args.func(args)

###########################################


# run_json2csv
###########################################
def run_json2csv(args):
    plantcv.utils.json2csv(json_file=args.json, csv_file=args.csv)
###########################################


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
